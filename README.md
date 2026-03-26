Here is a complete technical documentation in Markdown format for your FastAPI Expense Manager backend project:

---

# Expense Manager Backend

A simple FastAPI backend for managing financial transactions, using SQLite as the database.

## Table of Contents

- Project Structure
- Models
- API Endpoints
  - Add Transaction
  - Get All Transactions
  - Delete Transaction
- Database Schema
- How to Run
- Testing

---

## Project Structure

```
expense-manager-backend/
├── app.py
├── transactions.db  # Created at runtime
└── README.md
```

---

## Models

### TransactionIn

| Field       | Type   | Description                        |
|-------------|--------|------------------------------------|
| amount      | float  | The amount of the transaction      |
| description | str    | Description of the transaction     |
| type        | str    | Type of transaction (e.g., expense, income) |
| date        | date   | Date of the transaction (YYYY-MM-DD) |

### Transaction

Extends `TransactionIn` with:

| Field | Type | Description                |
|-------|------|----------------------------|
| id    | int  | Unique identifier (auto-increment) |

---

## API Endpoints

### Add Transaction

- **URL:** `/transactions/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "amount": 100.0,
    "description": "Grocery shopping",
    "type": "expense",
    "date": "2023-01-01"
  }
  ```
- **Response:**
  ```json
  {
    "amount": 100.0,
    "description": "Grocery shopping",
    "type": "expense",
    "date": "2023-01-01",
    "id": 1
  }
  ```
- **Description:**  
  Creates a new transaction record and returns the created transaction with its unique ID.

---

### Get All Transactions

- **URL:** `/transactions/`
- **Method:** `GET`
- **Response:**
  ```json
  [
    {
      "amount": 100.0,
      "description": "Grocery shopping",
      "type": "expense",
      "date": "2023-01-01",
      "id": 1
    },
    ...
  ]
  ```
- **Description:**  
  Retrieves a list of all transactions in the database.

---

### Delete Transaction

- **URL:** `/transactions/{transaction_id}`
- **Method:** `DELETE`
- **Response (Success):**
  ```json
  {
    "message": "Transaction deleted"
  }
  ```
- **Response (Not Found):**
  ```json
  {
    "detail": "Transaction not found"
  }
  ```
- **Description:**  
  Deletes the transaction with the specified ID.

---

## Database Schema

The SQLite database contains a single table:

```sql
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount NUMBER NOT NULL,
    description TEXT,
    type TEXT NOT NULL,
    date TEXT NOT NULL
);
```

---

## How to Run

1. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn pydantic
   ```

2. **Start the server:**
   ```bash
   uvicorn app:app --reload
   ```

3. **Access the API docs:**  
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser for interactive Swagger UI.

---

## Testing

You can write tests using `pytest` and FastAPI's `TestClient`.  
Example test file: `test_app.py`

---

## CORS

CORS is enabled for all origins, methods, and headers for development convenience.

---

## License

MIT License (add your license here if needed)

---

Let me know if you need more details or want to include usage examples or test cases!