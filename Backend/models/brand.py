from pydantic import BaseModel, Field
from typing import ClassVar
from database import conn, cursor

class Brand(BaseModel):
    TABLE_NAME: ClassVar[str] = "brands"

    id: int = None
    name: str
    product_id: int

    def save(self):
        sql = f"INSERT INTO {self.TABLE_NAME} (name, product_id) VALUES (?, ?)"
        cursor.execute(sql, (self.name, self.product_id))
        conn.commit()
        self.id = cursor.lastrowid
        return self

    def update(self, updated_data):
        sql = f"UPDATE {self.TABLE_NAME} SET name = ?, product_id = ? WHERE id = ?"
        cursor.execute(sql, (updated_data.name, updated_data.product_id, self.id))
        conn.commit()
        return self

    def delete(self):
        sql = f"DELETE FROM {self.TABLE_NAME} WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
        return {"message": "Brand deleted successfully"}

    def to_dict(self):
        return {"id": self.id, "name": self.name, "product_id": self.product_id}

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
        brand = cls(name=row[1], product_id=row[2])
        brand.id = row[0]
        return brand

    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                product_id INTEGER,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """
        cursor.execute(sql)
        conn.commit()

Brand.create_table()