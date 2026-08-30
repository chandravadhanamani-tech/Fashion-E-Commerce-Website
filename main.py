import os
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, get_db
from app import models, auth
from app.routers import (
    auth as auth_router,
    products as products_router,
    categories as categories_router,
    brands as brands_router,
    cart as cart_router,
    orders as orders_router,
    wishlist as wishlist_router,
    recommendations as recommendations_router
)

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Directories for static and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Include API Routers under /api/v1
api_v1 = settings.API_V1_STR
app.include_router(auth_router.router, prefix=api_v1)
app.include_router(products_router.router, prefix=api_v1)
app.include_router(categories_router.router, prefix=api_v1)
app.include_router(brands_router.router, prefix=api_v1)
app.include_router(cart_router.router, prefix=api_v1)
app.include_router(orders_router.router, prefix=api_v1)
app.include_router(wishlist_router.router, prefix=api_v1)
app.include_router(recommendations_router.router, prefix=api_v1)

# Frontend Page Routes
@app.get("/", response_class=HTMLResponse)
def page_home(request: Request, db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    brands = db.query(models.Brand).all()
    featured_products = db.query(models.Product).filter(models.Product.is_active == True).limit(8).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "categories": categories,
            "brands": brands,
            "featured_products": featured_products
        }
    )

@app.get("/products", response_class=HTMLResponse)
def page_products(request: Request):
    return templates.TemplateResponse(request=request, name="products.html", context={})

@app.get("/products/{slug}", response_class=HTMLResponse)
def page_product_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.slug == slug).first()
    return templates.TemplateResponse(
        request=request,
        name="product_detail.html",
        context={
            "product_slug": slug,
            "product": product
        }
    )

@app.get("/cart", response_class=HTMLResponse)
def page_cart(request: Request):
    return templates.TemplateResponse(request=request, name="cart.html", context={})

@app.get("/checkout", response_class=HTMLResponse)
def page_checkout(request: Request):
    return templates.TemplateResponse(request=request, name="checkout.html", context={})

@app.get("/profile", response_class=HTMLResponse)
def page_profile(request: Request):
    return templates.TemplateResponse(request=request, name="profile.html", context={})

@app.get("/auth", response_class=HTMLResponse)
def page_auth(request: Request):
    return templates.TemplateResponse(request=request, name="auth.html", context={})

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
