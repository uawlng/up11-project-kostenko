from database import Database

def main():
    print(" Тест подключения к БД ")
    db = Database()
    
    products = db.get_products()
    print(f"Количество товаров: {len(products)}")
    
    if products:
        print("\nПервые 3 товара:")
        for p in products[:3]:
            print(f"ID: {p[0]}, Название: {p[1]}, Цена: {p[2]}")
    else:
        print("Товары не найдены.")
        
    db.close_all()

if __name__ == "__main__":
    main()