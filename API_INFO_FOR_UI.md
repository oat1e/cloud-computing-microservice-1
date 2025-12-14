# API Information for UI Team

## ✅ Microservice 1 is Deployed!

**Base URL:** `https://matcha-api-ktr6lb33ta-uc.a.run.app`

**Status:** ✅ Live and accessible

## API Endpoints

### Health Check
```
GET https://matcha-api-ktr6lb33ta-uc.a.run.app/health
```

### User Endpoints

**List all users:**
```
GET https://matcha-api-ktr6lb33ta-uc.a.run.app/users
```

**Get specific user by ID:**
```
GET https://matcha-api-ktr6lb33ta-uc.a.run.app/users/{user_id}
```

**Create a new user:**
```
POST https://matcha-api-ktr6lb33ta-uc.a.run.app/users
Content-Type: application/json

{
  "username": "test_user",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User"
}
```

**Update user:**
```
PUT https://matcha-api-ktr6lb33ta-uc.a.run.app/users/{user_id}
Content-Type: application/json

{
  "first_name": "Updated",
  "last_name": "Name"
}
```

**Delete user:**
```
DELETE https://matcha-api-ktr6lb33ta-uc.a.run.app/users/{user_id}
```

### Matcha Session Endpoints

**List all sessions:**
```
GET https://matcha-api-ktr6lb33ta-uc.a.run.app/matcha-sessions
```

**Get specific session:**
```
GET https://matcha-api-ktr6lb33ta-uc.a.run.app/matcha-sessions/{session_id}
```

**Create session:**
```
POST https://matcha-api-ktr6lb33ta-uc.a.run.app/matcha-sessions
Content-Type: application/json

{
  "session_date": "2025-01-23",
  "location": "Home",
  "matcha_type": "Ceremonial Grade",
  "rating": 4.5,
  "notes": "Great matcha!"
}
```

## Interactive API Documentation

**Swagger UI:** https://matcha-api-ktr6lb33ta-uc.a.run.app/docs

This provides an interactive interface to test all endpoints!

## Current Database Status

The database is currently **empty** (no users yet). 

To create a test user for UI development:

```bash
curl -X POST https://matcha-api-ktr6lb33ta-uc.a.run.app/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo_user",
    "email": "demo@example.com",
    "first_name": "Demo",
    "last_name": "User",
    "favorite_matcha_place": "Cha Cha Matcha"
  }'
```

This will return a user object with an `id` field (UUID) that you can use.

## User Object Structure

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "demo_user",
  "email": "demo@example.com",
  "first_name": "Demo",
  "last_name": "User",
  "phone": null,
  "favorite_matcha_powder": null,
  "favorite_matcha_place": "Cha Cha Matcha",
  "matcha_budget": null,
  "join_date": null,
  "matcha_sessions": [],
  "created_at": "2025-01-23T18:30:00Z",
  "updated_at": "2025-01-23T18:30:00Z"
}
```

## CORS

The API should accept requests from any origin. If you encounter CORS issues, let me know and we can add specific CORS configuration.

## Testing

You can test the API using:
- Browser: Visit `/docs` for interactive Swagger UI
- curl: Use the examples above
- Postman/Insomnia: Import the OpenAPI spec from `/openapi.json`
- Your UI: Make HTTP requests to the endpoints

## Need Help?

If you need sample data or encounter any issues, let me know!







