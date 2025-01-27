# Event Management API

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Database Schema](#database-schema)
8. [Error Handling](#error-handling)
9. [Testing](#testing)
10. [Contributing](#contributing)
11. [License](#license)
12. [Contact](#contact)

---

## 1. Project Overview

The **Event Management API** is a backend service built with FastAPI. It enables users to create, update, delete, and fetch event information. It supports filtering and querying based on event attributes such as status, location, and date.

This API is ideal for managing events in applications such as:

- Event booking platforms
- Corporate event management
- Personal scheduling tools

---

## 2. Features

- Create, update, and delete events.
- Fetch event details by ID.
- Filter events based on status, location, or date.
- Error handling with appropriate HTTP status codes.
- Database integration with SQLAlchemy and support for relational databases.

---

## 3. Technologies Used

- **Framework**: FastAPI
- **Database**: SQLAlchemy with MySQL
- **Python Version**: Python 3.x
- **Libraries**:
  - `Pydantic` for data validation
  - `uvicorn` for ASGI server
- **Tools**:
  - Virtual environment for dependency management
  - Postman for API testing

---

## 4. Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MySQL server installed and running
- Git (optional for cloning the repository)

### Steps to Set Up the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/event-management-api.git
   cd event-management-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate    # For Linux/Mac
   venv\Scripts\activate       # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a MySQL database (e.g., `event_management`).
   - Update the `DATABASE_URL` in the `.env` file with your database credentials:
     ```
     DATABASE_URL=mysql+pymysql://username:password@localhost/event_management
     ```

5. Run migrations (if applicable):
   ```bash
   alembic upgrade head
   ```

6. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Access the API documentation:
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the Swagger UI.

---

## 5. Usage

- Test the API using tools like Postman or cURL.
- Refer to the API documentation available at `/docs` for detailed endpoints and request formats.

---

## 6. API Endpoints

### Base URL: `/api/v1`

| Method | Endpoint               | Description                         |
|--------|-------------------------|-------------------------------------|
| POST   | `/events/`             | Create a new event                 |
| PUT    | `/events/{event_id}`   | Update an existing event           |
| GET    | `/events/`             | Fetch all events with filters      |
| GET    | `/events/{event_id}`   | Fetch details of a specific event  |
| DELETE | `/events/{event_id}`   | Delete an event by its ID          |

---

## 7. Database Schema

### `Event` Table

| Column         | Type          | Description                       |
|----------------|---------------|-----------------------------------|
| `event_id`     | Integer (PK)  | Unique identifier for each event |
| `name`         | String        | Name of the event                |
| `description`  | String        | Detailed description             |
| `start_time`   | DateTime      | Start date and time of the event |
| `end_time`     | DateTime      | End date and time of the event   |
| `location`     | String        | Location of the event            |
| `max_attendees`| Integer       | Maximum attendees allowed        |
| `status`       | Enum          | Status of the event (Scheduled, Completed, etc.) |

---

## 8. Error Handling

- **404 Not Found**: Returned when a requested resource (e.g., event) is not found.
- **400 Bad Request**: Returned for validation errors in request data.
- **500 Internal Server Error**: Returned for unexpected server-side issues.

---

## 9. Testing

Run unit tests to verify functionality:

1. Install test dependencies:
   ```bash
   pip install pytest
   ```

2. Run tests:
   ```bash
   pytest tests/
   ```

---

## 10. Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a description of your changes.
