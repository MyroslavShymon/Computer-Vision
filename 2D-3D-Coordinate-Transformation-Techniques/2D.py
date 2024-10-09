from graphics import *  # Імпорт бібліотеки для графіки
import time  # Імпорт модуля для роботи з часом
import numpy as np  # Імпорт бібліотеки для роботи з масивами
import math as mt  # Імпорт модуля для роботи з математичними функціями

# Параметри вікна
xw, yw = 500, 500  # Розміри вікна (ширина та висота)
dx, dy = 25, 25  # Розміри переміщення по осі x і y
width, height = 80, 40  # Розміри прямокутника
win = GraphWin("2-D проекції в бібліотеці graphics ПЕРЕНОС З РУХОМ матрицями", xw, yw)  # Створення вікна
win.setBackground('white')  # Встановлення білого фону

def move_rectangle(win_width, win_height, rect_width, rect_height, dx, dy, sleep_time):
    # Початкові координати прямокутника
    x1 = 0  # Ліва координата верхнього кута
    y1 = win_height - rect_height  # Моя координата верхнього кута
    x2 = x1 + rect_width  # Права координата верхнього кута
    y2 = y1 + rect_height  # Нижня координата верхнього кута

    # Малювання початкового прямокутника
    obj = Rectangle(Point(x1, y1), Point(x2, y2))  # Створення прямокутника
    obj.draw(win)  # Відображення прямокутника

    # Циклічний блок матричних перетворень типу ПЕРЕНОС
    stop = int(win_width / dx)  # Кількість кроків переміщення
    for i in range(stop):
        time.sleep(sleep_time)  # Затримка зображення на екрані
        obj.setOutline("white")  # Замальовування попереднього прямокутника під фон
        obj.undraw()  # Сховати попередній прямокутник

        # Визначення нових координат
        a = np.array([[x1, y1, 1]])  # Вектор координат з однією додатковою вимірністю
        f = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])  # Переміщення по діагоналі
        ft = f.T  # Транспонування матриці переміщення
        total = a.dot(ft)  # Обчислення нових координат
        x1, y1 = total[0, 0], total[0, 1]  # Оновлення координат

        x2 = x1 + rect_width  # Оновлення правої координати
        y2 = y1 + rect_height  # Оновлення нижньої координати

        # Відновлення прямокутника з новими координатами
        obj = Rectangle(Point(x1, y1), Point(x2, y2))  # Створення нового прямокутника
        obj.draw(win)  # Відображення нового прямокутника

    # Підсумкова позиція
    obj.setOutline("white")  # Замальовування під фон
    obj.undraw()  # Сховати попередній прямокутник

    obj = Rectangle(Point(x1, y1), Point(x2, y2))  # Створення підсумкового прямокутника
    obj.draw(win)  # Відображення підсумкового прямокутника

def animate_rectangle(win_width, win_height, dx, dy, width, height, rotation_angle, rotation_direction=1):
    win = GraphWin("2-D проекції в бібліотеці graphics ПЕРЕНОС обертання З РУХОМ матрицями", win_width, win_height)  # Створення нового вікна
    win.setBackground('white')  # Встановлення білого фону

    # Формування прямокутника по 4 точкам
    x1 = dx  # Ліва координата верхнього кута
    y1 = win_height - dy  # Моя координата верхнього кута
    x2 = dx + width  # Права координата верхнього кута
    y2 = win_height - dy  # Моя координата верхнього кута
    x3 = dx + width  # Права координата нижнього кута
    y3 = win_height - dy - height  # Моя координата нижнього кута
    x4 = dx  # Ліва координата нижнього кута
    y4 = win_height - dy - height  # Моя координата нижнього кута

    # Перенос
    def translate(x, y):
        return np.array([[x, y, 1]]).dot(np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]]).T)[0, :2]  # Обчислення нових координат після переносу

    # Обертання
    def rotate(x, y, angle):
        angle_rad = mt.radians(angle)  # Перетворення кута в радіани
        return np.array([[x, y, 1]]).dot(np.array([[mt.cos(angle_rad), -mt.sin(angle_rad), 0],
                                                    [mt.sin(angle_rad), mt.cos(angle_rad), 0],
                                                    [0, 0, 1]]).T)[0, :2]  # Обчислення нових координат після обертання

    obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))  # Створення полігону з чотирьох точок
    obj.draw(win)  # Відображення полігону
    obj.setOutline("white")  # Замальовування контуру під фон

    stop = win_width / dx * 6  # Кількість кроків анімації
    ii = int(float(stop))  # Преобразування у ціле число

    for i in range(ii):
        time.sleep(0.1)  # Затримка між кроками
        obj.setOutline("white")  # Замальовування контуру під фон
        obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))  # Створення нового полігону

        # Циклічний блок матричних перетворень типу ПЕРЕНОС
        x1, y1 = translate(x1, y1)  # Перенос нових координат
        x2, y2 = translate(x2, y2)  # Перенос нових координат
        x3, y3 = translate(x3, y3)  # Перенос нових координат
        x4, y4 = translate(x4, y4)  # Перенос нових координат

        # Циклічний поворот
        rotation_step = rotation_direction * (rotation_angle * (win_width / dx) * 0.65) / ii  # Обчислення куту повороту
        x1, y1 = rotate(x1, y1, rotation_step)  # Обертання координат
        x2, y2 = rotate(x2, y2, rotation_step)  # Обертання координат
        x3, y3 = rotate(x3, y3, rotation_step)  # Обертання координат
        x4, y4 = rotate(x4, y4, rotation_step)  # Обертання координат

        obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))  # Створення нового полігону з оберненими координатами
        obj.draw(win)  # Відображення нового полігону

    # Чекати кліку миші перед закриттям вікна
    win.getMouse()  # Очікування натискання миші
    win.close()  # Закриття вікна

move_rectangle(xw, yw, width, height, dx, dy, 0.1)  # Виклик функції для переміщення прямокутника
win.getMouse()  # Очікування натискання миші
win.close()  # Закриття вікна

# Виклик функції для обертання за годинниковою стрілкою
animate_rectangle(xw, yw, dx, dy, width, height, rotation_angle=50, rotation_direction=1)

# Виклик функції для обертання проти годинникової стрілки
animate_rectangle(xw, yw, dx, dy, width, height, rotation_angle=300, rotation_direction=-1)

win.getMouse()
win.close()