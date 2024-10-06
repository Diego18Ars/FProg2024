'''
third_implementation.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 110050)
    Francisco Afonso (No. 109466)

Modulo que contem a classe da terceira implementacao

IST - LEMec - 2023/2024
'''

from math import sqrt
from graphics import GraphWin, Image, Circle, Point, update
from button import Button
from table import Table
from docking_station import DockingStation
from file_reader import FileReader
from waiter import Waiter2
from counter import Counter




class ThirdImplementation:
    '''Classe da 3a implementacao'''
    def __init__(self, filepath):
        '''win - Janela (classe GraphWin) onde a implementacao sera projetada'''
        self.robot_radius = 35
        
        self.file_reader = FileReader(filepath)
        
        self.size, self.dspoints, self.TableList, self.XYList = self.file_reader.return_values()
        self.size = [int(self.size[0]), int(self.size[1])]


        self.win = GraphWin("3a Implementacao", self.size[0], self.size[1])
        self.win.setCoords(0, self.size[1], self.size[0], 0)

        balcao = Counter(Point(self.size[0]/4, self.size[1]-35), self.size[0]/2, 2*35)
        ds1 = DockingStation(eval(self.dspoints[0])[0], 2*eval(self.dspoints[0])[1])
        ds2 = DockingStation(eval(self.dspoints[1])[0], 2*eval(self.dspoints[1])[1])

        self.obstacles = [balcao, ds1, ds2]

        l = len(self.TableList)           
        for i in range(0, l, 2):
            if self.TableList[i] == "Rect":
                x, y = eval(self.TableList[i+1])
                self.obstacles.append(Table.Rectangular(Point(x,y)))
            elif self.TableList[i] == "Circ":
                x, y = eval(self.TableList[i+1])
                self.obstacles.append(Table.Circular(Point(x,y)))

        self.b_quit = Button(Point(25, 662), Point(200, 705), "Sair", 'silver')

        self.floor = Image(Point(self.size[0]/2, self.size[1]/2), "marble_floor.ppm")
        self.run()


    def run(self):
        '''Metodo que executa a 3a implementacao'''

        self.waiter = Waiter2(Point(35, 35), self.robot_radius, (self.size[0], self.size[1]))

        self.draw()

        while True:

            c = self.win.checkMouse()

            if c != None:
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
                    if not (2*self.robot_radius <= click_x <= self.size[0]-2*self.robot_radius and 2*self.robot_radius <= click_y <= self.size[1]-2*self.robot_radius):
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
        '''Metodo que encerra a implementacao adequadamente'''
        self.undraw()
        self.win.close()


    def draw(self):
        self.win.setBackground('white')
        self.floor.draw(self.win)
        for o in self.obstacles:
            o.draw(self.win)
        self.waiter.draw(self.win)
        self.b_quit.draw(self.win)


    def undraw(self):
        self.floor.undraw()
        self.waiter.undraw()
        for o in self.obstacles:
            o.undraw()
        self.b_quit.undraw()
