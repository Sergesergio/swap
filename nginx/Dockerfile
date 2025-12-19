FROM nginx:1.25-alpine

# Install tools for health checks
RUN apk add --no-cache curl

# Copy nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Create cache directories
RUN mkdir -p /var/cache/nginx/general /var/cache/nginx/api && \
    chown -R nginx:nginx /var/cache/nginx

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
