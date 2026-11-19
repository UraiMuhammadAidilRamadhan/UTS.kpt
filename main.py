from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from routes.resource import router as resource_router
from routes.transaction import router as transaction_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Sistem Kasir dan Manajemen Stok UMKM",
    description="REST API untuk pengelolaan produk, stok, dan transaksi UMKM.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(resource_router)
app.include_router(transaction_router)

@app.get("/", tags=["Informasi"])
async def root():
    return {"message": "API Kasir UMKM berjalan", "docs": "/docs"}
