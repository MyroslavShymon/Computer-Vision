from PIL import Image, ImageEnhance
import numpy as np
import os

def adjust_brightness(image, factor):
    # Змінює яскравість зображення на заданий коефіцієнт
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def convert_to_grayscale(image):
    # Перетворює зображення в градації сірого
    return image.convert("L")


def create_negative(image):
    # Створює негатив зображення, інвертуючи кольори
    return Image.eval(image, lambda p: 255 - p)


def apply_sepia(image):
    # Застосовує сепійний фільтр до зображення, щоб надати йому теплі відтінки
    sepia_filter = np.array([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])
    img_array = np.array(image)
    sepia_image = np.dot(img_array[..., :3], sepia_filter.T)  # Використовує матричне множення для зміни кольору
    sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)  # Обмежує значення кольорів в діапазоні [0, 255]
    return Image.fromarray(sepia_image)


def gradient_effect(image, direction='diagonal'):
    # Застосовує градієнтний ефект до зображення в залежності від напрямку
    width, height = image.size
    img_array = np.array(image)

    if direction == 'diagonal':
        # Застосування діагонального градієнта
        for i in range(width):
            for j in range(height):
                img_array[j, i] = img_array[j, i] * (i / width)  # Змінює яскравість в залежності від позиції по осі X

    elif direction == 'from_center':
        # Градієнт від центру зображення
        center_x, center_y = width // 2, height // 2
        for i in range(width):
            for j in range(height):
                distance = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)  # Відстань до центру
                factor = 1 - min(distance / (width // 2), 1)  # Визначення коефіцієнта на основі відстані
                img_array[j, i] = img_array[j, i] * factor  # Зменшення яскравості

    elif direction == 'to_center':
        # Градієнт до центру зображення
        center_x, center_y = width // 2, height // 2
        for i in range(width):
            for j in range(height):
                distance = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)  # Відстань до центру
                factor = min(distance / (width // 2), 1)  # Визначення коефіцієнта на основі відстані
                img_array[j, i] = img_array[j, i] * (1 - factor)  # Збільшення яскравості

    return Image.fromarray(img_array)  # Повертає оброблене зображення


def save_image(image, filename):
    """Зберігає зображення в заданий файл."""
    image.save(filename)
    print(f"Зображення збережено: {filename}")  # Підтвердження про збереження


def main():
    # Завантажує зображення з диска
    image_path = 'person.jpg'
    sepia_image = 0  # Ініціалізація змінної для зображення в сепії

    if not os.path.isfile(image_path):
        print(f"Файл '{image_path}' не знайдено.")  # Перевірка наявності файлу
        return

    try:
        image = Image.open(image_path)  # Відкриття зображення
    except Exception as e:
        print(f"Помилка при відкритті зображення: {e}")  # Обробка помилки при відкритті
        return

    # Зміна яскравості
    try:
        bright_image = adjust_brightness(image, 1.5)  # Збільшення яскравості
        save_image(bright_image, 'bright_person.jpg')  # Збереження обробленого зображення
    except Exception as e:
        print(f"Помилка при зміні яскравості: {e}")  # Обробка помилки

    # Конвертація в градації сірого
    try:
        gray_image = convert_to_grayscale(image)  # Перетворення в сірі відтінки
        save_image(gray_image, 'gray_person.jpg')  # Збереження
    except Exception as e:
        print(f"Помилка при конвертації в градації сірого: {e}")  # Обробка помилки

    # Створення негативу
    try:
        negative_image = create_negative(image)  # Створення негативного зображення
        save_image(negative_image, 'negative_person.jpg')  # Збереження
    except Exception as e:
        print(f"Помилка при створенні негативу: {e}")  # Обробка помилки

    # Застосування сепії
    try:
        sepia_image = apply_sepia(image)  # Застосування сепійного фільтру
        save_image(sepia_image, 'sepia_person.jpg')  # Збереження
    except Exception as e:
        print(f"Помилка при застосуванні сепії: {e}")  # Обробка помилки

    # Застосування ефекту градієнта
    try:
        gradient_image_diagonal = gradient_effect(image, 'diagonal')  # Діагональний градієнт
        save_image(gradient_image_diagonal, 'gradient_diagonal_person.jpg')  # Збереження

        gradient_image_from_center = gradient_effect(image, 'from_center')  # Градієнт від центру
        save_image(gradient_image_from_center, 'gradient_from_center_person.jpg')  # Збереження

        gradient_image_to_center = gradient_effect(image, 'to_center')  # Градієнт до центру
        save_image(gradient_image_to_center, 'gradient_to_center_person.jpg')  # Збереження
    except Exception as e:
        print(f"Помилка при застосуванні градієнтного ефекту: {e}")  # Обробка помилки

    # Застосування градієнтного ефекту до сепії
    try:
        gradient_sepia_image_image_diagonal = gradient_effect(sepia_image, 'diagonal')  # Діагональний градієнт до сепії
        save_image(gradient_sepia_image_image_diagonal, 'sepia_gradient_diagonal_person.jpg')  # Збереження

        gradient_sepia_image_from_center = gradient_effect(sepia_image, 'from_center')  # Градієнт від центру до сепії
        save_image(gradient_sepia_image_from_center, 'sepia_gradient_from_center_person.jpg')  # Збереження

        gradient_sepia_image_to_center = gradient_effect(sepia_image, 'to_center')  # Градієнт до центру до сепії
        save_image(gradient_sepia_image_to_center, 'sepia_gradient_to_center_person.jpg')  # Збереження
    except Exception as e:
        print(f"Помилка при застосуванні градієнтного ефекту до сепії: {e}")  # Обробка помилки


if __name__ == "__main__":
    main()  # Запуск основної програми