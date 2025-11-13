# Docker Deployment Guide

## Prerequisites
- Docker installed
- Docker Compose installed
- API keys for Gemini, Heygen, and Creatomate

## Quick Start

### 1. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 2. Build and Run with Docker Compose
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Access Application
- Application: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Redis: localhost:6379

## Docker Services

### App Service
- **Container**: ai-video-automation
- **Port**: 8000
- **Volumes**:
  - `./generated_images` - Generated background images
  - `./uploads` - Uploaded files
- **Environment**:
  - DATABASE_URL - PostgreSQL connection
  - REDIS_HOST/PORT - Redis connection
  - API keys for external services

### Redis Service
- **Container**: ai-video-redis
- **Port**: 6379
- **Volume**: redis-data (persistent storage)
- **Image**: redis:7-alpine

## Manual Docker Build

```bash
# Build image
docker build -t ai-video-automation .

# Run container
docker run -d \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e HEYGEN_API_KEY=your_key \
  -e CREATOMATE_API_KEY=your_key \
  -v $(pwd)/generated_images:/app/generated_images \
  -v $(pwd)/uploads:/app/uploads \
  --name ai-video-automation \
  ai-video-automation
```

## Database Initialization

```bash
# Run inside container
docker-compose exec app python init_db.py
```

## Useful Commands

```bash
# View app logs
docker-compose logs -f app

# View Redis logs
docker-compose logs -f redis

# Restart app
docker-compose restart app

# Execute command in container
docker-compose exec app python -c "print('Hello')"

# Access container shell
docker-compose exec app bash

# Remove all containers and volumes
docker-compose down -v
```

## Production Deployment

### 1. Update docker-compose.yml
- Remove port exposure for Redis (use internal network only)
- Add resource limits
- Configure proper restart policies
- Use secrets for sensitive data

### 2. Use External Services
```yaml
environment:
  - DATABASE_URL=postgresql://user:pass@external-db:5432/db
  - REDIS_HOST=external-redis-host
  - REDIS_PORT=6379
```

### 3. Enable HTTPS
Use nginx or traefik as reverse proxy:
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs app

# Check if ports are available
netstat -an | grep 8000
```

### Database connection error
```bash
# Test database connection
docker-compose exec app python -c "from app.core.Database import engine; print(engine.connect())"
```

### Redis connection error
```bash
# Test Redis connection
docker-compose exec app python -c "from app.core.WorkflowStorage import workflow_storage; print(workflow_storage.redis_client.ping())"
```

### Permission issues
```bash
# Fix permissions
sudo chown -R $USER:$USER generated_images uploads
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | Required |
| REDIS_HOST | Redis host | 149.129.238.126 |
| REDIS_PORT | Redis port | 6379 |
| GEMINI_API_KEY | Google Gemini API key | Required |
| HEYGEN_API_KEY | Heygen API key | Required |
| CREATOMATE_API_KEY | Creatomate API key | Required |
| SECRET_KEY | JWT secret key | Required |

## Volume Management

### Backup volumes
```bash
# Backup generated images
docker run --rm -v ai-automation-v2_redis-data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz /data
```

### Restore volumes
```bash
# Restore Redis data
docker run --rm -v ai-automation-v2_redis-data:/data -v $(pwd):/backup alpine tar xzf /backup/redis-backup.tar.gz -C /
```

## Scaling

### Multiple app instances
```bash
docker-compose up -d --scale app=3
```

Note: Requires load balancer configuration.

## Monitoring

### Health check
```bash
curl http://localhost:8000/
```

### Redis stats
```bash
docker-compose exec redis redis-cli INFO
```

### Container stats
```bash
docker stats ai-video-automation ai-video-redis
```
