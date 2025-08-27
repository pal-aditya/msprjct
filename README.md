# msprjct

A microservices-based Kubernetes deployment example containing services such as:

- **adservice**
- **cartservice**
- **checkoutservice**
- **currencyservice**
- **emailservice**
- **frontend**
- **paymentservice**
- **productcatalogservice**
- **recommendationservice**
- **shippingservice**

## Table of Contents

1. [Overview](#overview)  
2. [Prerequisites](#prerequisites)  
3. [Deployment](#deployment)  
4. [Service Descriptions](#service-descriptions)  
5. [Using the Email Service](#using-the-email-service)  
6. [Accessing the Application](#accessing-the-application)  
7. [Cleanup](#cleanup)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## Overview

This project demonstrates a full microservices architecture deployed on Kubernetes. Each component runs as an independent service, with `frontend` acting as the entry point. The services collaborate to simulate an e-commerce-like workflow, providing capabilities such as product browsing, cart management, payment processing, recommendations, shipping, emails, currency conversion, advertisements, and checkout orchestration.

---

## Prerequisites

Ensure you have the following installed:

- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- A running Kubernetes cluster (e.g., Minikube, kind, or a managed cloud cluster)
- (Optional) [helm](https://helm.sh) if you integrate any Helm charts in the future

---

## Deployment

Apply each service manifest:

```sh
kubectl apply -f adservice.yaml
kubectl apply -f cartservice.yaml
kubectl apply -f checkoutservice.yaml
kubectl apply -f currencyservice.yaml
kubectl apply -f emailservice.yaml
kubectl apply -f productcatalogservice.yaml
kubectl apply -f recommendationservice.yaml
kubectl apply -f shippingservice.yaml
kubectl apply -f paymentservice.yaml
kubectl apply -f frontend.yaml
```

You can also apply all at once:

```sh
kubectl apply -f .
```

---

## Service Descriptions

| Service Name               | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| **frontend**               | UI gateway providing the user entry point to the microservices ecosystem.  |
| **productcatalogservice**  | Serves product catalog data.                                                |
| **adservice**              | Returns advertisements to display alongside products.                       |
| **recommendationservice**  | Offers product recommendations based on user context.                       |
| **cartservice**            | Manages user cart operations (add/remove items).                           |
| **checkoutservice**        | Coordinates checkout workflow.                                              |
| **currencyservice**        | Converts prices into different currencies.                                  |
| **paymentservice**         | Processes payments during checkout.                                         |
| **shippingservice**        | Calculates shipping details and cost.                                       |
| **emailservice**           | Sends confirmation emails after purchases. Supports real-time configuration with `ConfigMap` and `Secrets`. |

---

## Using the Email Service

The **Email service** is fully functional. To enable real-time email delivery:

1. Create a **ConfigMap** with your SMTP or email server settings.
2. Create a **Secret** with sensitive values such as username, password, or API keys.
3. Reference the `ConfigMap` and `Secret` in the `emailservice` Deployment YAML.

Example:

```yaml
envFrom:
  - configMapRef:
      name: email-config
  - secretRef:
      name: email-secrets
```

Once configured, the email service can be used in production or development environments to send real emails (e.g., order confirmations).

---

## Accessing the Application

To interact with the deployment:

1. Determine how to expose the `frontend` service:
   - **Minikube**:
     ```sh
     minikube service frontend --url
     ```
   - **Port forwarding**:
     ```sh
     kubectl port-forward svc/frontend 8080:80
     ```
     Then navigate to `http://localhost:8080`.

2. The frontend communicates with backend services through internal Kubernetes networking.

---

## Cleanup

To remove all deployed services:

```sh
kubectl delete -f .
```

---

---

**Enjoy exploring the microservices setup!**  
The Email service is production-ready once configured with your secrets 🔑.
