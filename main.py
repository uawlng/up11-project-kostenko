import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,
                               QWidget, QHBoxLayout, QScrollArea, QPushButton,
                               QMessageBox, QComboBox, QLineEdit)
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt
from database import Database

#Функция
def calculate_discount(old_price, new_price):
    # Защита от деления на ноль, если старой цены нет
    if old_price == 0:
        return 0
    # Процент скидки
    return (old_price - new_price) / old_price * 100


def calculate_price(product_id, old_price):
    # Скидка 20% 
    return float(old_price) * 0.8


def create_card(product):
    card = QWidget()
    card.setObjectName("productCard")

    # Остаток на складе
    total_quantity = product[5] if len(product) > 5 else 1
    old_price = float(product[2]) if product[2] else 0.0
    new_price = calculate_price(product[0], old_price)
    discount = calculate_discount(old_price, new_price)

    # Подсветка карточки в зависимости от остатка и скидки
    if total_quantity == 0:
        # Товара нет на складе
        bg_color = "#ADD8E6"
        border_color = "#ADD8E6"
    elif discount > 15:
        # Скидка больше 15%
        bg_color = "#E8F5E9"
        border_color = "#2E8B57"
    else:
        bg_color = "#FFFFFF"
        border_color = "#000000"

    card.setStyleSheet(f"""
        #productCard {{
            border: 1px solid {border_color};
            border-radius: 4px;
            background-color: {bg_color};
        }}
        #productCard QLabel {{
            background-color: transparent;
            font-family: Calibri;
        }}
    """)

    main_layout = QHBoxLayout(card)
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(15)

    image_label = QLabel()
    image_label.setFixedSize(100, 100)
    image_label.setAlignment(Qt.AlignCenter)
    image_label.setStyleSheet("border: 1px solid #000000; background-color: #FFFFFF;")

    product_id = product[0]
    name = product[1] if product[1] else "Наименование"
    file_name = product[3]
    manufacturer = product[4] if product[4] else "Неизвестный производитель"

    # Название категории
    category_name = product[6] if len(product) > 6 else "Без категории"

    # Путь к заглушке
    placeholder_path = os.path.join("resources", "picture.png")

    if file_name:
        image_path = os.path.join("images", file_name)
    else:
        # Если имя файла не указано
        image_path = placeholder_path

    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        # Файл не найден 
        pixmap = QPixmap(placeholder_path)

    if pixmap.isNull():
        image_label.setText("IMG")
    else:
        image_label.setPixmap(
            pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
    main_layout.addWidget(image_label)

    text_layout = QVBoxLayout()
    text_layout.setSpacing(5)

    text_style = "font-size: 14px; border: none; color: #000000; font-family: Calibri;"

    title = QLabel(f"<b>{manufacturer} | {name}</b>")
    title.setStyleSheet(text_style)

    category_label = QLabel(f"Категория: {category_name}")
    category_label.setStyleSheet(text_style)

    # Нет в наличии
    quantity_text = f"Количество: {total_quantity} шт." if total_quantity > 0 else "Нет в наличии"
    quantity_label = QLabel(quantity_text)

    if total_quantity == 0:
        # Нет в наличии 
        quantity_label.setStyleSheet("font-size: 14px; border: none; color: #d9534f; font-weight: bold; font-family: Calibri;")
    else:
        quantity_label.setStyleSheet(text_style)

    compound_label = QLabel(f"Состав: Металл, дерево")
    compound_label.setStyleSheet(text_style)
    compound_label.setWordWrap(True)

    text_layout.addWidget(title)
    text_layout.addWidget(category_label)
    text_layout.addWidget(quantity_label)
    text_layout.addWidget(compound_label)
    text_layout.addStretch()

    main_layout.addLayout(text_layout, 1)

    price_layout = QVBoxLayout()
    price_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
    price_layout.setSpacing(2)

    # Старая цена зачёркнута
    old_price_label = QLabel(f"<s>{old_price:.2f} ₽</s>")
    old_price_label.setAlignment(Qt.AlignRight)
    old_price_label.setStyleSheet("color: red; font-size: 14px; border: none; font-family: Calibri;")

    new_price_label = QLabel(f"<b>{new_price:.2f} ₽</b>")
    new_price_label.setAlignment(Qt.AlignRight)

    if discount > 15:
        # Большая скидка 
        new_price_label.setStyleSheet("color: #2E8B57; font-weight: bold; font-size: 16px; border: none; font-family: Calibri;")
    else:
        new_price_label.setStyleSheet("color: black; font-weight: bold; font-size: 16px; border: none; font-family: Calibri;")

    if discount > 0:
        old_price_label.show()
    else:
        old_price_label.hide()

    price_layout.addWidget(old_price_label)
    price_layout.addWidget(new_price_label)

    main_layout.addLayout(price_layout)

    return card


class MainWindow(QMainWindow):
    def __init__(self, role_id=None, full_name=None, db=None):
        super().__init__()
        self.role_id = role_id
        self.full_name = full_name
        self.db = db if db is not None else Database()

        self.setWindowTitle("Сад и огород — Каталог")
        self.resize(900, 700)
        self.setWindowIcon(QIcon("resources/icon.ico"))

        font = QFont("Calibri", 10)
        self.setFont(font)

        self.setStyleSheet("""
            QMainWindow { background-color: #FFFFFF; font-family: Calibri; }
            QLabel { font-family: Calibri; }
            #HeaderLabel { font-size: 28px; font-weight: bold; color: #2c3e50; margin: 20px; }
            QPushButton { 
                padding: 10px; margin: 5px; font-size: 14px; 
                background-color: #70B2AF; color: white; 
                border: none; border-radius: 5px; font-family: Calibri; 
            }
            QPushButton:hover { background-color: #5a9a97; }
            QComboBox, QLineEdit {
                padding: 5px; font-size: 14px; font-family: Calibri; 
                border: 1px solid #ccc; border-radius: 3px;
            }
        """)

        self.setup_ui()
        self.setup_role_interface()
        self.load_products()

    def setup_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Шапка
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #D2F6E7; border-radius: 5px;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)

        logo_header = QLabel()
        pixmap_logo = QPixmap("resources/logo.png")
        if not pixmap_logo.isNull():
            logo_header.setPixmap(pixmap_logo.scaledToHeight(50, Qt.SmoothTransformation))
        header_layout.addWidget(logo_header)

        header_layout.addStretch()

        # Если ФИО нет — прочерк
        name_text = f"ФИО: {self.full_name}" if self.full_name else "ФИО: —"
        name_label = QLabel(name_text)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; background-color: transparent;")
        header_layout.addWidget(name_label)

        self.logout_button = QPushButton("Выход")
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #70B2AF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-family: Calibri;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a9a97;
            }
        """)
        header_layout.addWidget(self.logout_button)

        main_layout.addWidget(header_widget)

        title = QLabel("Сад и огород — Каталог")
        title.setObjectName("HeaderLabel")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        controls_layout = QHBoxLayout()

        # Поле поиска 
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        self.search_input.textChanged.connect(self.load_products)
        controls_layout.addWidget(self.search_input, 2)

        # Фильтр по категориям 
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Все категории")
        categories = self.db.get_categories()
        for cat in categories:
            self.filter_combo.addItem(cat)
        self.filter_combo.currentIndexChanged.connect(self.load_products)
        controls_layout.addWidget(self.filter_combo, 1)

        # Сортировка по цене
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["По возрастанию", "По убыванию"])
        self.sort_combo.currentIndexChanged.connect(self.load_products)
        controls_layout.addWidget(self.sort_combo, 1)

        main_layout.addLayout(controls_layout)

        # Кнопки ролей 
        self.order_button = QPushButton("Оформить заказ")
        self.manager_button = QPushButton("Заказы (менеджер)")
        self.admin_button = QPushButton("Админ-панель")

        main_layout.addWidget(self.order_button)
        main_layout.addWidget(self.manager_button)
        main_layout.addWidget(self.admin_button)

        # Область прокрутки для карточек товаров
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background-color: #FFFFFF")

        self.container = QWidget()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.container)
        main_layout.addWidget(self.scroll)

        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def load_products(self):
        search = self.search_input.text()
        category = self.filter_combo.currentText()
        sort_order = self.sort_combo.currentText()

        for i in reversed(range(self.list_layout.count())):
            widget = self.list_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.products = self.db.get_products(search, category, sort_order)
        if not self.products:
            self.list_layout.addWidget(QLabel("Товары не найдены."))
        else:
            for product in self.products:
                self.list_layout.addWidget(create_card(product))

    def setup_role_interface(self):
        self.order_button.hide()
        self.manager_button.hide()
        self.admin_button.hide()

        # Администратор 
        if self.role_id == 1:
            self.admin_button.show()
            self.manager_button.show()
        # Менеджер 
        elif self.role_id == 2:
            self.manager_button.show()
        # Покупатель 
        elif self.role_id == 3:
            self.order_button.show()

    def logout(self):
        # Подтверждение выхода
        reply = QMessageBox.question(
            self,
            "Выход",
            "Вы уверены, что хотите выйти?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            from window_login import LoginWindow
            self.login_window = LoginWindow(self.db)
            self.login_window.show()
            self.close()

    def closeEvent(self, event):
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = Database()

    from window_login import LoginWindow
    login_window = LoginWindow(db)
    login_window.show()

    exit_code = app.exec()
    # Закрываем пул соединений при завершении приложения
    db.close_all()
    sys.exit(exit_code)