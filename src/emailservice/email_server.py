#!/usr/bin/python
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent import futures
import grpc
import time
import traceback
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateError

import demo_pb2
import demo_pb2_grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc

from logger import getJSONLogger
logger = getJSONLogger('emailservice-server')

# Load email template
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('confirmation.html')


class BaseEmailService(demo_pb2_grpc.EmailServiceServicer):
    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING
        )

    def Watch(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.UNIMPLEMENTED
        )


class EmailService(BaseEmailService):
    def __init__(self):
        # Read SMTP config from environment
        self.smtp_server = os.environ.get("SMTP_SERVER")
        self.smtp_port = int(os.environ.get("SMTP_PORT", 587))
        self.smtp_user = os.environ.get("SMTP_USER")
        self.smtp_pass = os.environ.get("SMTP_PASS")
        if not all([self.smtp_server, self.smtp_port, self.smtp_user, self.smtp_pass]):
            raise Exception("SMTP configuration is incomplete!")
        logger.info("EmailService initialized in real mode.")

    def send_email(self, email_address, content):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = email_address
        msg['Subject'] = "Your Confirmation Email"
        msg.attach(MIMEText(content, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            logger.info(f"Email sent successfully to {email_address}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise

    def SendOrderConfirmation(self, request, context):
        email = request.email
        order = request.order
        try:
            confirmation = template.render(order=order)
        except TemplateError as err:
            context.set_details("Error rendering email template.")
            context.set_code(grpc.StatusCode.INTERNAL)
            logger.error(err)
            return demo_pb2.Empty()

        try:
            self.send_email(email, confirmation)
        except Exception as err:
            context.set_details("Error sending email.")
            context.set_code(grpc.StatusCode.INTERNAL)
            logger.error(err)
            return demo_pb2.Empty()

        return demo_pb2.Empty()


class DummyEmailService(BaseEmailService):
    def SendOrderConfirmation(self, request, context):
        logger.info(f"A request to send order confirmation email to {request.email} has been received.")
        return demo_pb2.Empty()


def start_server(dummy_mode):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = DummyEmailService() if dummy_mode else EmailService()
    demo_pb2_grpc.add_EmailServiceServicer_to_server(service, server)
    health_pb2_grpc.add_HealthServicer_to_server(service, server)

    port = os.environ.get("PORT", "8080")
    logger.info(f"Listening on port: {port}")
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    dummy_mode = os.environ.get("DUMMY_MODE", "1") == "1"
    logger.info(f"Starting email service. Dummy mode: {dummy_mode}")
    start_server(dummy_mode)
