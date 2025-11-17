# Database Reset Guide

This guide explains how to reset the publishing module database to a fresh state.

## Quick Reset

To reset the database (drops all tables and recreates them):

```bash
python3 scripts/reset_database.py
```

The script will:
1. ⚠️  Warn you that all data will be deleted
2. Ask for confirmation (type `yes` to continue)
3. Drop all existing tables
4. Recreate all tables from scratch
5. Confirm successful reset

## Alternative: Docker Volume Reset

If you're using Docker and want a completely fresh database (including PostgreSQL initialization):

```bash
# Stop containers
/Applications/Docker.app/Contents/Resources/bin/docker compose down

# Remove the database volume (this deletes all data)
/Applications/Docker.app/Contents/Resources/bin/docker compose down -v

# Start fresh
/Applications/Docker.app/Contents/Resources/bin/docker compose up -d postgres redis

# Wait for services to be ready, then tables will be auto-created on next API startup
```

## What Gets Reset

- **Channels**: All channel configurations
- **Subscribers**: All subscriber profiles and preferences
- **Publications**: All scheduled and sent publications
- **Templates**: All email templates
- **Analytics**: All analytics data

## After Reset

After resetting, you'll need to:

1. **Create channels** - Use the frontend or API to create channels
2. **Create subscribers** - Add subscribers with their channel preferences
3. **Schedule publications** - Create new publications for testing

The frontend is available at: http://localhost:3000

## Safety

⚠️ **Warning**: Database reset is permanent and cannot be undone!

Make sure to:
- Export important data before resetting (if needed)
- Confirm you want to reset when prompted
- Only use in development/testing environments

