from locust import HttpUser, task









class AdminUser(HttpUser):

    def on_start(self):
        response = self.client.post("/api/auth/jwt/admin-login" ,
                         json= {"phone_number":"09123456789",
                                "password":"@hamid14520"})
        print(response.content)


    @task
    def get_user(self):
        self.client.get('/api/user/user')
