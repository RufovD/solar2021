# coding: utf-8
# license: GPLv3

from math import sin, cos, atan, pi
from solar_vis import DrawableObject

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.

    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        dx = obj.x - body.x
        dy = obj.y - body.y
        r = (dx ** 2 + dy ** 2) ** 0.5
        try:
            fi = atan(dy / abs(dx))
        except ZeroDivisionError:
            fi = atan(dy / (abs(dx) + 0.0000000001))
        if dx < 0:
            fi = pi - fi
        F = gravitational_constant * body.m * obj.m / r ** 2
        body.Fx += F * cos(fi)
        body.Fy += F * sin(fi)

    return body


def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    ax = body.Fx / body.m
    ay = body.Fy / body.m
    body.Vx += ax * dt
    body.Vy += ay * dt
    body.x += body.Vx * dt + ax * dt ** 2 / 2
    body.y += body.Vy * dt + ay * dt ** 2 / 2

    return body


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список объектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
    for body_i in range(len(space_objects)):
        space_objects[body_i] = calculate_force(space_objects[body_i], space_objects)
    for body_i in range(len(space_objects)):
        space_objects[body_i] = move_space_object(space_objects[body_i], dt)

    return [DrawableObject(obj) for obj in space_objects]


if __name__ == "__main__":
    print("This module is not for direct call!")
