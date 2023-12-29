from locust import HttpUser, between

# from concurrency.credit.models import CreditRequest


class IncreaseCreditRequest(HttpUser):
    between(1, 5)

    def on_start(self):
        response = self.client.post("/api/auth/jwt/seller-login/",
                                    json={"phone_number": "09101111111",
                                          "password": "@hamid14520"})
        self.token = self.token = response.json()['token']['access']
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def create_increase_request(self):
        self.client.post("api/credit/submit-request/",
                         json={
                             "amount": "100000"
                         },
                         headers=self.headers)


class ChangeRequestStatus(HttpUser):

    def on_start(self):
        response = self.client.post("/api/auth/jwt/admin-login/",
                                    json={"phone_number": "09123456789",
                                          "password": "@hamid14520"})
        self.token = self.token = response.json()['token']['access']
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def change_credit_request_status(self):
        request = self.client.put(f"/api/credit/change-request-status/",
                                  json={
                                      'status': True
                                  },
                                  headers=self.headers)
