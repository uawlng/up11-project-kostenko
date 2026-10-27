import psycopg2
from psycopg2 import pool

class Database:
    def __init__(self):
        self.connection_pool = None
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                1, 5,
                host="localhost", port=5432,
                database="sad_i_ogorod", user="postgres", password="123"
            )
            print("Пул соединений создан")
        except psycopg2.Error as e:
            print(f"Ошибка БД: {e}")
            self.connection_pool = None

    def get_connection(self):
        if self.connection_pool is not None:
            return self.connection_pool.getconn()
        return None

    def release_connection(self, conn):
        if self.connection_pool is not None and conn is not None:
            self.connection_pool.putconn(conn)

    def close_all(self):
        if self.connection_pool is not None:
            self.connection_pool.closeall()
            print("Пул закрыт")

    def get_categories(self):
        conn = self.get_connection()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM categories ORDER BY name")
            categories = cursor.fetchall()
            cursor.close()
            return [row[0] for row in categories]
        except psycopg2.Error as e:
            print(f"Ошибка запроса категорий: {e}")
            return []
        finally:
            self.release_connection(conn)

    def get_products(self, search="", category="Все категории", sort_order="По возрастанию"):
        conn = self.get_connection()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            
            search_pattern = f"%{search}%"
            order = "ASC" if sort_order == "По возрастанию" else "DESC"
            
            # Запрос без p.description (поиск только по названию)
            query = f"""
                SELECT p.product_id, p.name, p.price, p.image, 
                       COALESCE(m.name, 'Неизвестно') AS manufacturer,
                       COALESCE(SUM(si.quantity), 0) AS total_quantity,
                       COALESCE(c.name, 'Без категории') AS category_name
                FROM products p
                LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN stock_items si ON p.product_id = si.product_id
                WHERE p.name ILIKE %s
                AND (c.name = %s OR %s = 'Все категории')
                GROUP BY p.product_id, p.name, p.price, p.image, m.name, c.name
                ORDER BY p.price {order}
            """
            
            cursor.execute(query, (search_pattern, category, category))
            products = cursor.fetchall()
            cursor.close()
            return products
        except psycopg2.Error as e:
            print(f"Ошибка запроса: {e}")
            return []
        finally:
            self.release_connection(conn)