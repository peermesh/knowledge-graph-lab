# Docker Setup

## Quick Start

Add to your `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    env_file:
      - .env
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_REGION=${AWS_REGION}
      - SES_FROM_EMAIL=${SES_FROM_EMAIL}
    ports:
      - "3000:3000"
```

Your `.env` file:
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-2
SES_FROM_EMAIL=noreply@distributedcreatives.org
```

That's it. Start with `docker-compose up`.

## Full Example

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: email-app
    env_file:
      - .env
    environment:
      - NODE_ENV=production
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_REGION=${AWS_REGION}
      - SES_FROM_EMAIL=${SES_FROM_EMAIL}
    ports:
      - "3000:3000"
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

**Dockerfile:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

## Testing

```bash
# Build and run
docker-compose up --build

# Test email endpoint
curl -X POST http://localhost:3000/api/email/test \
  -H "Content-Type: application/json" \
  -d '{"to":"your@email.com","subject":"Test","body":"Works!"}'
```

## Security

Never commit `.env` - add to `.gitignore`:
```
.env
.env.local
.env.*.local
```
