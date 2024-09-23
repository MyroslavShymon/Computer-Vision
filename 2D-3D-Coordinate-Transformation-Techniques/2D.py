from graphics import *
import time
import numpy as np
import math as mt


# Параметри вікна
xw, yw = 500, 500
dx, dy = 25, 25  # Розміри переміщення по осі x і y
width, height = 80, 40  # Розміри прямокутника
win = GraphWin("2-D проекции в библиотеке graphics ПЕРЕНОС З РУХОМ матрицями", xw, yw)
win.setBackground('white')

def move_rectangle(win_width, win_height, rect_width, rect_height, dx, dy, sleep_time):
    # Початкові координати прямокутника
    x1 = 0
    y1 = win_height - rect_height
    x2 = x1 + rect_width
    y2 = y1 + rect_height

    # Малювання початкового прямокутника
    obj = Rectangle(Point(x1, y1), Point(x2, y2))
    obj.draw(win)

    # Циклічний блок матричних перетворень типу ПЕРЕНОС
    stop = int(win_width / dx)
    for i in range(stop):
        time.sleep(sleep_time)  # Затримка зображення на екрані
        obj.setOutline("white")  # Замальовування попереднього прямокутника під фон
        obj.undraw()  # Сховати попередній прямокутник

        # Визначення нових координат
        a = np.array([[x1, y1, 1]])
        f = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])  # Переміщення по діагоналі
        ft = f.T
        total = a.dot(ft)
        x1, y1 = total[0, 0], total[0, 1]

        x2 = x1 + rect_width
        y2 = y1 + rect_height

        # Відновлення прямокутника з новими координатами
        obj = Rectangle(Point(x1, y1), Point(x2, y2))
        obj.draw(win)

    # Підсумкова позиція
    obj.setOutline("white")
    obj.undraw()

    obj = Rectangle(Point(x1, y1), Point(x2, y2))
    obj.draw(win)

def animate_rectangle(win_width, win_height, dx, dy, width, height, rotation_angle, rotation_direction=1):
    win = GraphWin("2-D проекции в библиотеке graphics ПЕРЕНОС обертання З РУХОМ матрицями", win_width, win_height)
    win.setBackground('white')

    # Формування прямокутника по 4 точкам
    x1 = dx
    y1 = win_height - dy
    x2 = dx + width
    y2 = win_height - dy
    x3 = dx + width
    y3 = win_height - dy - height
    x4 = dx
    y4 = win_height - dy - height

    # Перенос
    def translate(x, y):
        return np.array([[x, y, 1]]).dot(np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]]).T)[0, :2]

    # Обертання
    def rotate(x, y, angle):
        angle_rad = mt.radians(angle)
        return np.array([[x, y, 1]]).dot(np.array([[mt.cos(angle_rad), -mt.sin(angle_rad), 0],
                                                    [mt.sin(angle_rad), mt.cos(angle_rad), 0],
                                                    [0, 0, 1]]).T)[0, :2]

    obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
    obj.draw(win)
    obj.setOutline("white")

    stop = win_width / dx * 6
    ii = int(float(stop))

    for i in range(ii):
        time.sleep(0.1)
        obj.setOutline("white")
        obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))

        # Циклічний блок матричних перетворень типу ПЕРЕНОС
        x1, y1 = translate(x1, y1)
        x2, y2 = translate(x2, y2)
        x3, y3 = translate(x3, y3)
        x4, y4 = translate(x4, y4)

        # Циклічний поворот
        rotation_step = rotation_direction * (rotation_angle * (win_width / dx) * 0.65) / ii
        x1, y1 = rotate(x1, y1, rotation_step)
        x2, y2 = rotate(x2, y2, rotation_step)
        x3, y3 = rotate(x3, y3, rotation_step)
        x4, y4 = rotate(x4, y4, rotation_step)

        obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
        obj.draw(win)

    # Чекати кліку миші перед закриттям вікна
    win.getMouse()
    win.close()

move_rectangle(xw, yw, width, height, dx, dy, 0.1)
win.getMouse()
win.close()

# Виклик функції для обертання за годинниковою стрілкою
animate_rectangle(xw, yw, dx, dy, width, height, rotation_angle=50, rotation_direction=1)

# Виклик функції для обертання проти годинникової стрілки
animate_rectangle(xw, yw, dx, dy, width, height, rotation_angle=300, rotation_direction=-1)

win.getMouse()
win.close()