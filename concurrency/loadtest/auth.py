from locust import HttpUser, task, between


class AdminUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.post("/api/auth/jwt/admin-login/",
                                    json={"phone_number": "09123456789",
                                          "password": "@hamid14520"})
        self.token = self.token = response.json()['token']['access']
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task
    def get_user(self):
        self.client.get('/api/user/user/', headers=self.headers)



