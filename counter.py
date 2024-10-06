'''
counter.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 11005)
    Francisco Afonso (No. 109466)

Modulo que contem a classe do balcao

IST - LEMec - 2023/2024
'''

from graphics import Point, Rectangle

class Counter():
    '''Classe do balcao'''
    def __init__(self, anchor, width, height):
        self.anchor = anchor
        self.width, self.height = width, height
        x, y = anchor.getX(), anchor.getY()
        counter_p1 = Point(x - (width/2), y - (height/2))
        counter_p2 = Point(x + (width/2), y + (height/2))
        self.balcao = Rectangle(counter_p1, counter_p2)
        self.balcao.setFill('dimgray')


    def is_clicked(self, p):
        '''Metodo que verifica se o ponto esta na mesa'''
        x, y = self.anchor.getX(), self.anchor.getY()
        half_width, half_height = self.width/2, self.height/2

        return x-half_width<=p.getX() and p.getX()<=x+half_width and y-half_height<=p.getY() and p.getY()<=y+half_height


    def get_p1(self):
        '''Retorna canto superior esquerdo'''
        return self.balcao.getP1()


    def get_p2(self):
        '''Retorna canto inferior direito'''
        return self.balcao.getP2()


    def draw(self, win):
        '''Metodo que desenha o balcao'''
        self.balcao.draw(win)


    def undraw(self):
        '''Metodo que apaga o balcao'''
        self.balcao.undraw()
