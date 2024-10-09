# --------------------- 3D - геометричні перетворення ---------------------------
# Завдання:
# Синтез 3D об'єкту та його геометричне перетворення:
# 1. Синтез піраміди геометричним методом - матриця;
# 2. Переміщення піраміди до центру екрану;
# 3. Обертання навколо пласких координатних вісій;
# 4. Ортогональна проекція на плаский екран - елюзія 3D об'єкту.

from graphics import *
import numpy as np
import math as mt

#---------------------------------- координати піраміди ------------------------------------
xw = 600  # Ширина вікна
yw = 600  # Висота вікна
st = 300  # Довжина сторони основи піраміди

# Визначення вершин піраміди: A, B, C, D - основа; E - вершина
Pyramid = np.array([
    [0, 0, 0, 1],    # A (верхня ліва точка основи)
    [st, 0, 0, 1],   # B (верхня права точка основи)
    [st, st, 0, 1],  # C (нижня права точка основи)
    [0, st, 0, 1],   # D (нижня ліва точка основи)
    [st/2, st/2, st, 1]  # E (вершина піраміди)
])  # Піраміда задається у вигляді масиву точок
print('enter matrix')
print(Pyramid)

#--------------------------------- функція проекції на xy, z=0 -------------------------------------
def ProjectXY(Figure):
    # Матриця проекції на плоскість XY, координата Z завжди 0
    f = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 1]])  # Матриця проекції
    ft = f.T  # Транспонування матриці
    Prxy = Figure.dot(ft)  # Виконання множення матриць
    print('проекція на ху')
    print(Prxy)  # Вивід результату проекції
    return Prxy  # Повертаємо результат проекції

#-------------------------------------------- зміщення ----------------------------------------------
def ShiftXYZ(Figure, l, m, n):
    # Матриця для зміщення точки у 3D просторі
    f = np.array([[1, 0, 0, l],
                   [0, 1, 0, m],
                   [0, 0, 1, n],
                   [1, 0, 0, 1]])  # Матриця трансформації
    ft = f.T  # Транспонування матриці
    Prxy = Figure.dot(ft)  # Виконання множення матриць
    print('зміщення')
    print(Prxy)  # Вивід результату зміщення
    return Prxy  # Повертаємо результат зміщення

#-------------------------------------------- обертання коло х----------------------------------------
def insertX(Figure, TetaG):
    # Конвертуємо градуси в радіани для обертання
    TetaR = (3/14 * TetaG) / 180
    # Матриця обертання навколо осі X
    f = np.array([[1, 0, 0, 0],
                   [0, mt.cos(TetaR), mt.sin(TetaR), 0],
                   [0, -mt.sin(TetaR), mt.cos(TetaR), 0],
                   [0, 0, 0, 1]])
    ft = f.T  # Транспонування матриці
    Prxy = Figure.dot(ft)  # Виконання множення матриць
    print('обертання коло х')
    print(Prxy)  # Вивід результату обертання
    return Prxy  # Повертаємо результат обертання

#-------------------------------------------- аксонометрія ----------------------------------------------
def dimetri(Figure, TetaG1, TetaG2):
    # Конвертуємо градуси в радіани для першого обертання
    TetaR1 = (3/14 * TetaG1) / 180
    # Матриця обертання навколо осі Y
    f1 = np.array([[mt.cos(TetaR1), 0, -mt.sin(TetaR1), 0],
                    [0, 1, 0, 0],
                    [mt.sin(TetaR1), 0, mt.cos(TetaR1), 1],
                    [0, 0, 0, 0]])
    ft1 = f1.T  # Транспонування матриці
    Prxy1 = Figure.dot(ft1)  # Виконання множення матриць для першого обертання

    # Конвертуємо градуси в радіани для другого обертання
    TetaR2 = (3/14 * TetaG2) / 180
    # Матриця обертання навколо осі Z
    f2 = np.array([[1, 0, 0, 0],
                    [0, mt.cos(TetaR2), mt.sin(TetaR2), 0],
                    [0, -mt.sin(TetaR2), mt.cos(TetaR2), 0],
                    [0, 0, 0, 1]])
    ft2 = f2.T  # Транспонування матриці
    Prxy2 = Prxy1.dot(ft2)  # Виконання множення матриць для другого обертання
    print('dimetri')
    print(Prxy2)  # Вивід результату аксонометрії
    return Prxy2  # Повертаємо результат аксонометрії

#-------------------------------------- функція побудови піраміди -----------------------------
def PyramidWiz(Prxy, contour_color):
    # Отримуємо координати вершин піраміди після проекції
    Ax, Ay = Prxy[0, 0], Prxy[0, 1]
    Bx, By = Prxy[1, 0], Prxy[1, 1]
    Cx, Cy = Prxy[2, 0], Prxy[2, 1]
    Dx, Dy = Prxy[3, 0], Prxy[3, 1]
    Ex, Ey = Prxy[4, 0], Prxy[4, 1]

    # Будуємо трикутники для піраміди
    obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Ex, Ey))  # Трикутник ABE
    obj.setOutline(contour_color)  # Задаємо колір контуру
    obj.draw(win)  # Відображення трикутника

    obj = Polygon(Point(Bx, By), Point(Cx, Cy), Point(Ex, Ey))  # Трикутник BCE
    obj.setOutline(contour_color)  # Задаємо колір контуру
    obj.draw(win)  # Відображення трикутника

    obj = Polygon(Point(Cx, Cy), Point(Dx, Dy), Point(Ex, Ey))  # Трикутник CDE
    obj.setOutline(contour_color)  # Задаємо колір контуру
    obj.draw(win)  # Відображення трикутника

    obj = Polygon(Point(Dx, Dy), Point(Ax, Ay), Point(Ex, Ey))  # Трикутник DAE
    obj.setOutline(contour_color)  # Задаємо колір контуру
    obj.draw(win)  # Відображення трикутника

    obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy))  # Основа ABCD
    obj.setOutline(contour_color)  # Задаємо колір контуру
    obj.draw(win)  # Відображення основи

#-------------------------------------------- побудова піраміди -----------------------------
# Створюємо вікно графічного інтерфейсу для відображення моделі піраміди
win = GraphWin("3-D модель піраміди, аксонометрічна проекція на ХУ", xw, yw)
win.setBackground('white')  # Задаємо білий фон для вікна

# Встановлюємо розміри вікна
xw = 600  # Ширина вікна
yw = 600  # Висота вікна
st = 50   # Величина, що визначає розміри піраміди

# Параметри для повороту піраміди
TetaG1 = 0     # Кут повороту навколо осі X
TetaG2 = -90   # Кут повороту навколо осі Y

# Обчислюємо координати для зміщення піраміди
l = (xw / 3) - st  # Відстань зміщення по осі X
m = (yw / 3) - st  # Відстань зміщення по осі Y
n = m               # Відстань зміщення по осі Z

# Pyramid1=ShiftXYZ (Pyramid, l, m, n)  # Зміщення піраміди
# Pyramid2=dimetri (Pyramid1, TetaG1, TetaG2)  # Поворот піраміди
# Pyramid2=insertX (Pyramid1, TetaG1)  # Вставка нових координат
# Prxy3=ProjectXY (Pyramid2)  # Проекція на площину XY
Prxy3 = Pyramid  # В даному випадку використовуємо початкову піраміду без змін

# Викликаємо функцію для малювання піраміди з червоним контуром
PyramidWiz(Prxy3, 'red')
win.getMouse()  # Чекаємо натискання миші
win.close()  # Закриваємо вікно

# Створюємо нове вікно для відображення піраміди з новими параметрами
win = GraphWin("3-D модель піраміди, аксонометрічна проекція на ХУ", xw, yw)
win.setBackground('white')  # Білий фон

# Повторно задаємо параметри
xw = 600
yw = 600
st = 50
TetaG1 = 0
TetaG2 = -90
l = (xw / 3) - st
m = (yw / 3) - st
n = m

# Зміщуємо піраміду
Pyramid1 = ShiftXYZ(Pyramid, l, m, n)
# Pyramid2=dimetri (Pyramid1, TetaG1, TetaG2)  # Поворот піраміди
Pyramid2 = insertX(Pyramid1, TetaG1)  # Вставка нових координат
Prxy3 = ProjectXY(Pyramid2)  # Проекція на площину XY

# Малюємо піраміду з синім контуром
PyramidWiz(Prxy3, 'blue')
win.getMouse()  # Чекаємо натискання миші
win.close()  # Закриваємо вікно

# Створюємо ще одне вікно для нової моделі піраміди
win = GraphWin("3-D модель піраміди оберт коло Х аксонометрічна проекція на ХУ", xw, yw)
win.setBackground('white')  # Білий фон

# Повторно задаємо параметри
xw = 600
yw = 600
st = 50
TetaG1 = 180  # Поворот навколо осі X
TetaG2 = -90  # Поворот навколо осі Y
l = (xw / 3) - st
m = (yw / 3) - st
n = m

# Зміщуємо піраміду
Pyramid1 = ShiftXYZ(Pyramid, l, m, n)
# Pyramid2=dimetri (Pyramid1, TetaG1, TetaG2)  # Поворот піраміди
Pyramid2 = insertX(Pyramid1, TetaG1)  # Вставка нових координат
Prxy3 = ProjectXY(Pyramid2)  # Проекція на площину XY

# Малюємо піраміду з зеленим контуром
PyramidWiz(Prxy3, 'green')
win.getMouse()  # Чекаємо натискання миші
win.close()  # Закриваємо вікно

# Створюємо ще одне вікно для обертання піраміди
win = GraphWin("3-D піраміди діметричний оберт навколо Х та У аксонометрічна проекція на ХУ", xw, yw)
win.setBackground('white')  # Білий фон

# Повторно задаємо параметри
xw = 600
yw = 600
st = 50
TetaG1 = 180  # Поворот навколо осі X
TetaG2 = -90  # Поворот навколо осі Y
l = (xw / 3) - st
m = (yw / 3) - st
n = m

# Зміщуємо піраміду
Pyramid1 = ShiftXYZ(Pyramid, l, m, n)
Pyramid2 = dimetri(Pyramid1, TetaG1, TetaG2)  # Поворот піраміди
Prxy3 = ProjectXY(Pyramid2)  # Проекція на площину XY

# Малюємо піраміду з жовтим контуром
PyramidWiz(Prxy3, 'yellow')
win.getMouse()  # Чекаємо натискання миші
win.close()  # Закриваємо вікно

import matplotlib.pyplot as plt  # Імпорт бібліотеки для візуалізації
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # Імпорт колекції полігонів для 3D
import matplotlib.animation as animation  # Імпорт бібліотеки для анімації

#---------------------------------- Перший приклад використання matplotlib ------------------------------------
# Імпорт полігонів для 3D

# Створення фігури для графіку
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # Додаємо 3D підграфік
ax.set_title('3D Pyramid')  # Заголовок графіка

# Визначення вершин піраміди: A, B, C, D - основа; E - вершина
vertices = np.array([[0, 0, 0],       # Вершина A
                     [st, 0, 0],     # Вершина B
                     [st, st, 0],    # Вершина C
                     [0, st, 0],     # Вершина D
                     [st / 2, st / 2, st]])  # Вершина E

# Визначення грані піраміди
faces = [[vertices[j] for j in [0, 1, 4]],  # Грань ABE
         [vertices[j] for j in [1, 2, 4]],  # Грань BCE
         [vertices[j] for j in [2, 3, 4]],  # Грань CDE
         [vertices[j] for j in [3, 0, 4]],  # Грань DAE
         [vertices[j] for j in range(4)]]   # Основна грань ABCD

# Створення полігонів з визначених граней
ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

# Встановлення меж графіку
ax.set_xlabel('X axis')  # Підпис осі X
ax.set_ylabel('Y axis')  # Підпис осі Y
ax.set_zlabel('Z axis')  # Підпис осі Z
ax.set_xlim(0, st)  # Межі осі X
ax.set_ylim(0, st)  # Межі осі Y
ax.set_zlim(0, st)  # Межі осі Z
plt.show()  # Відображення графіка


#---------------------------------- Другий приклад використання matplotlib ------------------------------------
#---------------------------------- координати піраміди ------------------------------------
def create_pyramid():
    # Створює масив вершин піраміди
    # Піраміда визначається 5-ма точками:
    # 4 точки для основи (A, B, C, D) та 1 точка для вершини (E)
    return np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0.5, 0.5, 1]])

#--------------------------------- проекція на XY -----------------------------------------
def project_onto_xy(points):
    # Повертає тільки X і Y координати вершин піраміди, ігноруючи Z
    return points[:, :2]

#---------------------------------- зміщення ----------------------------------------------
def translate(points, tx, ty, tz):
    # Створює матрицю зсуву для переміщення піраміди
    translation_matrix = np.array([[1, 0, 0, tx],  # Зсув по X
                                    [0, 1, 0, ty],  # Зсув по Y
                                    [0, 0, 1, tz],  # Зсув по Z
                                    [0, 0, 0, 1]])  # Гомогенна координата
    # Розширює координати піраміди до 4D, щоб застосувати матрицю зсуву
    extended_points = np.hstack((points, np.ones((points.shape[0], 1))))  # розширення до 4D
    # Повертає нові координати після зсуву
    return (extended_points.dot(translation_matrix.T))[:, :3]

#---------------------------------- обертання ----------------------------------------------
def rotate(points, angle, axis):
    # Обертає піраміду навколо заданої осі на вказаний кут
    theta = np.radians(angle)  # Перетворює градуси в радіани
    if axis == 'x':
        # Матриця обертання навколо осі X
        rotation_matrix = np.array([[1, 0, 0],
                                     [0, np.cos(theta), -np.sin(theta)],
                                     [0, np.sin(theta), np.cos(theta)]])
    elif axis == 'y':
        # Матриця обертання навколо осі Y
        rotation_matrix = np.array([[np.cos(theta), 0, np.sin(theta)],
                                     [0, 1, 0],
                                     [-np.sin(theta), 0, np.cos(theta)]])
    elif axis == 'z':
        # Матриця обертання навколо осі Z
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                     [np.sin(theta), np.cos(theta), 0],
                                     [0, 0, 1]])
    # Повертає нові координати після обертання
    return points.dot(rotation_matrix.T)

#---------------------------------- анімація ----------------------------------------------
def animate(i):
    # Очищає осі перед кожним кадром анімації
    ax.clear()
    ax.set_title("Анімація обертання піраміди")  # Назва графіка
    ax.set_xlabel('X')  # Позначення осі X
    ax.set_ylabel('Y')  # Позначення осі Y
    ax.set_zlabel('Z')  # Позначення осі Z

    # Обертання піраміди навколо осі Y на kут, що залежить від кадру
    rotated_pyramid = rotate(pyramid, i * 5, 'y')  # обертання навколо осі Y
    projected_pyramid = project_onto_xy(rotated_pyramid)  # Проекція на XY

    # Визначає вершини для малювання піраміди
    vertices = [
        [rotated_pyramid[0], rotated_pyramid[1], rotated_pyramid[2], rotated_pyramid[3]],  # основа
        [rotated_pyramid[0], rotated_pyramid[1], rotated_pyramid[4]],  # бокові грані
        [rotated_pyramid[1], rotated_pyramid[2], rotated_pyramid[4]],
        [rotated_pyramid[2], rotated_pyramid[3], rotated_pyramid[4]],
        [rotated_pyramid[3], rotated_pyramid[0], rotated_pyramid[4]]
    ]
    # Додає полігональні грані до 3D-осей
    ax.add_collection3d(Poly3DCollection(vertices, facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.5))

    # Встановлення меж графіка
    ax.set_xlim([-2, 2])  # Межі осі X
    ax.set_ylim([-2, 2])  # Межі осі Y
    ax.set_zlim([-0.5, 2])  # Межі осі Z

#---------------------------------- основний код ----------------------------------------------
pyramid = create_pyramid()  # Створює піраміду
fig = plt.figure()  # Ініціалізує новий графік
ax = fig.add_subplot(111, projection='3d')  # Додає 3D-підграфік до фігури

# Створює анімацію обертання піраміди з 72 кадрами, інтервал між кадрами 100 мс
ani = animation.FuncAnimation(fig, animate, frames=72, interval=100)
plt.show()  # Відображає анімацію