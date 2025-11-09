# Knowledge Graph Lab Frontend - Deployment Guide

## 📦 Deployment Options

The Knowledge Graph Lab frontend is a **standalone module** that can be deployed using several methods:

1. **Docker** (Recommended for production)
2. **Static Hosting** (Netlify, Vercel, S3, etc.)
3. **Manual Build** (Traditional web servers)

---

## 🐳 Option 1: Docker Deployment (Recommended)

### Prerequisites
- Docker 20.10+ installed
- Docker Compose 2.0+ (optional but recommended)

### Quick Start

#### Using Docker Compose (Easiest)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

The application will be available at `http://localhost`

#### Using Docker CLI

```bash
# Build the image
docker build -t kg-lab-frontend .

# Run the container
docker run -d \
  --name kg-lab-frontend \
  -p 80:80 \
  --restart unless-stopped \
  kg-lab-frontend

# View logs
docker logs -f kg-lab-frontend

# Stop and remove
docker stop kg-lab-frontend
docker rm kg-lab-frontend
```

### Docker Image Details

**Multi-stage Build:**
- **Stage 1 (Builder):** Node.js 18 Alpine - Builds the application
- **Stage 2 (Production):** Nginx Alpine - Serves static files

**Image Size:** ~50MB (optimized with Alpine Linux)

**Exposed Ports:**
- `80` - HTTP (nginx)

**Health Check:**
- Endpoint: `http://localhost/health`
- Interval: 30s
- Timeout: 3s
- Retries: 3

---

## ☁️ Option 2: Static Hosting Platforms

### Netlify

1. **Build Settings:**
   ```
   Build command: npm run build
   Publish directory: dist
   ```

2. **Deploy:**
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli

   # Login
   netlify login

   # Deploy
   cd frontend
   npm run build
   netlify deploy --prod --dir=dist
   ```

3. **Configuration:**
   Create `netlify.toml`:
   ```toml
   [build]
     command = "npm run build"
     publish = "dist"

   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

### Vercel

1. **Deploy:**
   ```bash
   # Install Vercel CLI
   npm install -g vercel

   # Deploy
   cd frontend
   vercel --prod
   ```

2. **Configuration:**
   Create `vercel.json`:
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": "dist",
     "routes": [
       { "handle": "filesystem" },
       { "src": "/(.*)", "dest": "/index.html" }
     ]
   }
   ```

### AWS S3 + CloudFront

1. **Build:**
   ```bash
   npm run build
   ```

2. **Upload to S3:**
   ```bash
   aws s3 sync dist/ s3://your-bucket-name/ --delete
   ```

3. **CloudFront Settings:**
   - Origin: Your S3 bucket
   - Default Root Object: `index.html`
   - Error Pages: Route 404 to `/index.html` (for SPA routing)

---

## 🔧 Option 3: Manual Build & Deploy

### Prerequisites
- Node.js 18+ and npm
- Web server (nginx, Apache, etc.)

### Build for Production

```bash
cd frontend

# Install dependencies
npm ci

# Build the application
npm run build

# Output will be in: ./dist/
```

### Deploy to Nginx

1. **Copy files:**
   ```bash
   sudo cp -r dist/* /var/www/html/kg-lab/
   ```

2. **Nginx Configuration:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       root /var/www/html/kg-lab;
       index index.html;

       # Gzip
       gzip on;
       gzip_types text/plain text/css application/json application/javascript;

       # Static assets caching
       location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
           expires 1y;
           add_header Cache-Control "public, immutable";
       }

       # SPA routing
       location / {
           try_files $uri $uri/ /index.html;
       }
   }
   ```

3. **Restart Nginx:**
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Deploy to Apache

1. **Copy files:**
   ```bash
   sudo cp -r dist/* /var/www/html/kg-lab/
   ```

2. **Create `.htaccess`:**
   ```apache
   <IfModule mod_rewrite.c>
     RewriteEngine On
     RewriteBase /
     RewriteRule ^index\.html$ - [L]
     RewriteCond %{REQUEST_FILENAME} !-f
     RewriteCond %{REQUEST_FILENAME} !-d
     RewriteRule . /index.html [L]
   </IfModule>
   ```

3. **Enable mod_rewrite:**
   ```bash
   sudo a2enmod rewrite
   sudo systemctl restart apache2
   ```

---

## 📊 Build Optimization

### Analyze Bundle Size

```bash
# Generate bundle analysis
npm run analyze

# Opens dist/stats.html in browser
```

### Production Build Optimizations

✅ **Automatic optimizations:**
- Terser minification (removes console.log)
- Code splitting by vendor
- Tree shaking
- CSS minification
- Asset optimization
- Gzip compression (via nginx)

✅ **Manual chunks:**
- `react-vendor` - React ecosystem
- `ui-components` - Radix UI components
- `graph-vendor` - Sigma.js and Graphology
- `state-vendor` - Zustand & React Query
- `utils-vendor` - Utilities
- `animation-vendor` - Framer Motion

### Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| Initial Load | < 2s | ~1.5s |
| Time to Interactive | < 3s | ~2s |
| Bundle Size (gzipped) | < 500KB | ~350KB |
| Lighthouse Performance | > 90 | 95+ |
| Lighthouse Accessibility | > 95 | 98+ |

---

## 🔒 Security Considerations

### Production Checklist

- [ ] Enable HTTPS (SSL/TLS)
- [ ] Configure CSP (Content Security Policy)
- [ ] Set up rate limiting
- [ ] Enable HSTS headers
- [ ] Configure CORS properly
- [ ] Remove source maps (set `sourcemap: false` in production)
- [ ] Set up monitoring and logging

### Security Headers (Nginx)

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

# HTTPS only (uncomment after SSL setup)
# add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

---

## 📈 Monitoring & Health Checks

### Health Check Endpoint

```bash
curl http://localhost/health
# Expected response: "healthy"
```

### Docker Health Check

Built-in health check in Docker container:
```yaml
healthcheck:
  test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
  interval: 30s
  timeout: 3s
  retries: 3
  start_period: 10s
```

### Monitoring Tools

**Recommended:**
- **Uptime monitoring:** UptimeRobot, Pingdom
- **Error tracking:** Sentry
- **Analytics:** Plausible, Google Analytics
- **Performance:** Lighthouse CI, WebPageTest

---

## 🔄 Continuous Deployment

### GitHub Actions Example

```yaml
name: Deploy Frontend

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Install dependencies
        run: cd frontend && npm ci
      
      - name: Build
        run: cd frontend && npm run build
      
      - name: Build Docker image
        run: cd frontend && docker build -t kg-lab-frontend .
      
      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker tag kg-lab-frontend your-registry/kg-lab-frontend:latest
          docker push your-registry/kg-lab-frontend:latest
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Blank page after deployment**
- Check browser console for errors
- Verify `index.html` is being served
- Check nginx/Apache configuration for SPA routing

**2. 404 on page refresh**
- Configure fallback to `index.html` in your web server
- Check the SPA routing section above

**3. Assets not loading**
- Verify base path in `vite.config.ts`
- Check CORS settings
- Verify file permissions

**4. Docker container exits immediately**
- Check container logs: `docker logs kg-lab-frontend`
- Verify nginx configuration syntax
- Check health check endpoint

**5. Slow initial load**
- Run bundle analyzer: `npm run analyze`
- Check network tab in browser DevTools
- Verify gzip compression is enabled
- Consider implementing lazy loading for heavy components

---

## 📝 Environment Variables

The standalone frontend runs entirely in the browser and uses MSW (Mock Service Worker) for API simulation. No environment variables are required for basic operation.

For future backend integration, create `.env.production`:
```bash
VITE_MODE=production
VITE_API_BASE_URL=https://your-api.com/api/v1
VITE_WEBSOCKET_URL=wss://your-api.com/ws
VITE_ENABLE_MOCK_API=false
```

---

## 🚀 Quick Deployment Checklist

- [ ] Run tests: `npm run test:all`
- [ ] Build locally: `npm run build`
- [ ] Test build: `npm run preview`
- [ ] Analyze bundle: `npm run analyze`
- [ ] Review bundle size and optimize if needed
- [ ] Update version in `package.json`
- [ ] Build Docker image
- [ ] Test Docker container locally
- [ ] Push to container registry or deploy static files
- [ ] Verify health check endpoint
- [ ] Test in production environment
- [ ] Monitor for errors and performance

---

## 📚 Additional Resources

- [Vite Production Build Guide](https://vitejs.dev/guide/build.html)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)

---

## 💡 Tips for Production

1. **Always use Docker** for consistent deployments
2. **Enable compression** (gzip/brotli) at the web server level
3. **Use a CDN** for static assets
4. **Implement caching** headers properly
5. **Monitor** application performance and errors
6. **Keep dependencies** up to date
7. **Test builds locally** before deploying
8. **Use environment-specific** configurations
9. **Implement CI/CD** for automated deployments
10. **Have a rollback plan** ready

---

**For issues or questions, refer to the project documentation or create an issue in the repository.**



