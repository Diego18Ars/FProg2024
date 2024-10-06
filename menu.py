'''
menu.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 110050)
    Francisco Afonso (No. 109466)

Modulo que contem a classe do menu a ser utilizada no projecto

IST - LEMec - 2023/2024
'''

from graphics import *
from button import Button
from first_implementation import FirstImplementation
from second_implementation import SecondImplementation
from third_implementation import ThirdImplementation


class Menu:
    '''Classe que gerencia toda a aplicacao'''
    def __init__(self):
        self.win = GraphWin("Projeto FPROG 2024", 1280, 720)
        self.win.setCoords(0, 720, 1280, 0)

        # Instancias das implementacoes
        self.first_implementation = FirstImplementation(1280, 720)
        self.second_implementation = SecondImplementation(1280, 720)
        self.third_implementation_menu = Menu3()
        self.image = Image(Point(640, 360), 'socials.ppm')

        # Botoes que levam as respectivas implementacoes
        b_1_impl = Button(Point(256, 72), Point(1024, 216), '1a Implementacao', 'steelblue', 15)
        b_2_impl = Button(Point(256, 288), Point(1024, 432), '2a Implementacao', 'steelblue', 15)
        b_3_impl = Button(Point(256, 504), Point(1024, 648), '3a Implementacao', 'steelblue', 15)

        self.items = [b_1_impl, b_2_impl, b_3_impl]

        self.draw()
        self.handle_input()


    def handle_input(self):
        '''Metodo usado para aguardar o input do utilizador e gerenciar o mesmo'''
        try:
            c = self.win.getMouse()
            while self.win.isOpen():
                if self.items[0].is_clicked(c):
                    self.close()
                    self.first_implementation.run()
                    self.display_window()
                    break
                if self.items[1].is_clicked(c):
                    self.close()
                    self.second_implementation.run()
                    self.display_window()
                    break
                if self.items[2].is_clicked(c):
                    self.close()
                    self.third_implementation_menu.click()
                    self.display_window()
                    break
                c = self.win.getMouse()
        except GraphicsError:
            pass


    def display_window(self):
        '''Metodo para exibir janela'''
        self.win = GraphWin("Projeto FPROG 2024", 1280, 720)
        self.win.setCoords(0, 720, 1280, 0)

        self.draw()
        self.handle_input()


    def close(self):
        '''Metodo que fecha a janela de modo adequado'''
        self.undraw()
        self.win.close()


    def draw(self):
        '''Desenha os elementos graficos menu'''
        self.win.setBackground('ghostwhite')
        self.image.draw(self.win)
        for i in self.items:
            i.draw(self.win)

        update(50)


    def undraw(self):
        '''Apaga os elementos graficos menu'''
        for i in self.items:
            i.undraw()
        self.image.undraw()

        update(50)

class Menu3:

    def __init__(self):
        pass

    def click(self):

        self.win = GraphWin("Projeto FPROG 2024", 1280, 720)
        self.win.setCoords(0, 720, 1280, 0)
        self.text = Text(Point(440,300), 'Insira aqui o nome do ficheiro seguido de .txt')
        self.text.setSize(12)
        self.entry = Entry(Point(640, 330), 100)
        self.b_quit = Button(Point(25, 662), Point(200, 705), "Sair", 'silver')
        self.b_continue = Button(Point(1080, 662), Point(1255, 705), "Continuar", 'silver')

        self.text.draw(self.win)
        self.entry.draw(self.win)
        self.b_quit.draw(self.win)
        self.b_continue.draw(self.win)

        while self.win.isOpen():
            c = self.win.getMouse()
            if self.b_quit.is_clicked(c):
                self.win.close()
            if self.b_continue.is_clicked(c):
                try:
                    open(self.entry.getText(), 'r')
                    third_implementation = ThirdImplementation(self.entry.getText())
                    self.win.close()
                except:
                    self.entry.setText("DOCUMENTO NAO EXISTENTE")


    def close(self):
        self.win.close()
