from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# --- AUTH & USER SCHEMAS ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str
    gender: Optional[str] = "unisex"
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    chest_cm: Optional[float] = None
    waist_cm: Optional[float] = None
    hip_cm: Optional[float] = None
    body_fit_preference: Optional[str] = "regular"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdateProfile(BaseModel):
    full_name: Optional[str] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    chest_cm: Optional[float] = None
    waist_cm: Optional[float] = None
    hip_cm: Optional[float] = None
    body_fit_preference: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    chest_cm: Optional[float] = None
    waist_cm: Optional[float] = None
    hip_cm: Optional[float] = None
    body_fit_preference: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class TokenData(BaseModel):
    email: Optional[str] = None

# --- SIZE RECOMMENDATION SCHEMAS ---
class SizeRecommendationInput(BaseModel):
    gender: str = Field("unisex", description="men, women, or unisex")
    height_cm: float = Field(..., gt=50, lt=250)
    weight_kg: float = Field(..., gt=20, lt=300)
    chest_cm: Optional[float] = None
    waist_cm: Optional[float] = None
    hip_cm: Optional[float] = None
    category_name: Optional[str] = None # Tops, Bottoms, Dresses, Outerwear
    fit_preference: Optional[str] = "regular" # tight, regular, loose

class SizeRecommendationOut(BaseModel):
    recommended_size: str
    confidence_percentage: int
    fit_summary: str
    size_breakdown: dict
    suggested_alternative: Optional[str] = None

# --- CATEGORY & BRAND SCHEMAS ---
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class BrandBase(BaseModel):
    name: str
    slug: str
    logo_url: Optional[str] = None
    description: Optional[str] = None

class BrandCreate(BrandBase):
    pass

class BrandOut(BrandBase):
    id: int

    class Config:
        from_attributes = True

# --- VARIANT & PRODUCT SCHEMAS ---
class VariantBase(BaseModel):
    size: str
    color: str
    sku: str
    stock_quantity: int
    additional_price: float = 0.0

class VariantCreate(VariantBase):
    pass

class VariantOut(VariantBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    price: float
    gender: str = "unisex"
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    category_id: int
    brand_id: int
    variants: List[VariantCreate]

class ProductOut(ProductBase):
    id: int
    category: Optional[CategoryOut] = None
    brand: Optional[BrandOut] = None
    variants: List[VariantOut] = []
    created_at: datetime

    class Config:
        from_attributes = True

class ProductPaginationOut(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    products: List[ProductOut]

# --- CART SCHEMAS ---
class CartItemAdd(BaseModel):
    variant_id: int
    quantity: int = Field(1, ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)

class CartItemOut(BaseModel):
    id: int
    variant_id: int
    quantity: int
    unit_price: float
    total_price: float
    product_name: str
    product_image: Optional[str] = None
    size: str
    color: str
    stock_quantity: int

    class Config:
        from_attributes = True

class CartSummaryOut(BaseModel):
    items: List[CartItemOut]
    subtotal: float
    tax: float
    shipping: float
    grand_total: float
    total_items: int

# --- ORDER SCHEMAS ---
class CheckoutRequest(BaseModel):
    shipping_address: str = Field(..., min_length=10)
    payment_method: str = Field("Credit Card", description="Credit Card, PayPal, Cash on Delivery")

class OrderItemOut(BaseModel):
    id: int
    variant_id: Optional[int]
    quantity: int
    unit_price: float
    total_price: float
    product_name: str
    size: str
    color: str

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    order_number: str
    total_amount: float
    shipping_address: str
    payment_method: str
    status: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True

# --- WISHLIST SCHEMAS ---
class WishlistAdd(BaseModel):
    product_id: int

class WishlistOut(BaseModel):
    id: int
    product: ProductOut
    created_at: datetime

    class Config:
        from_attributes = True
