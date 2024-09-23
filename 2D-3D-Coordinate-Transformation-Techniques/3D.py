import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation

#---------------------------------- координати піраміди ------------------------------------
def create_pyramid():
    return np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0.5, 0.5, 1]])

#--------------------------------- проекція на XY -----------------------------------------
def project_onto_xy(points):
    return points[:, :2]

#---------------------------------- зміщення ----------------------------------------------
def translate(points, tx, ty, tz):
    translation_matrix = np.array([[1, 0, 0, tx],
                                    [0, 1, 0, ty],
                                    [0, 0, 1, tz],
                                    [0, 0, 0, 1]])
    extended_points = np.hstack((points, np.ones((points.shape[0], 1))))  # розширення до 4D
    return (extended_points.dot(translation_matrix.T))[:, :3]

#---------------------------------- обертання ----------------------------------------------
def rotate(points, angle, axis):
    theta = np.radians(angle)
    if axis == 'x':
        rotation_matrix = np.array([[1, 0, 0],
                                     [0, np.cos(theta), -np.sin(theta)],
                                     [0, np.sin(theta), np.cos(theta)]])
    elif axis == 'y':
        rotation_matrix = np.array([[np.cos(theta), 0, np.sin(theta)],
                                     [0, 1, 0],
                                     [-np.sin(theta), 0, np.cos(theta)]])
    elif axis == 'z':
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                     [np.sin(theta), np.cos(theta), 0],
                                     [0, 0, 1]])
    return points.dot(rotation_matrix.T)

#---------------------------------- анімація ----------------------------------------------
def animate(i):
    ax.clear()
    ax.set_title("Анімація обертання піраміди")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Обертання піраміди
    rotated_pyramid = rotate(pyramid, i * 5, 'y')  # обертання навколо осі Y
    projected_pyramid = project_onto_xy(rotated_pyramid)

    # Малювання піраміди
    vertices = [
        [rotated_pyramid[0], rotated_pyramid[1], rotated_pyramid[2], rotated_pyramid[3]],  # основа
        [rotated_pyramid[0], rotated_pyramid[1], rotated_pyramid[4]],  # бокові грані
        [rotated_pyramid[1], rotated_pyramid[2], rotated_pyramid[4]],
        [rotated_pyramid[2], rotated_pyramid[3], rotated_pyramid[4]],
        [rotated_pyramid[3], rotated_pyramid[0], rotated_pyramid[4]]
    ]
    ax.add_collection3d(Poly3DCollection(vertices, facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.5))

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-0.5, 2])

#---------------------------------- основний код ----------------------------------------------
pyramid = create_pyramid()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ani = animation.FuncAnimation(fig, animate, frames=72, interval=100)
plt.show()
