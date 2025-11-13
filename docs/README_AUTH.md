# Authentication & Video History Features

## New Features Added

### 1. User Authentication
- **Signup**: Create new user account
- **Login**: Authenticate and get JWT token
- **Protected Routes**: All video operations require authentication

### 2. Video History
- **List Videos**: View all videos created by user
- **Search**: Search videos by product name
- **Filter**: Filter by status (processing, completed, error)
- **Pagination**: Support for large video lists

### 3. Bulk Operations
- **Select Multiple**: Checkbox selection for multiple videos
- **Bulk Delete**: Delete multiple videos at once
- **Individual Delete**: Delete single video

### 4. Database
- **PostgreSQL**: Using external PostgreSQL database
- **Tables**: 
  - `users`: Store user accounts
  - `videos`: Store video history with workflow tracking

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Run Application
```bash
python run.py
```

### 4. Access Application
- **Auth Page**: http://localhost:8000/static/auth.html
- **Dashboard**: http://localhost:8000/static/dashboard.html (after login)
- **Create Video**: http://localhost:8000/static/index.html (after login)

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - Login and get token

### Video History
- `GET /api/history/videos` - List all videos (with search & filter)
- `GET /api/history/videos/{id}` - Get video detail
- `DELETE /api/history/videos/{id}` - Delete single video
- `POST /api/history/videos/bulk-delete` - Delete multiple videos

### Video Creation (Protected)
- `POST /api/video/start-workflow` - Start video workflow (requires auth)
- `POST /api/video/start-workflow-non-product` - Start non-product workflow (requires auth)

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Videos Table
```sql
CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    workflow_id VARCHAR UNIQUE NOT NULL,
    nama_produk VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'processing',
    video_url VARCHAR,
    thumbnail_url VARCHAR,
    script_data TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

## Frontend Pages

### 1. auth.html
- Login/Signup tabs
- Form validation
- Token storage in localStorage

### 2. dashboard.html
- Video grid with thumbnails
- Search bar
- Status filter dropdown
- Bulk delete functionality
- Floating "Create" button

### 3. index.html (Updated)
- Auth check on page load
- Logout button
- Dashboard navigation
- Token included in API requests

## Security Features

- **Password Hashing**: Using bcrypt
- **JWT Tokens**: 7-day expiration
- **Protected Routes**: Bearer token authentication
- **User Isolation**: Users can only see/delete their own videos

## Usage Flow

1. **Sign Up** → Create account at `/static/auth.html`
2. **Login** → Get JWT token, redirected to dashboard
3. **Dashboard** → View all videos, search, filter, delete
4. **Create Video** → Click "+" button, redirected to creation page
5. **Video Creation** → Fill form, generate script, create video
6. **Auto Save** → Video automatically saved to database
7. **View History** → Return to dashboard to see all videos

## Notes

- Videos are automatically saved when workflow starts
- Video status updates when workflow completes
- Thumbnails can be added later (currently placeholder)
- Search is case-insensitive
- Bulk operations support unlimited selections
