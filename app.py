from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import sqlite3
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()

# Database setup

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


def get_db():
    conn = sqlite3.connect("transactions.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount number NOT NULL,
            description TEXT,
            type TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()

# Pydantic models


class TransactionIn(BaseModel):
    amount: float
    description: str = ""
    type: str = ""
    date: date


class Transaction(TransactionIn):
    id: int

# Endpoints


@app.post("/transactions/", response_model=Transaction)
def add_transaction(transaction: TransactionIn):
    """
    Create a new transaction record.

    Inserts a new transaction into the database using the provided transaction details.
    The transaction includes amount, description, type, and date. Returns the created
    transaction with its assigned unique ID.

    Args:
        transaction (TransactionIn): The transaction data to be added.

    Returns:
        dict: The created transaction data including the generated 'id'.

    Raises:
        HTTPException: If the database operation fails (not explicitly handled here).
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (amount, description, type, date) VALUES (?, ?, ?, ?)",
        (transaction.amount, transaction.description,
         transaction.type, transaction.date.isoformat())
    )
    conn.commit()
    transaction_id = cursor.lastrowid
    conn.close()
    return {**transaction.dict(), "id": transaction_id}


@app.get("/transactions/", response_model=List[Transaction])
def get_transactions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.delete("/transactions/{transaction_id}", response_model=dict)
def delete_transaction(transaction_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
