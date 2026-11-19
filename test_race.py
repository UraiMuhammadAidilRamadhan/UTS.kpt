import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def main():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as client:
        # Pastikan produk ID 1 memiliki stok 1 sebelum pengujian.
        # Ubah stok melalui PUT /resource/1 di Swagger, atau reset database dan seed.
        requests = [
            client.post("/transactions", json={"product_id": 1, "qty": 1}),
            client.post("/transactions", json={"product_id": 1, "qty": 1}),
        ]
        results = await asyncio.gather(*requests)
        for index, response in enumerate(results, start=1):
            try:
                body = response.json()
            except ValueError:
                body = response.text
            print(f"Respon Request {index}: {response.status_code} {body}")

        product = await client.get("/resource/1")
        print("Produk setelah pengujian:", product.status_code, product.json())

if __name__ == "__main__":
    asyncio.run(main())
