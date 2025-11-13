# Frontend Templates - Video Creator

## Overview
Production-ready HTML templates for FastAPI video automation application. All templates are self-contained with embedded CSS and JavaScript.

## Files
- `auth.html` - Login & signup page with tabbed interface
- `dashboard.html` - Video history dashboard with search, filter, and bulk actions
- `create-product.html` - Multi-step video creation with product
- `create-non-product.html` - Simplified video creation without product
- `index.html` - Legacy navigation page

## FastAPI Integration

### 1. Setup Jinja2 Templates

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Optional: serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### 2. Route Examples

```python
@app.get("/auth", response_class=HTMLResponse)
async def auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    # Optional: pass server-side context
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "username": "John Doe"  # Optional, JS uses localStorage
    })

@app.get("/create-product", response_class=HTMLResponse)
async def create_product_page(request: Request):
    return templates.TemplateResponse("create-product.html", {"request": request})

@app.get("/create-non-product", response_class=HTMLResponse)
async def create_non_product_page(request: Request):
    return templates.TemplateResponse("create-non-product.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

### 3. Required API Endpoints

#### Authentication
```python
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    email: str
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str
    username: str

@app.post("/api/auth/login", response_model=AuthResponse)
async def login(data: LoginRequest):
    # Validate credentials
    # Generate JWT token
    return {"token": "jwt_token_here", "username": data.username}

@app.post("/api/auth/signup", response_model=AuthResponse)
async def signup(data: SignupRequest):
    # Create user
    # Generate JWT token
    return {"token": "jwt_token_here", "username": data.username}
```

#### Videos
```python
from typing import List, Optional

class VideoResponse(BaseModel):
    id: str
    title: str
    thumbnail: Optional[str]
    status: str  # processing, completed, error
    created_at: str
    workflow_id: str
    product_name: Optional[str]
    video_url: Optional[str]

@app.get("/api/videos", response_model=List[VideoResponse])
async def get_videos(
    q: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    # Query videos with filters
    return videos

class DeleteRequest(BaseModel):
    ids: List[str]

@app.delete("/api/videos")
async def delete_videos(
    data: DeleteRequest,
    current_user: User = Depends(get_current_user)
):
    # Delete videos by IDs
    return {"deleted": len(data.ids)}
```

#### Templates
```python
class TemplateResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    data: dict

@app.get("/api/templates", response_model=List[TemplateResponse])
async def get_templates(current_user: User = Depends(get_current_user)):
    return templates

@app.post("/api/templates")
async def create_template(
    data: dict,
    current_user: User = Depends(get_current_user)
):
    # Save template
    return {"id": "template_id"}

@app.get("/api/templates/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: str, current_user: User = Depends(get_current_user)):
    return template

@app.delete("/api/templates/{template_id}")
async def delete_template(template_id: str, current_user: User = Depends(get_current_user)):
    return {"deleted": True}
```

#### File Upload
```python
@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Save file
    # Return URL
    return {"url": f"/uploads/{file.filename}"}
```

## API Endpoints Summary

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration

### Videos
- `GET /api/videos?q=&status=` - List videos with filters
- `DELETE /api/videos` - Bulk delete videos
- `GET /api/video/workflow-status/{workflow_id}` - Get workflow status

### Video Creation (Already implemented in your code)
- `POST /api/video/generate-script` - Generate video script
- `POST /api/video/start-workflow` - Start video creation with product
- `POST /api/video/start-workflow-non-product` - Start video creation without product

### Templates
- `GET /api/templates` - List user templates
- `POST /api/templates` - Save new template
- `GET /api/templates/{id}` - Get template by ID
- `DELETE /api/templates/{id}` - Delete template

### Uploads
- `POST /api/upload` - Upload image file

## Security Notes

1. **JWT Authentication**: All API endpoints (except auth) require Bearer token in Authorization header
2. **CORS**: Configure CORS for frontend-backend communication
3. **Rate Limiting**: Implement rate limiting on auth endpoints
4. **File Validation**: Validate file types and sizes server-side
5. **HTTPS**: Use HTTPS in production

## Client-Side Features

### Authentication
- Token stored in localStorage
- Auto-redirect to /auth if no token
- Auto-redirect to /dashboard if already logged in

### Dashboard
- Real-time search with 300ms debounce
- Status filtering
- Bulk selection and delete
- Polling for processing videos (10s interval)
- Video player modal

### Create Video
- Multi-step workflow (4 steps)
- File upload with preview
- Script generation
- Progress polling (5s interval with exponential backoff)
- Template save/load

## Customization

### Colors
Edit CSS variables in `:root`:
```css
:root {
    --color-primary: #6366f1;
    --bg: #f8f9fa;
    --card-bg: #ffffff;
    --success: #198754;
    --danger: #dc3545;
    /* ... */
}
```

### API Endpoints
Update `data-api-*` attributes in HTML:
```html
<form data-api-login="/api/auth/login">
```

### Polling Intervals
Edit JavaScript constants:
```javascript
// Dashboard polling: 10 seconds
setInterval(pollFunction, 10000);

// Workflow polling: 5 seconds
setInterval(pollWorkflow, 5000);
```

## Browser Support
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Accessibility
- ARIA labels and roles
- Keyboard navigation
- Screen reader friendly
- Focus management in modals

## Testing Checklist

### auth.html
- [ ] Tab switching works
- [ ] Password toggle works
- [ ] Form validation
- [ ] Login redirects to dashboard
- [ ] Signup creates account

### dashboard.html
- [ ] Videos load and display
- [ ] Search filters results
- [ ] Status filter works
- [ ] Bulk delete works
- [ ] Video player opens
- [ ] Polling updates status

### create-product.html
- [ ] File uploads work
- [ ] Script generation works
- [ ] Multi-step navigation
- [ ] Progress polling works
- [ ] Video result displays
- [ ] Template save/load works

### create-non-product.html
- [ ] Form submits
- [ ] Redirects to dashboard
- [ ] Avatar upload works

## Notes
- All templates work without JavaScript for core functionality (progressive enhancement)
- Forms can submit directly to backend if JS disabled
- Templates are mobile-responsive
- No external dependencies except Google Fonts
