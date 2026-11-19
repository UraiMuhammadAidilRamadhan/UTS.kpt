import asyncio
from database import init_db, fetch_one, execute

SEED_PRODUCTS = [
    ("Beras 5 Kg", "Sembako", 75000, 20, "Beras kemasan 5 kilogram"),
    ("Minyak Goreng 1 L", "Sembako", 18000, 30, "Minyak goreng kemasan 1 liter"),
    ("Gula Pasir 1 Kg", "Sembako", 17000, 25, "Gula pasir putih"),
    ("Kopi Sachet", "Minuman", 2000, 100, "Kopi sachet"),
    ("Mi Instan", "Makanan", 3500, 80, "Mi instan berbagai rasa"),
    ("Teh Celup", "Minuman", 8000, 40, "Teh celup satu kotak"),
    ("Susu UHT", "Minuman", 6500, 35, "Susu UHT 250 ml"),
    ("Air Mineral", "Minuman", 4000, 60, "Air mineral 600 ml"),
    ("Sabun Mandi", "Kebutuhan Rumah", 5000, 45, "Sabun mandi batang"),
    ("Detergen 800 g", "Kebutuhan Rumah", 16000, 22, "Detergen kemasan 800 gram"),
]

async def main():
    await init_db()
    for item in SEED_PRODUCTS:
        existing = await fetch_one("SELECT id FROM products WHERE nama=?", (item[0],))
        if not existing:
            await execute(
                "INSERT INTO products (nama, kategori, harga, stok, deskripsi) VALUES (?, ?, ?, ?, ?)",
                item,
            )
    print("Seed selesai. Minimal 10 produk tersedia.")

if __name__ == "__main__":
    asyncio.run(main())
