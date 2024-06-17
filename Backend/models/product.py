from pydantic import BaseModel
from typing import ClassVar
from database import conn, cursor

class Product(BaseModel):
    TABLE_NAME: ClassVar[str] = "products"

    id: int = None
    name: str
    description: str
    cost: int
    image: bytes

    def save(self):
        sql = f"INSERT INTO {self.TABLE_NAME} (name, description, cost, image) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (self.name, self.description, self.cost, self.image))
        conn.commit()
        self.id = cursor.lastrowid
        return self

    def update(self):
        sql = f"UPDATE {self.TABLE_NAME} SET name = ?, description = ?, cost = ?, image = ? WHERE id = ?"
        cursor.execute(sql, (self.name, self.description, self.cost, self.image, self.id))
        conn.commit()
        return self

    def delete(self):
        sql = f"DELETE FROM {self.TABLE_NAME} WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
        return {"message": "Product deleted successfully"}

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "cost": self.cost, "image": self.image}

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
        product = cls(name=row[1], description=row[2], cost=row[3], image=row[4])
        product.id = row[0]
        return product

    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                cost INTEGER,
                image BLOB
            )
        """
        cursor.execute(sql)
        conn.commit()

# Ensure the table is created in the database
Product.create_table()
