import os

picture_exists = os.path.exists("resources/picture.png")
print(f"resources/picture.png: {'Да' if picture_exists else 'Нет'}")

image_exists = os.path.exists("resources/IMG_29_001.png")
print(f"resources/IMG_29_001.png: {'Да' if image_exists else 'Нет'}")