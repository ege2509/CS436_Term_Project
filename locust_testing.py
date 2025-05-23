from locust import HttpUser, task, between
import json
import random
import logging

class MovieBookingUser(HttpUser):
    # Wait between 3 to 10 seconds between tasks
    wait_time = between(3, 10)
    
    def on_start(self):
        """Initialize user session data when a simulated user starts"""
        # Cache for movie data to avoid repeated queries
        self.movie_cache = {}
        self.available_movies = []
        
        # Load initial movie list
        self.load_movies()
    
    def load_movies(self):
        try:
            response = self.client.get("/api/movies")
            if response.status_code == 200 and response.text:
                self.available_movies = response.json()
                logging.info(f"Loaded {len(self.available_movies)} movies")
            else:
                logging.error(f"Failed to load movies: Status {response.status_code}, Body: {response.text}")
        except Exception as e:
            logging.error(f"Error loading movies: {str(e)}")

    
    def get_random_movie(self):
        """Get a random movie from the available movies"""
        if not self.available_movies:
            self.load_movies()
        
        if self.available_movies:
            return random.choice(self.available_movies)
        else:
            # Fallback if no movies are available
            return {"id": 1, "title": "Sample Movie"}  
    
    def generate_random_showtime(self):
        """Generate a random showtime for testing"""
        hours = random.randint(10, 22)  # Theater hours 10 AM to 10 PM
        minutes = random.choice([0, 15, 30, 45])  # Common minute intervals
        return f"2025-05-21 {hours:02d}:{minutes:02d}:00"
    
    def generate_random_seats(self, count=2):
        """Generate random seat selections with 'S' prefix"""
        # Generate 'count' unique random seats with S prefix
        seats = []
        while len(seats) < count:
            number = random.randint(1, 30)  # Assuming seats are numbered S1 to S100
            seat = f"S{number}"
            if seat not in seats:
                seats.append(seat)
        
        return seats
    
    @task(10)
    def browse_movies(self):
        """Browse the list of movies (most common task)"""
        self.client.get("/api/movies")
    
    @task(5)
    def view_movie_details(self):
        """View details for a specific movie"""
        movie = self.get_random_movie()
        movie_id = movie["id"]
        
        # Check if we've already cached this movie's details
        if movie_id not in self.movie_cache:
            with self.client.get(f"/api/movies/{movie_id}", catch_response=True) as response:
                if response.status_code == 200:
                    self.movie_cache[movie_id] = response.json()
                else:
                    logging.error(f"Failed to get movie {movie_id}: {response.status_code}")
    
    @task(3)
    def check_seat_availability(self):
        """Check which seats are booked for a specific movie and showtime"""
        movie = self.get_random_movie()
        showtime = self.generate_random_showtime()
        
        self.client.get(f"/api/bookings/booked-seats?movieId={movie['id']}&showtime={showtime}")
    
    @task(2)
    def book_movie_tickets(self):
        """Create a new booking (least frequent but most complex task)"""
        movie = self.get_random_movie()
        showtime = self.generate_random_showtime()
        
        # First check which seats are already booked
        with self.client.get(f"/api/bookings/booked-seats?movieId={movie['id']}&showtime={showtime}", catch_response=True) as response:
            if response.status_code != 200:
                logging.error(f"Failed to check seat availability: {response.status_code}")
                return
                
            booked_seats = response.json()
            
        # Choose random seats that aren't already booked
        all_possible_seats = [f"S{num}" for num in range(1, 30)]  # S1 to S30
        available_seats = [seat for seat in all_possible_seats if seat not in booked_seats]
        
        if len(available_seats) < 2:
            logging.warning("Not enough available seats to make a booking")
            return
            
        # Select 1-3 random seats
        num_seats = random.randint(1, min(3, len(available_seats)))
        selected_seats = random.sample(available_seats, num_seats)
        
        # Create the booking
        booking_data = {
            "movieId": movie["id"],
            "showtime": showtime,
            "seats": selected_seats
        }
        
        with self.client.post("/api/bookings", json=booking_data, catch_response=True) as response:
            if response.status_code == 201:
                # If booking is successful, sometimes check the booking details
                booking_response = response.json()
                if "bookingId" in booking_response and random.random() < 0.7:  # 70% chance
                    self.client.get(f"/api/bookings/{booking_response['bookingId']}")
            else:
                logging.error(f"Failed to create booking: {response.status_code}, {response.text}")

# You can run this with: locust -f locustfile.py --host=http://34.118.54.253