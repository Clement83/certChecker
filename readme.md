# Certs API

This project provides an API to list SSL certificates from **Let's Encrypt** and their expiration dates. The API is designed to run inside a Docker container and is built using **Flask**.

### Features
- List all SSL certificates stored in `/etc/letsencrypt/live`
- Check certificate expiration and remaining days
- Filter certificates by the remaining days using the `warn_days` query parameter

---

## 🚀 How to Run

To get started with the project, follow these steps:

### 1. Clone the repository
```bash
git clone https://your-repository-url.git
cd certs-api
```

### 2. Build and Start with Docker Compose
Run the following command to build and start the application with Docker Compose:
```bash
docker compose up --build -d
```

### 3. Access the API
Once the container is running, you can access the API at `http://<your-server-ip>:8000/certs`.

For example, to get all certificates:
```
GET /certs
```

To filter certificates that will expire within 30 days:
```
GET /certs?warn_days=30
```

### 4. Access Logs
To view logs of the application, use the following Docker command:
```bash
docker compose logs -f
```

---

## ⚙️ Configuration

By default, the application uses the directory `/etc/letsencrypt/live` to retrieve SSL certificates.

### Docker Volume Mount
In the `docker-compose.yml` file, the `/etc/letsencrypt` directory from the host is mounted as read-only into the container under `/certs`:
```yaml
volumes:
  - /etc/letsencrypt:/certs:ro
```

Ensure that the host directory `/etc/letsencrypt` contains the SSL certificates for the Let's Encrypt setup.

---

## 🛠️ Development Mode

If you're in development mode and want to edit files without rebuilding the container every time, you can mount the `app/` directory as a volume:
```yaml
volumes:
  - ./app:/app
```

This will allow changes to the `certs_api.py` file to take effect without rebuilding the container.

---

## 🐳 Docker Compose Configuration

The `docker-compose.yml` file is set up to:
- Build the Docker image from the `Dockerfile`
- Expose port `8000` for the API
- Mount the `letsencrypt` directory to access certificates

### Example `docker-compose.yml`:
```yaml
version: "3.8"

services:
  certs-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - /etc/letsencrypt:/certs:ro
    restart: unless-stopped
```

---

## 📝 Logging

The API logs relevant actions such as certificate loading, errors, and filtering operations. You can monitor the logs to troubleshoot or view activity:

```bash
docker compose logs -f
```

---

## 💬 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
