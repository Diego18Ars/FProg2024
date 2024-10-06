'''
table.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 11005)
    Francisco Afonso (No. 109466)

Modulo que contem a classe das mesas

IST - LEMec - 2023/2024
'''

from math import sqrt
from graphics import Rectangle, Circle, Polygon, Point





class Table:
    '''Classe das mesas a utilizar ao longo do projecto'''
    class Rectangular():
        '''Subclasse da mesa retangular'''
        def __init__(self, anchor):
            self.anchor = anchor
            self.food = []

            self.width = 220
            self.height = 130

            half_width, half_height = self.width/2, self.height/2

            # 110 = Largura da mesa, 65 = Comprimento da mesa
            x, y = self.anchor.getX(), self.anchor.getY()
            table_p1 = Point(x - half_width, y - half_height)
            table_p2 = Point(x + half_width, y + half_height)
            self.table = Rectangle(table_p1, table_p2)
            self.table.setFill('saddlebrown')

            self.towel = Rectangle(Point(x - 83, y - half_height), Point(x + 83, y + half_height))
            self.towel.setFill('darkred')

            self.plates = []
            self.define_plates()


        def define_plates(self):
            '''Metodo que define os pratos dispostos na mesa'''
            x, y = self.anchor.getX(), self.anchor.getY()

            plate1_outer = Circle(Point(x-50, y+40), 20)
            plate1_outer.setFill('snow')
            plate1_inner = Circle(Point(x-50, y+40), 15)
            plate1_inner.setOutline('cornflowerblue')
            plate1_inner.setWidth(2)
            plate1 = (plate1_outer, plate1_inner)

            plate2_outer = Circle(Point(x+50, y+40), 20)
            plate2_outer.setFill('snow')
            plate2_inner = Circle(Point(x+50, y+40), 15)
            plate2_inner.setOutline('cornflowerblue')
            plate2_inner.setWidth(2)
            plate2 = (plate2_outer, plate2_inner)

            plate3_outer = Circle(Point(x+50, y-40), 20)
            plate3_outer.setFill('snow')
            plate3_inner = Circle(Point(x+50, y-40), 15)
            plate3_inner.setOutline('cornflowerblue')
            plate3_inner.setWidth(2)
            plate3 = (plate3_outer, plate3_inner)

            plate4_outer = Circle(Point(x-50, y-40), 20)
            plate4_outer.setFill('snow')
            plate4_inner = Circle(Point(x-50, y-40), 15)
            plate4_inner.setOutline('cornflowerblue')
            plate4_inner.setWidth(2)
            plate4 = (plate4_outer, plate4_inner)

            self.plates = (plate1, plate2, plate3, plate4)


        def draw_food(self):
            '''Metodo que desenha a comida nos pratos dispostos na mesa (deprecado)'''
            x, y = self.anchor.getX(), self.anchor.getY()

            food1 = Circle(Point(x-50, y+40), 12)
            food1.setFill('darkgoldenrod')

            food2 = Circle(Point(x+50, y+40), 12)
            food2.setFill('darkgoldenrod')

            food3 = Circle(Point(x+50, y-40), 12)
            food3.setFill('darkgoldenrod')

            food4 = Circle(Point(x-50, y-40), 12)
            food4.setFill('darkgoldenrod')

            self.food = [food1, food2, food3, food4]


        def erase_food(self):
            '''Metodo que apaga a comida dos pratos dispostos na mesa (deprecado)'''
            for food in self.food:
                food.undraw()
            self.food = []


        def get_width(self):
            '''Retorna a largura da mesa'''
            return self.width


        def get_height(self):
            '''Retorna a altura da mesa'''
            return self.height


        def get_center(self):
            '''Retorna o centro da mesa'''
            return self.anchor


        def get_p1(self):
            '''Retorna canto superior esquerdo'''
            return self.table.getP1()


        def get_p2(self):
            '''Retorna canto inferior direito'''
            return self.table.getP2()


        def is_clicked(self, p):
            '''Metodo que verifica se o ponto esta na mesa'''
            x, y = self.anchor.getX(), self.anchor.getY()
            half_width, half_height = self.width/2, self.height/2

            return x-half_width<=p.getX() and p.getX()<=x+half_width and y-half_height<=p.getY() and p.getY()<=y+half_height


        def draw(self, win):
            '''Metodo que desenha a mesa na janela fornecida'''
            self.table.draw(win)
            self.towel.draw(win)
            for plate in self.plates:
                for component in plate:
                    component.draw(win)
            for food in self.food:
                food.draw(win)


        def undraw(self):
            '''Metodo que apaga a mesa da janela'''
            self.table.undraw()
            self.towel.undraw()
            for plate in self.plates:
                for component in plate:
                    component.undraw()
            for food in self.food:
                food.undraw()


    class Circular():
        '''Subclasse da mesa circular'''
        def __init__(self, anchor):
            self.anchor = anchor
            self.radius = 75
            self.food = []

            self.table = Circle(anchor, self.radius)
            self.table.setFill('saddlebrown')

            x, y = anchor.getX(), anchor.getY()
            self.towel = Polygon(Point(x-75, y), Point(x, y-75), Point(x+75, y), Point(x, y+75))
            self.towel.setFill('darkred')

            self.plates = []
            self.define_plates()


        def define_plates(self):
            '''Metodo que define os pratos dispostos na mesa'''
            x, y = self.anchor.getX(), self.anchor.getY()

            plate1_outer = Circle(Point(x-50, y), 20)
            plate1_outer.setFill('snow')
            plate1_inner = Circle(Point(x-50, y), 15)
            plate1_inner.setOutline('cornflowerblue')
            plate1_inner.setWidth(2)
            plate1 = (plate1_outer, plate1_inner)

            plate2_outer = Circle(Point(x, y-50), 20)
            plate2_outer.setFill('snow')
            plate2_inner = Circle(Point(x, y-50), 15)
            plate2_inner.setOutline('cornflowerblue')
            plate2_inner.setWidth(2)
            plate2 = (plate2_outer, plate2_inner)

            plate3_outer = Circle(Point(x+50, y), 20)
            plate3_outer.setFill('snow')
            plate3_inner = Circle(Point(x+50, y), 15)
            plate3_inner.setOutline('cornflowerblue')
            plate3_inner.setWidth(2)
            plate3 = (plate3_outer, plate3_inner)

            plate4_outer = Circle(Point(x, y+50), 20)
            plate4_outer.setFill('snow')
            plate4_inner = Circle(Point(x, y+50), 15)
            plate4_inner.setOutline('cornflowerblue')
            plate4_inner.setWidth(2)
            plate4 = (plate4_outer, plate4_inner)

            self.plates = (plate1, plate2, plate3, plate4)


        def draw_food(self):
            '''Metodo que define os pratos dispostos na mesa (deprecado)'''
            x, y = self.anchor.getX(), self.anchor.getY()

            food1 = Circle(Point(x-50, y), 12)
            food1.setFill('darkgoldenrod')

            food2 = Circle(Point(x, y-50), 12)
            food2.setFill('darkgoldenrod')

            food3 = Circle(Point(x+50, y), 12)
            food3.setFill('darkgoldenrod')

            food4 = Circle(Point(x, y+50), 12)
            food4.setFill('darkgoldenrod')

            self.food = [food1, food2, food3, food4]


        def erase_food(self):
            '''Metodo que apaga a comida dos pratos dispostos na mesa (deprecado)'''
            for food in self.food:
                food.undraw()
            self.food = []


        def is_clicked(self, p):
            '''Metodo que verifica se o ponto esta na mesa'''
            x, y = self.anchor.getX(), self.anchor.getY()

            return sqrt((p.getX()-x)**2 + (p.getY()-y)**2)<=self.radius


        def get_radius(self):
            '''Retorna o raio da mesa'''
            return self.radius


        def get_center(self):
            '''Retorna o centro da mesa'''
            return self.table.getCenter()


        def draw(self, win):
            '''Metodo que desenha a mesa na janela fornecida'''
            self.table.draw(win)
            self.towel.draw(win)
            for plate in self.plates:
                for component in plate:
                    component.draw(win)
            for food in self.food:
                food.draw(win)


        def undraw(self):
            '''Metodo que apaga a mesa da janela'''
            self.table.undraw()
            self.towel.undraw()
            for plate in self.plates:
                for component in plate:
                    component.undraw()
            for food in self.food:
                food.undraw()
