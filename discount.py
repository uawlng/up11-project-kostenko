import psycopg

def calculate_price(product_id, base_price):
    if not isinstance(product_id, int):
        print("Ошибка: product_id должен быть целым числом")
        return None, None
    if not isinstance(base_price, (int, float)):
        print("Ошибка: base_price должен быть числом")
        return None, None
    if base_price <= 0:
        print("Ошибка: base_price должен быть больше нуля")
        return None, None

    conn = None
    try:
        conn = psycopg.connect(
            host="localhost", port=5432, dbname="sad_i_ogorod",
            user="postgres", password="123"  
        )
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM products WHERE product_id = %s;", (product_id,))
        product_result = cursor.fetchone()
        
        if product_result is None:
            print("Ошибка: товар не найден")
            return None, None
            
        product_name = product_result[0]

        cursor.execute("""
            SELECT COUNT(*) 
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            WHERE oi.stock_item_id = %s
            AND o.order_date >= CURRENT_DATE - INTERVAL '1 month';
        """, (product_id,))

        result = cursor.fetchone()
        if result is None:
            print("Ошибка: нет результата")
            return None, None
            
        orders_count = result[0]

        if orders_count == 0:
            discount_size = base_price * 0.25  
            final_price = base_price - discount_size
            print(f"Товар: {product_name} | Скидка 25%: {discount_size} руб.")
        else:
            final_price = base_price
            discount_size = 0.0
            print(f"Товар: {product_name} | Скидка не применяется")

        return final_price, discount_size

    except psycopg.Error as e:
        print(f"Ошибка БД: {e}")
        return None, None
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    price, discount = calculate_price(1, 1000)
    print(f"Итоговая цена: {price}, Скидка: {discount}")
    
    calculate_price(99999, 1000)