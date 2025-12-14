# How to View CloudSQL Tables

## Option 1: Using gcloud SQL Connect (Easiest)

```bash
~/Downloads/google-cloud-sdk/bin/gcloud sql connect matcha-db --user=root
```

When prompted, enter password: `cloudettes`

Then run SQL commands:
```sql
USE matcha_db;
SHOW TABLES;
DESCRIBE users;
DESCRIBE matcha_sessions;
SELECT * FROM users;
SELECT * FROM matcha_sessions;
```

## Option 2: Using Cloud Console (Web Interface)

1. Go to: https://console.cloud.google.com/sql/instances
2. Click on your instance: `matcha-db`
3. Click "Databases" tab to see databases
4. Click "Connect using Cloud Shell" or use the built-in SQL editor

## Option 3: Using Cloud SQL Proxy (For MySQL Client)

1. Download Cloud SQL Proxy:
```bash
curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.8.0/cloud-sql-proxy.darwin.arm64
chmod +x cloud-sql-proxy
```

2. Run the proxy:
```bash
./cloud-sql-proxy microservice-1-479117:us-central1:matcha-db
```

3. In another terminal, connect with MySQL client:
```bash
mysql -h 127.0.0.1 -u root -p matcha_db
# Password: cloudettes
```

4. Then run:
```sql
SHOW TABLES;
DESCRIBE users;
SELECT * FROM users;
```

## Option 4: Quick Query via gcloud

```bash
# List databases
~/Downloads/google-cloud-sdk/bin/gcloud sql databases list --instance=matcha-db

# Execute SQL query (if supported)
# Note: gcloud doesn't have direct SQL execution, use one of the above methods
```

## Expected Tables

After your app runs, you should see:
- `users` - User profiles
- `matcha_sessions` - Matcha drinking sessions

## Check if Tables Exist

Connect and run:
```sql
USE matcha_db;
SHOW TABLES;
```

If tables don't exist yet, they'll be created automatically when your app first starts and calls `init_db()`.







