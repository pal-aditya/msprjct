# ---- Build Stage ----
FROM golang:1.23.4-alpine AS builder
WORKDIR /app

# Download dependencies first (better caching)
COPY go.mod go.sum ./
RUN go mod download

# Copy the source
COPY . .

# Build the Go binary (static build)
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o server .

# ---- Runtime Stage ----
FROM scratch
WORKDIR /app

# Copy binary and assets
COPY --from=builder /app/server /app/server
COPY ./templates ./templates
COPY ./static ./static

# Show stack trace on crash
ENV GOTRACEBACK=single

EXPOSE 8080
ENTRYPOINT ["/app/server"]
