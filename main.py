import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,
                               QWidget, QHBoxLayout, QScrollArea, QPushButton,
                               QMessageBox)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
from database import Database


def calculate_discount(old_price, new_price):
    if old_price == 0:
        return 0
    return (old_price - new_price) / old_price * 100


def calculate_price(product_id, old_price):
    return float(old_price) * 0.8


def create_card(product):
    card = QWidget()
    card.setObjectName("productCard")
    card.setStyleSheet("""
        #productCard {
            border: 1px solid #000000;
            border-radius: 4px;
            background-color: #FFFFFF;
        }
    """)

    main_layout = QHBoxLayout(card)
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(15)

    image_label = QLabel()
    image_label.setFixedSize(100, 100)
    image_label.setAlignment(Qt.AlignCenter)
    image_label.setStyleSheet("border: 1px solid #000000;")

    product_id = product[0]
    name = product[1] if product[1] else "Наименование"
    old_price = float(product[2]) if product[2] else 0.0
    file_name = product[3]
    manufacturer = product[4] if product[4] else "Неизвестный производитель"

    if file_name:
        image_path = os.path.join("images", file_name)
    else:
        image_path = os.path.join("resources", "picture.png")

    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        image_label.setText("IMG")
    else:
        image_label.setPixmap(
            pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
    main_layout.addWidget(image_label)

    text_layout = QVBoxLayout()
    text_layout.setSpacing(5)
    
    text_style = "font-size: 14px; border: none; color: #000000;"

    title = QLabel(f"<b>{manufacturer} | {name}</b>")
    title.setStyleSheet(text_style)

    category_label = QLabel(f"Категория: Садовый инвентарь")
    category_label.setStyleSheet(text_style)

    quantity_label = QLabel(f"Количество: 1 шт.")
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

    # --- БЛОК С ЦЕНАМИ ---
    new_price = calculate_price(product_id, old_price)
    discount = calculate_discount(old_price, new_price)

    price_layout = QVBoxLayout()
    price_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
    price_layout.setSpacing(2)

    # 1. Старая цена (перечеркнутая и красная)
    old_price_label = QLabel(f"<s>{old_price:.2f} ₽</s>")
    old_price_label.setAlignment(Qt.AlignRight)
    old_price_label.setStyleSheet("color: red; font-size: 14px; border: none;")

    # 2. Итоговая цена (ЧЁРНАЯ и жирная)
    new_price_label = QLabel(f"<b>{new_price:.2f} ₽</b>")
    new_price_label.setAlignment(Qt.AlignRight)
    new_price_label.setStyleSheet("color: black; font-weight: bold; font-size: 16px; border: none;")

    # Скрываем старую цену, если скидки нет
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

        self.setStyleSheet("""
            QMainWindow { background-color: #FFFFFF; }
            QLabel { font-family: Calibri; }
            #HeaderLabel { font-size: 28px; font-weight: bold; color: #2c3e50; margin: 20px; }
            QPushButton { padding: 10px; margin: 5px; font-size: 14px; background-color: #70B2AF; color: white; border: none; border-radius: 5px; }
            QPushButton:hover { background-color: #5a9a97; }
        """)

        self.setup_ui()
        self.setup_role_interface()

    def setup_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        header = QHBoxLayout()

        logo_header = QLabel()
        pixmap_logo = QPixmap("resources/logo.png")
        if not pixmap_logo.isNull():
            logo_header.setPixmap(pixmap_logo.scaledToHeight(50, Qt.SmoothTransformation))
        header.addWidget(logo_header)

        header.addStretch()

        name_text = f"ФИО: {self.full_name}" if self.full_name else "ФИО: —"
        name_label = QLabel(name_text)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        header.addWidget(name_label)

        self.logout_button = QPushButton("Выход")
        self.logout_button.clicked.connect(self.logout)
        header.addWidget(self.logout_button)

        main_layout.addLayout(header)

        title = QLabel("Сад и огород — Каталог")
        title.setObjectName("HeaderLabel")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self.order_button = QPushButton("Оформить заказ")
        self.manager_button = QPushButton("Заказы (менеджер)")
        self.admin_button = QPushButton("Админ-панель")

        main_layout.addWidget(self.order_button)
        main_layout.addWidget(self.manager_button)
        main_layout.addWidget(self.admin_button)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #FFFFFF")

        container = QWidget()
        list_layout = QVBoxLayout(container)
        list_layout.setAlignment(Qt.AlignTop)

        self.products = self.db.get_products()
        if not self.products:
            list_layout.addWidget(QLabel("Товары не найдены."))
        else:
            for product in self.products:
                list_layout.addWidget(create_card(product))

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def setup_role_interface(self):
        self.order_button.hide()
        self.manager_button.hide()
        self.admin_button.hide()

        if self.role_id == 1:
            self.admin_button.show()
            self.manager_button.show()
        elif self.role_id == 2:
            self.manager_button.show()
        elif self.role_id == 3:
            self.order_button.show()

    def logout(self):
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
        self.db.close_all()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = Database()

    from window_login import LoginWindow
    login_window = LoginWindow(db)
    login_window.show()

    sys.exit(app.exec())