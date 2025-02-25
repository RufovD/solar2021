# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet
from solar_vis import DrawableObject


def read_space_objects_data_from_file(input_filename):
    """Считывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов.

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем

            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                star = parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                planet = parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return [DrawableObject(obj) for obj in objects]


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.

    Входная строка должна иметь следующий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.

    Пример строки:

    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.

    **star** — объект звезды.
    """
    param_list = line.split()
    star.R = float(param_list[1])
    star.color = param_list[2]
    star.m = float(param_list[3])
    star.x = float(param_list[4])
    star.y = float(param_list[5])
    star.Vx = float(param_list[6])
    star.Vy = float(param_list[7])

    return star


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Входная строка должна иметь следюущий формат:

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.

    Пример строки:

    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.

    **planet** — объект планеты.
    """
    param_list = line.split()
    planet.R = float(param_list[1])
    planet.color = param_list[2]
    planet.m = float(param_list[3])
    planet.x = float(param_list[4])
    planet.y = float(param_list[5])
    planet.Vx = float(param_list[6])
    planet.Vy = float(param_list[7])

    return planet


def write_space_objects_data_to_file(output_filename, space_objects, model_time):
    """Сохраняет данные о космических объектах в файл.

    Строки должны иметь следующий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла

    **space_objects** — список объектов планет и звёзд
    """
    if len(space_objects) == 2 and ((space_objects[0].type == 'star' and space_objects[1].type == 'planet') or
                                    (space_objects[1].type == 'star' and space_objects[0].type == 'planet')):
        if space_objects[0].type == 'star' and space_objects[1].type == 'planet':
            star = space_objects[0]
            planet = space_objects[1]
        else:
            star = space_objects[1]
            planet = space_objects[0]
        with open(output_filename, 'a') as out_file:
            distance = ((planet.x - star.x) ** 2 + (planet.y - star.y) ** 2) ** 0.5
            speed = (planet.Vx ** 2 + planet.Vy ** 2) ** 0.5
            out_file.write(('\t').join([str(i) for i in [model_time, distance, speed, '\n']]))



if __name__ == "__main__":
    print("This module is not for direct call!")
