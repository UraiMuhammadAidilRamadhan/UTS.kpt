from locust import HttpUser, task, between

class KasirUMKMUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(4)
    def read_products(self):
        self.client.get("/resource", name="GET /resource")

    @task(1)
    def create_transaction(self):
        # Pastikan produk ID 1 tersedia dan stok cukup saat menjalankan skenario write.
        self.client.post(
            "/transactions",
            json={"product_id": 1, "qty": 1},
            name="POST /transactions",
        )
