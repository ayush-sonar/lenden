# Lenden

## Project Setup

### Prerequisites

- Python 3.8+
- Django 5.1.5
- Virtualenv

### Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd lenden
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Make the migrations:

    ```sh
    python3 manage.py makemigrations
    ```

5. Apply the migrations:

    ```sh
    python3 manage.py migrate
    ```

6. Create a superuser:

    ```sh
    python3 manage.py createsuperuser
    ```

7. Run the development server:

    ```sh
    python3 manage.py runserver
    ```

## Database Design

### Models

#### User

- `id`: Primary Key
- `username`: CharField
- `password`: CharField
- `games_played`: IntegerField
- `games_won`: IntegerField
- `games_lost`: IntegerField
- `games_drawn`: IntegerField

#### Game

- `id`: UUIDField (Primary Key)
- `p1`: ForeignKey (User)
- `p2`: ForeignKey (User)
- `status`: CharField (Choices: 'P', 'A', 'F')
- `canvas`: JSONField
- `currentTurn`: ForeignKey (User)
- `winner`: ForeignKey (User, nullable)
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

#### Move

- `id`: BigAutoField (Primary Key)
- `game`: ForeignKey (Game)
- `player`: ForeignKey (User)
- `pos_x`: IntegerField
- `pos_y`: IntegerField
- `move_number`: IntegerField
- `timestamp`: DateTimeField

## Endpoints

### Authentication

- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token

### User

- `POST /api/auth/register/`: Register a new user
- `GET /api/auth/profile/`: Retrieve user profile
- `PUT /api/auth/profile/`: Update user profile

### Game

- `GET /api/games/`: List all games for the authenticated user
- `POST /api/games/`: Create a new game
- `POST /api/games/{id}/accept/`: Accept a game (only player 2 can accept)
- `POST /api/games/{id}/move/`: Make a move in the game
- `GET /api/games/history/`: List finished games for the authenticated user
- `GET /api/games/history/{id}/`: Retrieve details of a finished game

### Admin

- `GET /admin/`: Admin interface for managing users, games, and moves


# API Documentation
## Base URL

`http://localhost:8000`

---

## Authentication Endpoints

### Register User

**URL:** `/api/auth/register/`\
**Method:** `POST`\
**Request Body:**

```json
{
    "username": "string",
    "password": "string"
}
```

**Response:**

- `201 Created` on success.
- `400 Bad Request` for invalid input.

---

### Login User

**URL:** `/api/token/`\
**Method:** `POST`\
**Request Body:**

```json
{
    "username": "string",
    "password": "string"
}
```

**Response:**

- `200 OK` on success with an access token:
  ```json
  {
      "access": "string"
  }
  ```
- `401 Unauthorized` on failure.

---

### Get User Details

**URL:** `/api/auth/profile/`\
**Method:** `GET`\
**Headers:**\
`Authorization: Bearer <access_token>`\
**Response:**

- `200 OK` with user profile information.
- `401 Unauthorized` if not authenticated.

---

## Game Management Endpoints

### Create a Game

**URL:** `/api/games/`\
**Method:** `POST`\
**Headers:**\
`Authorization: Bearer <access_token>`\
**Request Body:**

```json
{
    "p1": "string", 
    "p2": "string"
}
```

**Response:**

- `201 Created` with game details.
- `400 Bad Request` for invalid input.

---

### Accept Game

**URL:** `/api/games/{gameID}/accept/`\
**Method:** `POST`\
**Headers:**\
`Authorization: Bearer <access_token>`\
**Response:**

- `200 OK` on successful acceptance.
- `404 Not Found` if game does not exist.

---

### Make a Move

**URL:** `/api/games/{gameID}/move/`\
**Method:** `POST`\
**Headers:**\
`Authorization: Bearer <access_token>`\
**Request Body:**

```json
{
    "pos_x": "integer",
    "pos_y": "integer"
}
```

**Response:**

- `200 OK` with updated game state.
- `400 Bad Request` for invalid input.

---

### Game History

**URL:** `/api/games/history/`\
**Method:** `GET`\
**Headers:**\
`Authorization: Bearer <access_token>`\
**Response:**

- `200 OK` with a list of games played by the user.
- `401 Unauthorized` if not authenticated.

---

## Notes

- Replace `{gameID}` with the actual game ID in the endpoints.
- Use valid JWT access tokens in the `Authorization` header for all protected endpoints.

