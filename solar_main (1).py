# coding: utf-8
# license: GPLv3

import pygame as pg
from solar_vis import *
from solar_model import *
from solar_input import *
from solar_objects import *
import thorpy
import time
import numpy as np
import matplotlib.pyplot as plt

timer = None

alive = True

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

model_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

time_scale = 1000000
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""


def execution(delta, scale_factor):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global model_time
    global displayed_time
    recalculate_space_objects_positions([dr.obj for dr in space_objects], delta, scale_factor)
    model_time += delta


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True


def pause_execution():
    global perform_execution
    perform_execution = False


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global alive
    alive = False


def open_file_1():
    in_filename = "one_satellite.txt"
    begining(in_filename)


def open_file_2():
    in_filename = "solar_system.txt"
    begining(in_filename)


def open_file_3():
    in_filename = "double_star.txt"
    begining(in_filename)


def begining(file_name):
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global browser
    global model_time
    global scale_factor

    model_time = 0.0
    # in_filename = "one_satellite.txt"
    space_objects = read_space_objects_data_from_file(file_name)
    max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in space_objects])
    scale_factor = calculate_scale_factor(max_distance)


def handle_events(events, menu):
    global alive
    for event in events:
        menu.react(event)
        if event.type == pg.QUIT:
            alive = False


def slider_to_real(val):
    return 500000 * (1.35 ** (val))


def slider_reaction(event):
    global time_scale
    time_scale = slider_to_real(event.el.get_value())


def draw_graphics():
    stop_execution()

    time_list = []
    distance_list = []
    speed_list = []
    with open('stats.txt', 'r') as stats:
        data = stats.read()
    data = data.split('\n')[1:]
    for line in data:
        if len(line) > 1:
            line_list = [float(i) for i in line.split()]
            time_list.append(line_list[0])
            distance_list.append(line_list[1])
            speed_list.append(line_list[2])

    plt.figure(figsize=(20, 10))

    sp = plt.subplot(131)
    plt.plot(time_list, speed_list, 'r')
    plt.xlabel(r'$t$')
    plt.ylabel(r'$v$')
    plt.grid('True')

    sp = plt.subplot(132)
    plt.plot(time_list, distance_list, 'r')
    plt.xlabel(r'$t$')
    plt.ylabel(r'$d$')
    plt.grid('True')

    sp = plt.subplot(133)
    plt.plot(distance_list, speed_list, 'r')
    plt.xlabel(r'$d$')
    plt.ylabel(r'$v$')
    plt.grid('True')

    sp.spines['left'].set_position('center')
    sp.spines['bottom'].set_position('center')
    plt.show()


def init_ui(screen):
    global browser
    slider = thorpy.SliderX(100, (-10, 10), "Simulation speed")
    slider.user_func = slider_reaction
    button_stop = thorpy.make_button("Quit", func=stop_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    button_play = thorpy.make_button("Play", func=start_execution)
    timer = thorpy.OneLineText("Seconds passed")

    button_load_1 = thorpy.make_button(text="Load one_satellite", func=open_file_1)
    button_load_2 = thorpy.make_button(text="Load solar_system", func=open_file_2)
    button_load_3 = thorpy.make_button(text="Load double_star", func=open_file_3)

    graphic_button = thorpy.make_button(text="Draw graphics and quit", func=draw_graphics)

    box = thorpy.Box(elements=[
        slider,
        button_pause,
        button_stop,
        button_play,
        button_load_1,
        button_load_2,
        button_load_3,
        graphic_button,
        timer])
    reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=slider_reaction,
                                event_args={"id": thorpy.constants.EVENT_SLIDE},
                                params={},
                                reac_name="slider reaction")
    box.add_reaction(reaction1)

    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((0, 0))
    box.blit()
    box.update()
    return menu, box, timer


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """

    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global perform_execution
    global timer
    global scale_factor

    print('Modelling started!')
    physical_time = 0

    pg.init()

    width = 1000
    height = 800
    screen = pg.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = Drawer(screen)
    menu, box, timer = init_ui(screen)
    perform_execution = True

    with open('stats.txt', 'w') as out_file:
        out_file.write('time\tdistance\tspeed\n')

    while alive:
        handle_events(pg.event.get(), menu)
        cur_time = time.perf_counter()
        if perform_execution:
            execution((cur_time - last_time) * time_scale, scale_factor)
            text = "%d seconds passed" % (int(model_time))
            timer.set_text(text)

        write_space_objects_data_to_file('stats.txt', [dr.obj for dr in space_objects], model_time)

        last_time = cur_time
        drawer.update(space_objects, box)
        time.sleep(1.0 / 60)

    print('Modelling finished!')


if __name__ == "__main__":
    main()
