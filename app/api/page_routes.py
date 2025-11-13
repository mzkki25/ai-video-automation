from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="templates")

@router.get("/auth", response_class=HTMLResponse)
async def auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/create-product", response_class=HTMLResponse)
async def create_product_page(request: Request):
    return templates.TemplateResponse("create-product.html", {"request": request})

@router.get("/create-non-product", response_class=HTMLResponse)
async def create_non_product_page(request: Request):
    return templates.TemplateResponse("create-non-product.html", {"request": request})

@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
