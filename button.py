'''
button.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 11005)
    Francisco Afonso (No. 109466)

Modulo que contem a classe dos botoes a serem usados no projecto

IST - LEMec - 2023/2024
'''

from graphics import Rectangle, Text, Point

class Button:
    '''Classe de todos os botoes usados ao longo do projecto'''
    def __init__(self, p1, p2, label='', color=(255, 255, 255), size=12):
        rectangle = Rectangle(p1, p2)
        rectangle.setFill(color)
        rectangle.setOutline("black")

        if label:
            centerpoint_x = p1.getX()+abs(p1.getX() - p2.getX()) / 2
            centerpoint_y = p1.getY()+abs(p1.getY() - p2.getY()) / 2
            label = Text(Point(centerpoint_x, centerpoint_y), label)
            label.setSize(size)
            self.items = [rectangle, label]
        else:
            self.items = [rectangle]


    def is_clicked(self, p):
        '''Retorna True se o clique foi feito no botao'''
        for i in self.items:
            if isinstance(i, Rectangle):
                return (p.getX() > i.getP1().getX() and p.getX() < i.getP2().getX() and p.getY() > i.getP1().getY() and p.getY() < i.getP2().getY())


    def draw(self, win):
        '''Desenha todos os elementos do botao na janela'''
        for i in self.items:
            i.draw(win)


    def undraw(self):
        '''Apaga todos os elementos do botao da janela'''
        for i in self.items:
            i.undraw()
