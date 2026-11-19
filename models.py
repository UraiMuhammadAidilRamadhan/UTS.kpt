from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class ProductCreate(BaseModel):
    nama: str = Field(min_length=1, max_length=100)
    kategori: str = Field(min_length=1, max_length=50)
    harga: float = Field(ge=0)
    stok: int = Field(ge=0)
    deskripsi: str = Field(default="", max_length=500)

class ProductUpdate(ProductCreate):
    pass

class ProductResponse(ProductCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class TransactionCreate(BaseModel):
    product_id: int = Field(gt=0)
    qty: int = Field(gt=0)

class TransactionResponse(BaseModel):
    id: int
    product_id: int
    nama_produk: str
    qty: int
    harga_satuan: float
    total_harga: float
    status: Literal["pending", "processing", "completed", "failed"]
    created_at: str
