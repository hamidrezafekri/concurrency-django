from random import randint

from locust import HttpUser, between, task


class SellAndBuyCheck(HttpUser):
    wait_time = between(1, 1)

    def on_start(self):
        response = self.client.post("/api/auth/jwt/seller-login/",
                                    json={"phone_number": "09101111111",
                                          "password": "@hamid14520"})
        self.token = self.token = response.json()['token']['access']
        self.seller1_headers = {"Authorization": f"Bearer {self.token}"}

        response = self.client.post("/api/auth/jwt/seller-login/",
                                    json={"phone_number": "09103333333",
                                          "password": "@hamid14520"})
        self.token = self.token = response.json()['token']['access']
        self.seller2_headers = {"Authorization": f"Bearer {self.token}"}

        response = self.client.post("/api/auth/jwt/cutomer-login/",
                                    json={"phone_number": "09102222222",
                                          "password": "@hamid14520"})
        self.token = self.token = response.json()['token']['access']
        self.customer_headers = {"Authorization": f"Bearer {self.token}"}

        response = self.client.post("/api/auth/jwt/admin-login/",
                                    json={"phone_number": "09123456789",
                                          "password": "@hamid14520"})
        self.token = self.token = response.json()['token']['access']
        self.admin_headers = {"Authorization": f"Bearer {self.token}"}

        response = self.client.post("/api/credit/submit-request/",
                                    json={
                                        "amount": "100000"
                                    },
                                    headers=self.seller1_headers,
                                    name="request_increase_credit")
        self.request_id = response.json()['id']
        self.client.put(f"/api/credit/change-request-status/{self.request_id}/",
                        json={
                            'status': True
                        },
                        headers=self.admin_headers, name="increase_credit-seller1")

    @task(1)
    def increase_credit_seller1(self):

    @task(2)
    def increase_credit_seller2(self):
        response = self.client.post("/api/credit/submit-request/",
                                    json={
                                        "amount": "80000"
                                    },
                                    headers=self.seller2_headers,
                                    name="request_increase_credit")
        self.request_id = response.json()['id']
        self.client.put(f"/api/credit/change-request-status/{self.request_id}/",
                        json={
                            'status': True
                        },
                        headers=self.admin_headers, name="increase_credit-seller2")

    @task(4)
    def buy_product(self):
        product_id = randint(1, 3)
        self.client.post("/api/credit/buy-product/",
                         json={"product": 1},
                         headers=self.customer_headers,
                         name='buy-product-seller1')

