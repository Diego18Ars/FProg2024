'''
docking_station.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 11005)
    Francisco Afonso (No. 109466)

Modulo que contem a classe da docking station a ser utilizada no projecto

IST - LEMec - 2023/2024
'''

from graphics import Rectangle, Circle, Point


class DockingStation:
    '''Classe da docking station'''
    def __init__(self, anchor, size):
        self.anchor = anchor

        x, y = self.anchor.getX(), self.anchor.getY()
        base = Rectangle(Point(x - (size/2), y - (size/2)), Point(x + (size/2), y + (size/2)))
        base.setFill('silver')

        inner_plate = Rectangle(Point(x - (5*size/14), y - (5*size/14)), Point(x + (5*size/14), y + (5*size/14)))
        inner_plate.setFill('gainsboro')

        self.items = [base, inner_plate]

        for n1 in range(1,4):
            for n2 in range(1,4):
                pin = Circle(Point((x - (size/2)) + n1 * (size/4), y - (size/2) + n2 * (size/4)), size*0.07)
                pin.setFill('goldenrod')
                self.items.append(pin)


    def is_clicked(self, p):
        '''Metodo que retorna a bool se o elemento for clickado'''
        x1, y1 = self.items[0].getP1().getX(), self.items[0].getP1().getY()
        x2, y2 = self.items[0].getP2().getX(), self.items[0].getP2().getY()

        return x1<=p.getX() and p.getX()<=x2 and y1<=p.getY() and p.getY()<=y2

    def get_center(self):
        '''Retorna o centro da docking station'''
        return self.anchor


    def draw(self, win):
        '''Metodo que desenha a docking station'''
        for i in self.items:
            i.draw(win)


    def undraw(self):
        '''Metodo que apaga a docking station'''
        for i in self.items:
            i.undraw()
