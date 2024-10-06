'''
battery.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 110050)
    Francisco Afonso (No. 109466)

Modulo que contem a bateria

IST - LEMec - 2023/2024
'''

from graphics import Circle




class Battery:
    '''Classe da bateria utilizada pelo robot'''
    def __init__(self, starting_point, size):
        self.size = size
        self.center = starting_point
        
        self.light = Circle(starting_point, size/1.1)
        self.light.setFill('limegreen')
        self.color = 'limegreen'

        self.cover = Circle(starting_point, size/1.3)
        self.cover.setFill('slategray')

    
    def reset(self, pos):
        '''Metodo que reseta a bateria (deprecado)'''
        self.light = Circle(pos, self.size/3)
        self.light.setFill('limegreen')
        self.color = 'limegreen'
        self.cover = Circle(pos, self.size/3.5)
        self.cover.setFill('slategrey')
        self.center = pos


    def charge(self):
        '''Metodo que recarrega a bateria (i.e. muda a cor para verde)'''
        self.light.setFill('limegreen')
        self.color = 'limegreen'


    def evaluate_distance(self, distance, allowed_dist):
        '''Conforme a distancia, avalia a cor do LED da bateria'''
        if distance > 0.25*allowed_dist and self.color == 'limegreen':
            self.color = 'gold'
            self.light.setFill('gold')
        if distance > 0.5*allowed_dist and self.color == 'gold':
            self.color = 'orangered'
            self.light.setFill('orangered')
        if distance > 0.75*allowed_dist and self.color == 'orangered':
            self.color = 'maroon'
            self.light.setFill('maroon')
            return True
        return False


    def move(self, dx, dy):
        '''Metodo que move a bateria'''
        self.center.move(dx, dy)
        self.light.move(dx, dy)
        self.cover.move(dx, dy)


    def getCenter(self):
        '''Retorna o centro da bateria'''
        return self.center


    def draw(self, win):
        '''Metodo que desenha a bateria (chamada em conjunto com o robot)'''
        self.light.draw(win)
        self.cover.draw(win)


    def undraw(self):
        '''Metodo que apaga a bateria (geralmente em conjunto com o robot)'''
        self.light.undraw()
        self.cover.undraw()