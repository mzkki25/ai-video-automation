# Template & Separate Pages Feature

## New Features

### 1. Product Information Templates
Save and reuse product information for faster video creation.

**Features:**
- Save template with custom name
- Store: Nama Produk, Target Audiens, USP, CTA
- Load template with one click
- Delete unused templates
- User-specific templates (isolated per user)

**API Endpoints:**
- `GET /api/templates` - List all templates
- `POST /api/templates` - Create new template
- `GET /api/templates/{id}` - Get template detail
- `DELETE /api/templates/{id}` - Delete template

### 2. Separate Pages for Video Types

**Two dedicated pages:**

#### A. Create Video - With Product (`/static/create-product.html`)
- For product videos requiring product image
- Uses `/api/video/start-workflow` endpoint
- Fields: Nama Produk, Target Audiens, USP, CTA, Product Image, Avatar

#### B. Create Video - Without Product (`/static/create-non-product.html`)
- For informational/tips videos without product
- Uses `/api/video/start-workflow-non-product` endpoint
- Fields: Topic/Title, Target Audience, Key Points, CTA, Avatar

### 3. Shared JavaScript
- Single `video-creator.js` file for both pages
- Configurable via page-level variables
- Handles: templates, script generation, workflow monitoring

## Usage Flow

### Using Templates

1. **Save Template:**
   - Fill product information form
   - Click "💾 Save as Template"
   - Enter template name
   - Template saved to database

2. **Use Template:**
   - Click "📋 Use Template"
   - Select from saved templates
   - Form auto-filled with template data
   - Modify as needed

3. **Delete Template:**
   - Open template modal
   - Click "Delete" on unwanted template

### Creating Videos

**Option 1: With Product**
1. Go to Dashboard
2. Click "+" button → "📦 With Product"
3. Fill form or use template
4. Upload product image
5. Generate script → Create video

**Option 2: Without Product**
1. Go to Dashboard
2. Click "+" button → "💡 Without Product"
3. Fill form or use template
4. Generate script → Create video

## Database Schema

### Templates Table
```sql
CREATE TABLE templates (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR NOT NULL,
    nama_produk VARCHAR NOT NULL,
    target_audiens VARCHAR NOT NULL,
    usp TEXT NOT NULL,
    cta VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## File Structure

```
static/
├── create-product.html      # Video with product page
├── create-non-product.html  # Video without product page
├── dashboard.html           # Updated with dropdown menu
├── index.html              # Updated with navigation
└── js/
    └── video-creator.js    # Shared JavaScript logic

app/
├── models/
│   └── Template.py         # Template model
├── schemas/
│   └── TemplateSchemas.py  # Template schemas
└── api/
    └── template_routes.py  # Template CRUD endpoints
```

## Benefits

1. **Faster Workflow**: Reuse product info without retyping
2. **Better Organization**: Separate pages for different video types
3. **Code Reusability**: Shared JS reduces duplication
4. **User Experience**: Clear navigation and intuitive UI
5. **Flexibility**: Easy to add more template fields later

## Notes

- Templates are user-specific (isolated by user_id)
- Template name is required for saving
- Both pages share same script editor and monitoring
- Dropdown menu on dashboard for easy access
- Templates work for both product and non-product videos
