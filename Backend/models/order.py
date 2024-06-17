from pydantic import BaseModel
from typing import ClassVar
from database import conn, cursor

class Order(BaseModel):
    TABLE_NAME: ClassVar[str] = "orders"

    id: int = None
    product_id: int

    def save(self):
        try:
            sql = f"INSERT INTO {self.TABLE_NAME} (product_id) VALUES (?)"
            print(f"Executing SQL: {sql} with product_id: {self.product_id}")
            cursor.execute(sql, (self.product_id,))
            conn.commit()
            self.id = cursor.lastrowid
            return self
        except Exception as e:
            print(f"Error saving order: {e}")
            conn.rollback()

    def update(self, updated_data):
        try:
            sql = f"UPDATE {self.TABLE_NAME} SET product_id = ? WHERE id = ?"
            print(f"Executing SQL: {sql} with product_id: {updated_data.product_id} and id: {self.id}")
            cursor.execute(sql, (updated_data.product_id, self.id))
            conn.commit()
            return self
        except Exception as e:
            print(f"Error updating order: {e}")
            conn.rollback()

    def delete(self):
        try:
            sql = f"DELETE FROM {self.TABLE_NAME} WHERE id = ?"
            print(f"Executing SQL: {sql} with id: {self.id}")
            cursor.execute(sql, (self.id,))
            conn.commit()
            return {"message": "Order deleted successfully"}
        except Exception as e:
            print(f"Error deleting order: {e}")
            conn.rollback()

    def to_dict(self):
        return {"id": self.id, "product_id": self.product_id}

    @classmethod
    def find_one(cls, id):
        try:
            sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE id = ?"
            print(f"Executing SQL: {sql} with id: {id}")
            row = cursor.execute(sql, (id,)).fetchone()
            return cls.row_to_instance(row)
        except Exception as e:
            print(f"Error finding order: {e}")

    @classmethod
    def find_all(cls):
        try:
            sql = f"SELECT * FROM {cls.TABLE_NAME}"
            print(f"Executing SQL: {sql}")
            rows = cursor.execute(sql).fetchall()
            return [cls.row_to_instance(row).to_dict() for row in rows]
        except Exception as e:
            print(f"Error finding all orders: {e}")

    @classmethod
    def row_to_instance(cls, row):
        if row is None:
            return None
        order = cls(product_id=row[1])
        order.id = row[0]
        return order

    @classmethod
    def create_table(cls):
        try:
            sql = f"""
                CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """
            print(f"Executing SQL: {sql}")
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

Order.create_table()