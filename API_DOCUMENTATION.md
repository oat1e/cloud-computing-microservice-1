# Matcha Drinking Tracker API - Complete Endpoint Documentation

## Base URL
```
http://localhost:8000
```
*(Default port is 8000, configurable via FASTAPIPORT environment variable)*

---

## Health Endpoints

### GET /health
**Description:** Health check endpoint

**Query Parameters:**
- `echo` (optional, string): Optional echo string

**Response Body Example:**
```json
{
  "status": 200,
  "status_message": "OK",
  "timestamp": "2025-01-15T10:20:30Z",
  "ip_address": "192.168.1.10",
  "echo": "test",
  "path_echo": null
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### GET /health/{path_echo}
**Description:** Health check endpoint with path parameter

**Path Parameters:**
- `path_echo` (required, string): Required echo in the URL path

**Query Parameters:**
- `echo` (optional, string): Optional echo string

**Response Body Example:**
```json
{
  "status": 200,
  "status_message": "OK",
  "timestamp": "2025-01-15T10:20:30Z",
  "ip_address": "192.168.1.10",
  "echo": "query_test",
  "path_echo": "path_test"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

## User Endpoints

### POST /users
**Description:** Create a new user

**Request Body Example:**
```json
{
  "username": "green_tea_master",
  "email": "green.tea@example.com",
  "first_name": "Hiroshi",
  "last_name": "Yamamoto",
  "phone": "+1-415-555-0101",
  "favorite_matcha_powder": "Premium Grade - Marukyu Koyamaen",
  "favorite_matcha_place": "Tea House NYC",
  "matcha_budget": 200.00,
  "join_date": "2024-02-01",
  "matcha_sessions": [
    {
      "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      "session_date": "2025-01-16",
      "location": "Tea House",
      "matcha_type": "Premium Grade",
      "brand": "Marukyu Koyamaen",
      "rating": 5.0,
      "notes": "Exceptional quality today"
    }
  ]
}
```

**Response Body Example:**
```json
{
  "id": "99999999-9999-4999-8999-999999999999",
  "username": "green_tea_master",
  "email": "green.tea@example.com",
  "first_name": "Hiroshi",
  "last_name": "Yamamoto",
  "phone": "+1-415-555-0101",
  "favorite_matcha_powder": "Premium Grade - Marukyu Koyamaen",
  "favorite_matcha_place": "Tea House NYC",
  "matcha_budget": 200.00,
  "join_date": "2024-02-01",
  "matcha_sessions": [
    {
      "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      "session_date": "2025-01-16",
      "location": "Tea House",
      "matcha_type": "Premium Grade",
      "brand": "Marukyu Koyamaen",
      "rating": 5.0,
      "notes": "Exceptional quality today"
    }
  ],
  "created_at": "2025-01-15T10:20:30Z",
  "updated_at": "2025-01-15T10:20:30Z"
}
```

**Status Codes:**
- `201 Created` - User successfully created
- `422 Unprocessable Entity` - Validation error

**Field Names:**
- `id` (UUID, server-generated)
- `username` (string, required, 3-20 chars, alphanumeric + underscores)
- `email` (string, required, valid email format)
- `first_name` (string, required)
- `last_name` (string, required)
- `phone` (string, optional)
- `favorite_matcha_powder` (string, optional)
- `favorite_matcha_place` (string, optional)
- `matcha_budget` (float, optional, USD)
- `join_date` (date, optional, YYYY-MM-DD format)
- `matcha_sessions` (array of MatchaSessionBase, optional)
- `created_at` (datetime, ISO 8601 format)
- `updated_at` (datetime, ISO 8601 format)

---

### GET /users
**Description:** List all users with optional filtering

**Query Parameters (all optional):**
- `username` (string): Filter by username
- `first_name` (string): Filter by first name
- `last_name` (string): Filter by last name
- `email` (string): Filter by email
- `phone` (string): Filter by phone number
- `favorite_matcha_powder` (string): Filter by favorite matcha powder
- `favorite_matcha_place` (string): Filter by favorite matcha place
- `min_budget` (float): Filter by minimum matcha budget
- `max_budget` (float): Filter by maximum matcha budget
- `join_date` (string): Filter by join date (YYYY-MM-DD)

**Example Request:**
```
GET /users?username=matcha_lover&min_budget=100.00
```

**Response Body Example:**
```json
[
  {
    "id": "99999999-9999-4999-8999-999999999999",
    "username": "matcha_lover",
    "email": "matcha@example.com",
    "first_name": "Sakura",
    "last_name": "Tanaka",
    "phone": "+1-212-555-0199",
    "favorite_matcha_powder": "Ceremonial Grade - Ippodo",
    "favorite_matcha_place": "Cha Cha Matcha NYC",
    "matcha_budget": 150.00,
    "join_date": "2024-01-15",
    "matcha_sessions": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "session_date": "2025-01-15",
        "location": "Home",
        "matcha_type": "Ceremonial Grade",
        "brand": "Ippodo",
        "rating": 4.5,
        "notes": "Perfect morning ritual"
      }
    ],
    "created_at": "2025-01-15T10:20:30Z",
    "updated_at": "2025-01-16T12:00:00Z"
  }
]
```

**Status Codes:**
- `200 OK` - Success

---

### GET /users/{user_id}
**Description:** Get a specific user by ID

**Path Parameters:**
- `user_id` (required, UUID): User ID

**Example Request:**
```
GET /users/99999999-9999-4999-8999-999999999999
```

**Response Body Example:**
```json
{
  "id": "99999999-9999-4999-8999-999999999999",
  "username": "matcha_lover",
  "email": "matcha@example.com",
  "first_name": "Sakura",
  "last_name": "Tanaka",
  "phone": "+1-212-555-0199",
  "favorite_matcha_powder": "Ceremonial Grade - Ippodo",
  "favorite_matcha_place": "Cha Cha Matcha NYC",
  "matcha_budget": 150.00,
  "join_date": "2024-01-15",
  "matcha_sessions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "session_date": "2025-01-15",
      "location": "Home",
      "matcha_type": "Ceremonial Grade",
      "brand": "Ippodo",
      "rating": 4.5,
      "notes": "Perfect morning ritual"
    }
  ],
  "created_at": "2025-01-15T10:20:30Z",
  "updated_at": "2025-01-16T12:00:00Z"
}
```

**Status Codes:**
- `200 OK` - User found
- `404 Not Found` - User not found

---

### PUT /users/{user_id}
**Description:** Update a user (partial update - only include fields to change)

**Path Parameters:**
- `user_id` (required, UUID): User ID

**Request Body Example (partial update):**
```json
{
  "first_name": "Emiko",
  "last_name": "Sato",
  "favorite_matcha_place": "New Favorite Place"
}
```

**Response Body Example:**
```json
{
  "id": "99999999-9999-4999-8999-999999999999",
  "username": "matcha_lover",
  "email": "matcha@example.com",
  "first_name": "Emiko",
  "last_name": "Sato",
  "phone": "+1-212-555-0199",
  "favorite_matcha_powder": "Ceremonial Grade - Ippodo",
  "favorite_matcha_place": "New Favorite Place",
  "matcha_budget": 150.00,
  "join_date": "2024-01-15",
  "matcha_sessions": [],
  "created_at": "2025-01-15T10:20:30Z",
  "updated_at": "2025-01-16T12:00:00Z"
}
```

**Status Codes:**
- `200 OK` - User updated successfully
- `404 Not Found` - User not found
- `422 Unprocessable Entity` - Validation error

**Note:** All fields in request body are optional. Only provided fields will be updated.

---

### DELETE /users/{user_id}
**Description:** Delete a user

**Path Parameters:**
- `user_id` (required, UUID): User ID

**Example Request:**
```
DELETE /users/99999999-9999-4999-8999-999999999999
```

**Response Body:**
- No content (empty body)

**Status Codes:**
- `204 No Content` - User deleted successfully
- `404 Not Found` - User not found

---

## Matcha Session Endpoints

### POST /matcha-sessions
**Description:** Create a new matcha drinking session

**Request Body Example:**
```json
{
  "id": "11111111-1111-4111-8111-111111111111",
  "session_date": "2025-01-16",
  "location": "Cha Cha Matcha",
  "matcha_type": "Premium Grade",
  "brand": "Marukyu Koyamaen",
  "rating": 4.8,
  "notes": "Excellent texture and aroma"
}
```

**Response Body Example:**
```json
{
  "id": "11111111-1111-4111-8111-111111111111",
  "session_date": "2025-01-16",
  "location": "Cha Cha Matcha",
  "matcha_type": "Premium Grade",
  "brand": "Marukyu Koyamaen",
  "rating": 4.8,
  "notes": "Excellent texture and aroma",
  "created_at": "2025-01-15T10:20:30Z",
  "updated_at": "2025-01-15T10:20:30Z"
}
```

**Status Codes:**
- `201 Created` - Session successfully created
- `400 Bad Request` - Session with this ID already exists
- `422 Unprocessable Entity` - Validation error

**Field Names:**
- `id` (UUID, required, can be provided or auto-generated)
- `session_date` (date, required, YYYY-MM-DD format)
- `location` (string, required)
- `matcha_type` (string, required, must be one of: "Ceremonial Grade", "Premium Grade", "Culinary Grade", "Latte Grade")
- `brand` (string, optional)
- `rating` (float, optional, 0.0 to 5.0)
- `notes` (string, optional)
- `created_at` (datetime, ISO 8601 format, server-generated)
- `updated_at` (datetime, ISO 8601 format, server-generated)

---

### GET /matcha-sessions
**Description:** List all matcha sessions with optional filtering

**Query Parameters (all optional):**
- `session_date` (string): Filter by session date (YYYY-MM-DD)
- `location` (string): Filter by location
- `matcha_type` (string): Filter by matcha type
- `brand` (string): Filter by brand
- `min_rating` (float): Filter by minimum rating (0.0-5.0)
- `max_rating` (float): Filter by maximum rating (0.0-5.0)

**Example Request:**
```
GET /matcha-sessions?matcha_type=Ceremonial Grade&min_rating=4.0
```

**Response Body Example:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "session_date": "2025-01-15",
    "location": "Home",
    "matcha_type": "Ceremonial Grade",
    "brand": "Ippodo",
    "rating": 4.5,
    "notes": "Perfect morning ritual with great umami flavor",
    "created_at": "2025-01-15T10:20:30Z",
    "updated_at": "2025-01-16T12:00:00Z"
  }
]
```

**Status Codes:**
- `200 OK` - Success

---

### GET /matcha-sessions/{session_id}
**Description:** Get a specific matcha session by ID

**Path Parameters:**
- `session_id` (required, UUID): Matcha session ID

**Example Request:**
```
GET /matcha-sessions/550e8400-e29b-41d4-a716-446655440000
```

**Response Body Example:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "session_date": "2025-01-15",
  "location": "Home",
  "matcha_type": "Ceremonial Grade",
  "brand": "Ippodo",
  "rating": 4.5,
  "notes": "Perfect morning ritual with great umami flavor",
  "created_at": "2025-01-15T10:20:30Z",
  "updated_at": "2025-01-16T12:00:00Z"
}
```

**Status Codes:**
- `200 OK` - Session found
- `404 Not Found` - Session not found

---

### PUT /matcha-sessions/{session_id}
**Description:** Update a matcha session (partial update - only include fields to change)

**Path Parameters:**
- `session_id` (required, UUID): Matcha session ID

**Request Body Example (partial update):**
```json
{
  "location": "New Location",
  "rating": 4.7,
  "notes": "Updated session notes"
}
```

**Response Body Example:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "session_date": "2025-01-15",
  "location": "New Location",
  "matcha_type": "Ceremonial Grade",
  "brand": "Ippodo",
  "rating": 4.7,
  "notes": "Updated session notes",
  "created_at": "2025-01-15T10:20:30Z",
  "updated_at": "2025-01-16T12:00:00Z"
}
```

**Status Codes:**
- `200 OK` - Session updated successfully
- `404 Not Found` - Session not found
- `422 Unprocessable Entity` - Validation error

**Note:** All fields in request body are optional. Only provided fields will be updated.

---

### DELETE /matcha-sessions/{session_id}
**Description:** Delete a matcha session

**Path Parameters:**
- `session_id` (required, UUID): Matcha session ID

**Example Request:**
```
DELETE /matcha-sessions/550e8400-e29b-41d4-a716-446655440000
```

**Response Body:**
- No content (empty body)

**Status Codes:**
- `204 No Content` - Session deleted successfully
- `404 Not Found` - Session not found

---

## Root Endpoint

### GET /
**Description:** Root endpoint

**Response Body Example:**
```json
{
  "message": "Welcome to the Matcha Drinking Tracker API. See /docs for OpenAPI UI."
}
```

**Status Codes:**
- `200 OK` - Success

---

## Important Notes

### UUID Format
All IDs are UUIDs in the format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
Example: `99999999-9999-4999-8999-999999999999`

### Date Format
All dates use ISO 8601 format: `YYYY-MM-DD`
Example: `2025-01-15`

### DateTime Format
All timestamps use ISO 8601 format with UTC timezone: `YYYY-MM-DDTHH:MM:SSZ`
Example: `2025-01-15T10:20:30Z`

### Matcha Type Values
The `matcha_type` field must be exactly one of:
- `"Ceremonial Grade"`
- `"Premium Grade"`
- `"Culinary Grade"`
- `"Latte Grade"`

### Username Validation
The `username` field must:
- Be 3-20 characters long
- Contain only alphanumeric characters and underscores
- Pattern: `^[a-zA-Z0-9_]{3,20}$`

### Rating Validation
The `rating` field (if provided) must be:
- A float between 0.0 and 5.0 (inclusive)
- Example: `4.5`, `5.0`, `0.0`

### Error Response Format
When an error occurs, the response body will be:
```json
{
  "detail": "Error message here"
}
```

Example for 404:
```json
{
  "detail": "User not found"
}
```

---

## OpenAPI Documentation
Interactive API documentation is available at:
```
http://localhost:8000/docs
```

OpenAPI JSON schema is available at:
```
http://localhost:8000/openapi.json
```

