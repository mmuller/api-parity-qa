import sqlite3
from validation.config import DB_PATH


class DBHelper:

    @staticmethod
    def get_order_by_id(order_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT customer, amount, status FROM orders WHERE id = ?", (order_id,)
        )

        row = cursor.fetchone()
        conn.close()

        return row
