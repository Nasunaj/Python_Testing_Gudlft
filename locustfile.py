from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    """Simulates a user navigating the Güdlft application."""
    # Wait between 1 and 3 seconds between each request.
    wait_time = between(1, 3)

    @task
    def view_points(self):
        """Go to the points table page."""
        self.client.get("/points")

    @task
    def purchase_places(self):
        """Simulates a place reservation."""
        self.client.post(
            "/purchasePlaces",
            data={
                "club": "Test Club",
                "competition": "Test Competition",
                "places": 1
            }
        )

    @task
    def view_welcome(self):
        """Go to the home page."""
        self.client.get("/")