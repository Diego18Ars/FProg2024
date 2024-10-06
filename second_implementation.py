'''
first_implementation.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 11005)
    Francisco Afonso (No. 109466)

Modulo que contem a classe da segunda implementacao

IST - LEMec - 2023/2024
'''

from time import sleep
from math import sqrt
from graphics import GraphWin, Circle, Point, Image, update
from button import Button
from table import Table
from counter import Counter
from docking_station import DockingStation
from waiter import Waiter2

class SecondImplementation:
    '''Classe gerenciadora da segunda implementacao'''
    def __init__(self, view_x, view_y):
        self.win = None
        self.waiter = None
        self.view_x, self.view_y = view_x, view_y

        self.robot_radius = 35

        # Elementos graficos da janela
        self.b_quit = Button(Point(25, 662), Point(200, 705), "Sair", 'silver')
        self.floor = Image(Point(self.view_x/2, self.view_y/2), "marble_floor.ppm")

        ds1 = DockingStation(Point(self.robot_radius, self.robot_radius), 2*self.robot_radius)
        ds2 = DockingStation(Point(self.view_x-self.robot_radius, self.view_y/2), 2*self.robot_radius)
        balcao = Counter(Point(self.view_x/4, self.view_y-self.robot_radius), self.view_x/2, 2*self.robot_radius)
        mesa1 = Table.Rectangular(Point(440, 160))
        mesa2 = Table.Rectangular(Point(950, 460))
        mesa3 = Table.Circular(Point(250, 450))
        mesa4 = Table.Circular(Point(600, 450))
        mesa5 = Table.Circular(Point(960, 195))

        self.obstacles = [ds1, ds2, balcao, mesa1, mesa2, mesa3, mesa4, mesa5]

    def run(self):
        '''Metodo que executa a 2a implementacao'''

        self.win = GraphWin("2a Implementacao", 1280, 720)
        self.win.setCoords(0, self.view_y, self.view_x, 0)

        self.waiter = Waiter2(Point(35, 35), self.robot_radius, (self.view_x, self.view_y))

        self.draw()

        while True:

            c = self.win.checkMouse()

            # Clique foi efetuado
            if c is not None:
                if self.b_quit.is_clicked(c):
                    self.close()
                    break
                
                clicked_on_obstacle = False

                # Algum mesa foi carregada
                for obs in self.obstacles:
                    if obs.is_clicked(c) and isinstance(obs, Table.Circular):
                        self.waiter.add_task(["GETORDER", obs])
                        clicked_on_obstacle = True
                    if obs.is_clicked(c) and isinstance(obs, Table.Rectangular):
                        self.waiter.add_task(["GETORDER", obs])
                        clicked_on_obstacle = True

                # O clique foi efetuado no chao
                if not clicked_on_obstacle:
                    click_x, click_y = c.getX(), c.getY()

                    can_draw = True

                    # Define a tolerancia da sujidade as bordas da janela
                    if not (2*self.robot_radius <= click_x <= self.view_x-2*self.robot_radius and 2*self.robot_radius <= click_y <= self.view_y-2*self.robot_radius):
                        can_draw = False

                    for o in self.obstacles:
                        # Define a tolerancia da sujidade as mesas circulares
                        if type(o) == Table.Circular:
                            if sqrt((o.get_center().getX()-click_x)**2 + (o.get_center().getY()-click_y)**2) < 2*self.robot_radius+o.get_radius():
                                can_draw = False

                        # Define a tolerancia da sujidade as mesas rectangulares
                        elif type(o) == Table.Rectangular:
                            x1, y1 = o.get_p1().getX(), o.get_p1().getY()
                            x2, y2 = o.get_p2().getX(), o.get_p2().getY()
                            if x1-2*self.robot_radius <= click_x <= x2+2*self.robot_radius and y1-2*self.robot_radius <= click_y <= y2+2*self.robot_radius:
                                can_draw = False

                        # Define a tolerancia da sujidade as docking stations
                        elif type(o) == DockingStation:
                            if sqrt((o.get_center().getX()-click_x)**2 + (o.get_center().getY()-click_y)**2) < 2.5*self.robot_radius:
                                can_draw = False

                        elif type(o) == Counter:
                            x1, y1 = o.get_p1().getX(), o.get_p1().getY()
                            x2, y2 = o.get_p2().getX(), o.get_p2().getY()
                            if x1-2*self.robot_radius <= click_x <= x2+2*self.robot_radius and y1-2*self.robot_radius <= click_y <= y2+2*self.robot_radius:
                                can_draw = False

                    # Se nao houver algum impedimento para que o lixo nao possa ser desenhado
                    if can_draw:
                        garbage = Circle(c, 13)
                        garbage.setFill('lightsalmon')
                        self.waiter.undraw()
                        garbage.draw(self.win)
                        self.waiter.draw(self.win)
                        self.waiter.add_task(["CLEANFLOOR", c, garbage])
                            

            self.waiter.process_task(self.obstacles)
            self.waiter.check_collision(self.obstacles)
            self.waiter.move()

            update(50)


    def close(self):
        '''Metodo que fecha a classe adequadamente'''
        self.undraw()
        self.win.close()

    def draw(self):
        '''Metodo que desenha todos os elementos na janela'''
        self.win.setBackground('white')
        self.floor.draw(self.win)
        for obs in self.obstacles:
            obs.draw(self.win)
        self.waiter.draw(self.win)
        self.b_quit.draw(self.win)


    def undraw(self):
        '''Metodo que apaga todos os elementos da janela'''
        self.floor.undraw()
        for obs in self.obstacles:
            obs.undraw()
        self.waiter.undraw()
        self.b_quit.undraw()