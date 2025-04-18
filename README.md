# Ticket Booking System - Full Stack

This is a full-stack web application for booking movie tickets, built with an Angular frontend and a Node.js/Express backend connected to a MySQL database.

## Features

*   Browse a list of currently playing movies.
*   View detailed information about a specific movie.
*   Select showtimes for a movie.
*   Visually select available seats for a chosen showtime.
*   Book selected seats.
*   View booking confirmation details.

## Tech Stack

*   **Frontend:** Angular (Standalone Components)
*   **Backend:** Node.js, Express.js
*   **Database:** MySQL
*   **API Communication:** RESTful API

## Prerequisites

Before you begin, ensure you have the following installed:

*   [Node.js](https://nodejs.org/) (which includes npm)
*   [MySQL Server](https://dev.mysql.com/downloads/mysql/)

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Krishna18062005/Ticket_Booking_System_Full-Stack.git
    cd Ticket_Booking_System_Full-Stack
    ```

2.  **Backend Setup:**
    *   Navigate to the backend directory (e.g., `cd backend` - adjust if your folder name is different).
    *   Install dependencies:
        ```bash
        npm install
        ```
    *   **Database Configuration:**
        *   Create a MySQL database (e.g., `movie_booking_db`).
        *   Configure your database connection details. This might be in a `.env` file or directly in a config file (e.g., `src/config/database.ts`). You'll typically need:
            *   `DB_HOST` (e.g., `localhost`)
            *   `DB_USER` (e.g., `root`)
            *   `DB_PASSWORD` (your MySQL password)
            *   `DB_NAME` (e.g., `movie_booking_db`)
        *   *(If using a `.env` file, create one based on a potential `.env.example`)*
    *   **Database Schema:** Run the necessary SQL scripts to create the `movies` and `bookings` tables. You might have these in an `sql/` directory or need to create them based on your entity models.
        ```sql
        -- Example table structures (adjust as per your actual schema)
        CREATE TABLE movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            duration INT, -- Duration in minutes
            rating DECIMAL(3, 1),
            -- Add other fields like poster_url, release_date etc. if needed
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_id INT NOT NULL,
            showtime VARCHAR(50) NOT NULL, -- Or DATETIME if storing specific date/time
            seats TEXT NOT NULL, -- Storing seats as JSON array string '["S1", "S5"]'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
        );
        ```
    *   **Seed Data (Optional):** Insert initial movie data into the `movies` table using SQL `INSERT` statements.

3.  **Frontend Setup:**
    *   Navigate to the frontend directory (e.g., `cd ../frontend-angular` - adjust if your folder name is different).
    *   Install dependencies:
        ```bash
        npm install
        ```

## Running the Application

1.  **Start the Backend Server:**
    *   Navigate to the backend directory.
    *   Run the development server (this command might differ based on your `package.json`):
        ```bash
        npm run dev
        ```
    *   The backend API should now be running (typically on `http://localhost:3001`).

2.  **Start the Frontend Server:**
    *   Navigate to the frontend directory.
    *   Run the Angular development server:
        ```bash
        ng serve -o
        ```
    *   This will compile the Angular app, start a development server (usually on `http://localhost:4200`), and open it in your default browser.

Now you should be able to access and use the ticket booking application.

## API Endpoints (Example)

*   `GET /api/movies`: Get list of all movies.
*   `GET /api/movies/:id`: Get details of a specific movie.
*   `GET /api/bookings/booked-seats?movieId=<id>&showtime=<time>`: Get booked seats for a specific movie/showtime.
*   `POST /api/bookings`: Create a new booking.
*   `GET /api/bookings/:id`: Get details of a specific booking.
