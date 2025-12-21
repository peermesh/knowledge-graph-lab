# Publishing Module - Backup and Recovery

## Overview

Backup and disaster recovery procedures for the Publishing Module to ensure data integrity and business continuity.

## Recovery Targets

- **RTO (Recovery Time Objective)**: < 1 hour
- **RPO (Recovery Point Objective)**: < 5 minutes
- **Data Retention**: Subscribers (permanent), Analytics (2 years), Publications (1 year)

## Database Backup

### PostgreSQL Backup Strategy

#### Automated Daily Backups

```bash
# Full database backup (daily at 2 AM UTC)
pg_dump -h localhost -U publishing_user -d publishing_db \
  --format=custom --file=backup_$(date +%Y%m%d).dump

# Backup with compression
pg_dump -h localhost -U publishing_user -d publishing_db \
  --format=custom --compress=9 --file=backup_$(date +%Y%m%d).dump.gz
```

#### Continuous Archiving (WAL)

- Enable WAL archiving for point-in-time recovery
- Archive WAL files to S3 with encryption
- Retention: 30 days of WAL logs

```sql
-- Enable WAL archiving in postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'aws s3 cp %p s3://backups/wal/%f'
```

#### Backup Verification

- Weekly restore tests to staging environment
- Automated integrity checks after backup
- Backup size and duration monitoring
- Alert if backup fails or size increases unexpectedly

### Redis Backup Strategy

#### RDB Snapshots

```conf
# redis.conf configuration
save 900 1     # Save after 900 seconds if at least 1 key changed
save 300 10    # Save after 300 seconds if at least 10 keys changed
save 60 10000  # Save after 60 seconds if at least 10000 keys changed
```

#### AOF (Append-Only File)

```conf
# redis.conf configuration
appendonly yes
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

#### Backup Schedule

- Hourly RDB snapshots to S3
- Continuous AOF syncing
- Retention: 7 days of hourly snapshots

## Data Export

### Subscriber Data Export

**Endpoint**: `GET /api/v1/subscribers/export` (to be implemented)

```python
# Export all subscriber data (GDPR compliance)
GET /api/v1/subscribers/export?format=csv
Authorization: Bearer {admin_token}

# Response: CSV file with all subscriber data
# Columns: id, email, preferences, topics, created_at, updated_at
```

### Analytics Data Export

**Endpoint**: `GET /api/v1/analytics/export` (to be implemented)

```python
# Export analytics data for reporting
GET /api/v1/analytics/export?start_date=2025-01-01&end_date=2025-12-31&format=json
Authorization: Bearer {admin_token}

# Response: JSON export of engagement and performance metrics
```

## Disaster Recovery

### Multi-Region Replication

#### Database Replication

- **Primary Region**: us-east-1
- **Secondary Region**: us-west-2
- **Replication**: Async streaming replication
- **Failover**: Automatic with health checks

```sql
-- Set up streaming replication
-- On primary:
CREATE ROLE replication_user WITH REPLICATION LOGIN PASSWORD 'secure_password';

-- On standby:
standby_mode = 'on'
primary_conninfo = 'host=primary-db port=5432 user=replication_user password=secure_password'
trigger_file = '/tmp/trigger_failover'
```

#### Redis Replication

- **Primary**: Master Redis instance
- **Replicas**: 2 read replicas in different AZs
- **Sentinel**: Automatic failover with Redis Sentinel

```bash
# Redis Sentinel configuration
sentinel monitor publishing-master 10.0.1.10 6379 2
sentinel down-after-milliseconds publishing-master 5000
sentinel failover-timeout publishing-master 10000
```

### Failover Procedures

#### Automated Failover

1. Health check detects primary failure
2. Sentinel/K8s triggers failover to standby
3. DNS updated to point to new primary
4. Application reconnects automatically
5. Alert sent to on-call engineer

#### Manual Failover

```bash
# 1. Promote standby to primary
pg_ctl promote -D /var/lib/postgresql/data

# 2. Update application connection string
kubectl set env deployment/publishing-api \
  DATABASE_URL=postgresql://new-primary:5432/publishing_db

# 3. Restart application pods
kubectl rollout restart deployment/publishing-api

# 4. Verify functionality
curl https://api.example.com/health
```

## Data Retention Policies

### Subscriber Data

- **Retention**: Permanent (until user requests deletion)
- **Backup**: Daily full backup + continuous WAL
- **GDPR**: Delete within 30 days of request

### Publication Data

- **Retention**: 1 year
- **Backup**: Daily snapshot
- **Archival**: Move to cold storage after 1 year

### Analytics Data

- **Retention**: 2 years
- **Backup**: Daily snapshot
- **Archival**: Move to cold storage after 6 months

### Audit Logs

- **Retention**: 7 years (compliance)
- **Backup**: Continuous archival to S3
- **Access**: Read-only after 90 days

## Backup Storage

### S3 Bucket Configuration

```yaml
# Backup bucket with lifecycle policies
Bucket: publishing-backups
Region: us-east-1
Encryption: AES-256
Versioning: Enabled

Lifecycle Policies:
  - Rule: Daily backups
    Transition: After 30 days → Glacier
    Expiration: After 2 years
  
  - Rule: WAL logs
    Expiration: After 30 days
  
  - Rule: Redis snapshots
    Transition: After 7 days → Glacier
    Expiration: After 30 days
```

### Backup Costs Optimization

- Compress database backups (9:1 ratio typical)
- Use S3 Intelligent-Tiering for automatic cost optimization
- Lifecycle policies for automatic archival and deletion
- Incremental backups where possible

## Recovery Procedures

### Database Restore

#### Full Database Restore

```bash
# 1. Stop application
kubectl scale deployment/publishing-api --replicas=0

# 2. Restore from backup
pg_restore -h localhost -U publishing_user -d publishing_db \
  --clean --if-exists backup_20251028.dump

# 3. Verify data integrity
psql -U publishing_user -d publishing_db -c "SELECT COUNT(*) FROM publishing_subscribers;"

# 4. Restart application
kubectl scale deployment/publishing-api --replicas=3
```

#### Point-in-Time Recovery

```bash
# 1. Restore base backup
pg_basebackup -h primary-db -D /var/lib/postgresql/data -U replication_user

# 2. Configure recovery
cat > recovery.conf << EOF
restore_command = 'aws s3 cp s3://backups/wal/%f %p'
recovery_target_time = '2025-10-28 14:30:00 UTC'
EOF

# 3. Start PostgreSQL (applies WAL until target time)
pg_ctl start -D /var/lib/postgresql/data
```

### Redis Restore

```bash
# 1. Stop Redis
systemctl stop redis

# 2. Restore RDB file
aws s3 cp s3://backups/redis/dump.rdb /var/lib/redis/dump.rdb

# 3. Start Redis
systemctl start redis

# 4. Verify data
redis-cli DBSIZE
```

## Testing and Validation

### Monthly Restore Tests

- Full database restore to staging environment
- Verify data integrity and application functionality
- Test failover procedures
- Document recovery time and issues

### Quarterly DR Drills

- Simulate region failure
- Execute full disaster recovery procedure
- Test multi-region failover
- Validate RTO/RPO compliance
- Update runbooks based on lessons learned

### Backup Monitoring

- Automated backup success/failure alerts
- Backup size and duration tracking
- Restore test success rate monitoring
- S3 storage costs tracking

## GDPR and Data Privacy

### Right to Deletion

```python
# User data deletion endpoint
DELETE /api/v1/subscribers/{id}
Authorization: Bearer {admin_token}

# Hard delete from database and backups
# Compliance: 30-day deletion window
```

### Data Portability

```python
# Export user data in machine-readable format
GET /api/v1/subscribers/{id}/export
Authorization: Bearer {user_token}

# Response: JSON with all user data
```

### Audit Trail

- All data access logged
- Backup access tracked
- Restoration operations recorded
- GDPR compliance reports generated

## Security

### Backup Encryption

- Database backups: AES-256 encryption at rest
- S3 server-side encryption (SSE-S3)
- WAL log encryption in transit (TLS)
- Redis RDB encryption with custom key

### Access Control

- Backup buckets: Read-only for application, admin write access
- Database restore: Requires admin credentials
- Multi-factor authentication for production access
- Audit logs for all backup/restore operations

## Documentation

### Runbook Location

- Located in: `docs/modules/publishing-tools/runbooks/`
- **database-restore.md**: Step-by-step database recovery
- **redis-restore.md**: Redis recovery procedures
- **disaster-recovery.md**: Full DR playbook
- **backup-verification.md**: Monthly restore test procedures

### Contact Information

- **Primary On-Call**: PagerDuty escalation
- **Database Admin**: DBA team email/Slack
- **Infrastructure**: DevOps team email/Slack
- **Security**: Security team for encryption issues

## Implementation Checklist

- [ ] Configure automated PostgreSQL backups
- [ ] Set up WAL archiving to S3
- [ ] Configure Redis RDB and AOF
- [ ] Create S3 backup bucket with lifecycle policies
- [ ] Set up multi-region replication
- [ ] Configure Redis Sentinel for failover
- [ ] Implement data export endpoints
- [ ] Create restoration runbooks
- [ ] Schedule monthly restore tests
- [ ] Set up backup monitoring and alerting
- [ ] Document GDPR compliance procedures
- [ ] Train team on recovery procedures

## Resources

- PostgreSQL Backup: https://www.postgresql.org/docs/current/backup.html
- Redis Persistence: https://redis.io/topics/persistence
- AWS S3 Lifecycle: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
- GDPR Compliance: https://gdpr.eu/

