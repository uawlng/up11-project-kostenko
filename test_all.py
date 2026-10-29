import psycopg
from discount import calculate_price

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="sad_i_ogorod",
    user="postgres",
    password="123"  
)
cursor = conn.cursor()

cursor.execute("SELECT product_id, name, price FROM products;")
products = cursor.fetchall()

print(f"{'ID':<4} {'Товар':<25} {'Цена':<10} {'Итог':<10} {'Скидка'}")
print("-" * 70)

for product_id, name, price in products:
    final_price = calculate_price(product_id, float(price))
    
    if final_price is not None and final_price < float(price):
        discount = "Да"
    else:
        discount = "Нет"
        
    print(f"{product_id:<4} {name[:23]:<25} {price:<10} {final_price:<10} {discount}")

cursor.close()
conn.close()