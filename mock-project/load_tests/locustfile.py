from locust import HttpUser, task, between

class ColorVisionUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def health_check(self):
        self.client.get("/health")
    
    @task(3)
    def submit_plate(self):
        # Simulate submitting a "No Number" answer
        self.client.post("/", data={"skip": "skip"})
    
    @task(1)
    def submit_number(self):
        # Simulate submitting a number answer
        self.client.post("/", data={"answer": "12"})
