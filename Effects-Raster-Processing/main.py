from PIL import Image, ImageEnhance
import numpy as np
import os

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def convert_to_grayscale(image):
    return image.convert("L")


def create_negative(image):
    return Image.eval(image, lambda p: 255 - p)


def apply_sepia(image):
    sepia_filter = np.array([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])
    img_array = np.array(image)
    sepia_image = np.dot(img_array[..., :3], sepia_filter.T)
    sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
    return Image.fromarray(sepia_image)


def gradient_effect(image, direction='diagonal'):
    width, height = image.size
    img_array = np.array(image)

    if direction == 'diagonal':
        for i in range(width):
            for j in range(height):
                img_array[j, i] = img_array[j, i] * (i / width)

    elif direction == 'from_center':
        center_x, center_y = width // 2, height // 2
        for i in range(width):
            for j in range(height):
                distance = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
                factor = 1 - min(distance / (width // 2), 1)
                img_array[j, i] = img_array[j, i] * factor

    elif direction == 'to_center':
        center_x, center_y = width // 2, height // 2
        for i in range(width):
            for j in range(height):
                distance = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
                factor = min(distance / (width // 2), 1)
                img_array[j, i] = img_array[j, i] * (1 - factor)

    return Image.fromarray(img_array)


def save_image(image, filename):
    """Зберегти зображення в заданий файл."""
    image.save(filename)
    print(f"Зображення збережено: {filename}")


def main():
    # Завантаження зображення
    image_path = 'person.jpg'

    if not os.path.isfile(image_path):
        print(f"Файл '{image_path}' не знайдено.")
        return

    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Помилка при відкритті зображення: {e}")
        return

    # Зміна яскравості
    try:
        bright_image = adjust_brightness(image, 1.5)
        save_image(bright_image, 'bright_person.jpg')
    except Exception as e:
        print(f"Помилка при зміні яскравості: {e}")

    # Конвертація в градації сірого
    try:
        gray_image = convert_to_grayscale(image)
        save_image(gray_image, 'gray_person.jpg')
    except Exception as e:
        print(f"Помилка при конвертації в градації сірого: {e}")

    # Створення негативу
    try:
        negative_image = create_negative(image)
        save_image(negative_image, 'negative_person.jpg')
    except Exception as e:
        print(f"Помилка при створенні негативу: {e}")

    # Застосування серпії
    try:
        sepia_image = apply_sepia(image)
        save_image(sepia_image, 'sepia_person.jpg')
    except Exception as e:
        print(f"Помилка при застосуванні серпії: {e}")

    # Застосування ефекту градієнта
    try:
        gradient_image_diagonal = gradient_effect(image, 'diagonal')
        save_image(gradient_image_diagonal, 'gradient_diagonal_person.jpg')

        gradient_image_from_center = gradient_effect(image, 'from_center')
        save_image(gradient_image_from_center, 'gradient_from_center_person.jpg')

        gradient_image_to_center = gradient_effect(image, 'to_center')
        save_image(gradient_image_to_center, 'gradient_to_center_person.jpg')
    except Exception as e:
        print(f"Помилка при застосуванні градієнтного ефекту: {e}")


if __name__ == "__main__":
    main()
