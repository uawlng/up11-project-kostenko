import psycopg2
from psycopg2 import pool

class Database:
    def __init__(self):
        self.connection_pool = None
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                1, 5,
                host="localhost",
                port=5432,
                database="sad_i_ogorod",  
                user="postgres",
                password="123"            
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

    def get_products(self):
        conn = self.get_connection()
        if conn is None:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.product_id, p.name, p.price, p.image, m.name
                FROM products p
                LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
                ORDER BY p.product_id
            """)
            products = cursor.fetchall()
            cursor.close()
            return products
        except psycopg2.Error as e:
            print(f"Ошибка запроса: {e}")
            return []
        finally:
            self.release_connection(conn)