from pydantic import BaseModel, Field
from typing import ClassVar
from database import conn, cursor

class User(BaseModel):
    TABLE_NAME: ClassVar[str] = "users"

    id: int = None
    username: str
    order_id: int

def save(self):
    sql = f"INSERT INTO {self.TABLE_NAME} (username, order_id) VALUES (?, ?)"
    cursor.execute(sql, (self.username, self.order_id))
    conn.commit()
    self.id = cursor.lastrowid
    return self

def update(self, updated_data):
    sql = f"UPDATE {self.TABLE_NAME} SET username = ?, order_id = ? WHERE id = ?"
    cursor.execute(sql, (updated_data.username, updated_data.order_id, self.id))
    conn.commit()
    return self

def delete(self):
    sql = f"DELETE FROM {self.TABLE_NAME} WHERE id = ?"
    cursor.execute(sql, (self.id,))
    conn.commit()
    return {"message": "User deleted successfully"}

def to_dict(self):
    return {"id": self.id, "username": self.username, "order_id": self.order_id}

@classmethod
def find_one(cls, id):
    sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE id = ?"
    row = cursor.execute(sql, (id,)).fetchone()
    return cls.row_to_instance(row)

@classmethod
def find_all(cls):
    sql = f"SELECT * FROM {cls.TABLE_NAME}"
    rows = cursor.execute(sql).fetchall()
    return [cls.row_to_instance(row).to_dict() for row in rows]

@classmethod
def row_to_instance(cls, row):
    if row is None:
        return None
    user = cls(username=row[1], order_id=row[2])
    user.id = row[0]
    return user

@classmethod
def create_table(cls):
    sql = f"""
        CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            order_id INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """
    cursor.execute(sql)
    conn.commit()