
from db import conn, cursor
from pydantic import BaseModel
from typing import List, Optional
from fastapi import HTTPException

class Product(BaseModel):
    id: Optional[int]
    name: str
    price: float

    TABLE_NAME = "products"

    def save(self):
        sql = f"INSERT INTO {self.TABLE_NAME} (name, price) VALUES (?, ?)"
        cursor.execute(sql, (self.name, self.price))
        conn.commit()
        self.id = cursor.lastrowid
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }

    @classmethod
    def create(cls, product):
        return product.save()

    @classmethod
    def find_all(cls) -> List:
        cursor.execute(f"SELECT * FROM {cls.TABLE_NAME}")
        rows = cursor.fetchall()
        return [cls.row_to_instance(row) for row in rows]

    @classmethod
    def update(cls, id: int, product):
        sql = f"UPDATE {cls.TABLE_NAME} SET name = ?, price = ? WHERE id = ?"
        cursor.execute(sql, (product.name, product.price, id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        conn.commit()
        product.id = id
        return product

    @classmethod
    def delete(cls, id: int) -> dict:
        sql = f"DELETE FROM {cls.TABLE_NAME} WHERE id = ?"
        cursor.execute(sql, (id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        conn.commit()
        return {"message": "Product deleted successfully"}

    @classmethod
    def row_to_instance(cls, row):
        if row is None:
            return None
        product = cls(id=row[0], name=row[1], price=row[2])
        return product

    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """
        cursor.execute(sql)
        conn.commit()
        print(f"{cls.TABLE_NAME.capitalize()} table created")

Product.create_table()


