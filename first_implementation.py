'''
first_implementation.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 110050)
    Francisco Afonso (No. 109466)

Modulo que contem a classe da primeira implementacao

IST - LEMec - 2023/2024
'''

from graphics import GraphWin, Point, Image, update
from button import Button
from table import Table
from counter import Counter
from docking_station import DockingStation
from waiter import Waiter




class FirstImplementation:
    '''Classe gerenciadora de todos os aspetos lógicos e gráficos da execução da 1a implementacao'''
    def __init__(self, view_x, view_y):
        self.win = None
        self.waiter = None
        self.view_x, self.view_y = view_x, view_y

        self.robot_radius = 35

        # Elementos graficos da janela
        self.b_quit = Button(Point(25, 662), Point(200, 705), "Sair", 'silver')

        self.floor = Image(Point(self.view_x/2, self.view_y/2), "marble_floor.ppm")

        #rightbound_x = view_x-35
        #target_points = ((rightbound_x, self.robot_radius), (rightbound_x, 3*self.robot_radius), (self.robot_radius, rightbound_x, 3*self.robot_radius),)

        ds1 = DockingStation(Point(self.robot_radius, self.robot_radius), 2*self.robot_radius)
        ds2 = DockingStation(Point(self.view_x-self.robot_radius, self.view_y/2), 2*self.robot_radius)
        balcao = Counter(Point(self.view_x/4, self.view_y-self.robot_radius), self.view_x/2, 2*self.robot_radius)
        mesa1 = Table.Rectangular(Point(440, 160))
        mesa2 = Table.Rectangular(Point(950, 460))
        mesa3 = Table.Circular(Point(250, 450))
        mesa4 = Table.Circular(Point(600, 450))
        mesa5 = Table.Circular(Point(960, 195))

        # Lista que contem os osbtaculos da implementacao 1
        self.obstacles = [ds1, ds2, balcao, mesa1, mesa2, mesa3, mesa4, mesa5]


    def run(self):
        '''Metodo que desenvolve toda o aspecto grafico e logico da implementacao'''

        self.win = GraphWin('1a Implementacao', 1280, 720)
        self.win.setCoords(0, self.view_y, self.view_x, 0)

        self.waiter = Waiter(Point(self.robot_radius, self.robot_radius), self.robot_radius)

        self.draw()

        targets = (Point(1245, 35), Point(1245, 105), Point(35, 105), Point(35, 175),
                   Point(1245, 175), Point(1245, 245), Point(35, 245), Point(35, 315),
                   Point(1245, 315), Point(1245, 385), Point(35, 385), Point(35, 455),
                   Point(1245, 455), Point(1245, 525), Point(35, 525), Point(35, 595),
                   Point(1245, 595), Point(1245, 615), Point(35, 615), Point(677, 615),
                   Point(677, 685), Point(1245, 685))

        for target in targets:
            self.waiter.add_target(target)

        while True:

            c = self.win.checkMouse()

            if c is not None:
                if self.b_quit.is_clicked(c):
                    self.close()
                    break

            # Movimento do robot
            self.waiter.sensor_room(self.obstacles)
            self.waiter.process_velocity()
            self.waiter.check_collisions()
            self.waiter.move()

            # Atualizacao da janela
            self.win.setBackground('white')
            update(50)


    def close(self):
        '''Metodo que encerra a implementacao adequadamente'''
        self.undraw()
        self.win.close()


    def draw(self):
        '''Desenha na janela todos os elementos graficos da implementacao'''
        self.win.setBackground('white')
        self.floor.draw(self.win)
        for i in self.obstacles:
            i.draw(self.win)
        self.waiter.draw(self.win)
        self.b_quit.draw(self.win)


    def undraw(self):
        '''Apaga da janela todos os elementos graficos da implementacao'''
        self.floor.undraw()
        for i in self.obstacles:
            i.undraw()
        self.waiter.undraw()
        self.b_quit.undraw()

