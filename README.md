# Daily Habit Tracker

A production-level daily habit tracker built with Flask, SQLite, Alpine.js, and Tailwind CSS.

## Features
-   **User Authentication:** Secure login and registration.
-   **Habit Management:** Create, edit, archive, and delete habits.
-   **Visual Tracking:** Daily check-offs, progress bars, and calendar heatmaps.
-   **Statistics:** Consistency trends and best performing habits.
-   **Interactive UI:** Drag-and-drop reordering, dark mode, and responsive design.

## Installation

1.  **Clone the repository** (if not already done).
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**
    -   Windows: `venv\Scripts\activate`
    -   Mac/Linux: `source venv/bin/activate`
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the App

1.  **Initialize the database and run the server:**
    ```bash
    python run.py
    ```
    The database will be automatically created in `instance/database.sqlite` on the first run.

2.  **Open your browser:**
    Navigate to `http://127.0.0.1:5000`.

## Project Structure
-   `app/`: Main application source code.
    -   `blueprints/`: Route handlers (auth, main, habits, stats).
    -   `templates/`: HTML templates (Jinja2).
    -   `models.py`: Database models.
-   `config.py`: Application configuration.
-   `run.py`: Application entry point.

## Tech Stack
-   **Backend:** Flask, SQLAlchemy
-   **Frontend:** Tailwind CSS (CDN), Alpine.js (CDN), SortableJS, Chart.js
-   **Database:** SQLite
