#!/usr/bin/env bash
# Setup PostgreSQL databases for local development

echo "Setting up PostgreSQL databases..."
echo ""

DATABASES=("auth" "users" "listings" "offers" "payments" "notifications" "chat" "admin")

for db in "${DATABASES[@]}"; do
    echo "Creating database: $db"
    createdb -h localhost -U postgres "$db" 2>/dev/null || echo "  (already exists or error)"
done

echo ""
echo "Connection strings for .env:"
for db in "${DATABASES[@]}"; do
    echo "postgresql://postgres:password@localhost:5432/$db"
done
