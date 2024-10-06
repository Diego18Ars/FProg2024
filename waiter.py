'''
waiter.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 110050)
    Francisco Afonso (No. 109466)

Modulo que contem as classes dos robots, i.e., Waiter e Waiter2

IST - LEMec - 2023/2024
'''

from time import sleep
from math import sqrt, pi, acos
from graphics import Circle, Point
from table import Table
from counter import Counter
from docking_station import DockingStation
from battery import Battery



class Waiter:
    '''Classe do robot'''
    def __init__(self, starting_point, radius):
        self.radius = radius
        self.distance = 0
        self.data = []
        self.targets = []
        self.target_counter = 0
        self.docked = None
        # Cordenadas do versor da velocidade
        self.dx, self.dy = 0, 0
        # Velocidade omnidirecional do robot
        self.velocity = 3

        self.robot = Circle(starting_point, self.radius)
        self.robot.setFill("slategray")


    def sensor_room(self, obstacles):
        '''Funcao para obter informacoes sobre os obstaculos da sala na proxima iteracao'''
        self.data = []

        for obst in obstacles:
            if isinstance(obst, DockingStation):
                self.data.append([DockingStation, obst.get_center()])
            elif isinstance(obst, Table.Circular):
                self.data.append([Table.Circular, obst.get_center(), obst.get_radius()])
            elif isinstance(obst, Table.Rectangular):
                x1, y1 = obst.get_p1().getX(), obst.get_p1().getY()
                x2, y2 = obst.get_p2().getX(), obst.get_p2().getY()
                self.data.append([Table.Rectangular, x1, y1, x2, y2])
            elif isinstance(obst, Counter):
                x1, y1 = obst.get_p1().getX(), obst.get_p1().getY()
                x2, y2 = obst.get_p2().getX(), obst.get_p2().getY()
                self.data.append([Counter, x1, y1, x2, y2])


    def process_velocity(self):
        '''Metodo que define a velocidade de acordo com os objetivos'''
        center = self.robot.getCenter()
        x, y = center.getX(), center.getY()

        if len(self.targets) > 0:
            target = self.targets[self.target_counter]
            target_x, target_y = target.getX(), target.getY()
            norm = sqrt((target_x - x)**2 + (target_y - y)**2)

            # Se o robot estivar mais longe do que uma bola centrada no target de raio igual a velocidade ele mexe-se com a velocidade normal
            if norm >= self.velocity:
                velocity_vector = (target_x - x, target_y - y)
                velocity_vector = (velocity_vector[0]/norm, velocity_vector[1]/norm)
                self.dx = self.velocity*velocity_vector[0]
                self.dy = self.velocity*velocity_vector[1]

            # Caso contrario ele vai direto ao ponto
            else:
                velocity_vector = (target_x - x, target_y - y)
                self.dx = velocity_vector[0]
                self.dy = velocity_vector[1]
                if self.target_counter + 2 > len(self.targets):
                    if not self.docked:
                        self.return_to_dock()
                else:
                    self.target_counter += 1


    def check_collisions(self):
        '''Metodo para detetar colisoes'''
        # Cordenadas do robo
        x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()


        for dataline in self.data:

            # Codigo de acomplamento do robot com a docking station
            if dataline[0] == DockingStation:
                dock_x, dock_y = dataline[1].getX(), dataline[1].getY()

                # Se o robo estiver em cima da docking station, o robo esta conectado
                if x == dock_x and y == dock_y:
                    self.docked = True
                else:
                    self.docked = False


            # Codigo de colisao com mesas circulares
            elif dataline[0] == Table.Circular:
                next_x, next_y = x+self.dx, y+self.dy
                table_x, table_y = dataline[1].getX(), dataline[1].getY()
                next_dist = sqrt((next_x-table_x)**2 + (next_y-table_y)**2)
                norm = sqrt((x-table_x)**2 + (y-table_y)**2)

                if next_dist <= dataline[2]+1.1*self.radius:
                    if self.dx > 0:
                        self.targets.insert(self.target_counter, Point(table_x+dataline[2]+self.radius ,y))
                        self.dx = self.velocity * (table_y-y) / norm
                        self.dy = -self.velocity * (table_x-x) / norm
                    elif self.dx < 0:
                        self.targets.insert(self.target_counter, Point(table_x-dataline[2]-self.radius, y))
                        self.dx = self.velocity * (table_y-y) / norm
                        self.dy = -self.velocity * (table_x-x) / norm

            # Codigo de colisao com mesas rectangulares
            elif dataline[0] == Table.Rectangular:
                next_x, next_y = x+self.dx, y+self.dy
                rr = self.radius

                # Robot colide
                if dataline[1]-1.1*rr <= next_x <= dataline[3]+1.1*rr and dataline[2]-1.1*rr <= next_y <= dataline[4]+1.1*rr:

                    # Bateu com o lado direito da mesa
                    if x > dataline[3] and dataline[2]-1.1*self.radius <= y <= dataline[4]+1.1*self.radius:
                        # Colidiu acima da metade da mesa
                        if y <= (dataline[2]+dataline[4])/2:
                            self.dx, self.dy = 0, 0
                            self.targets.insert(self.target_counter, Point(dataline[1]-1.2*rr, y))
                            self.targets.insert(self.target_counter, Point(dataline[1]-1.2*rr, dataline[2]-1.2*rr))
                            self.targets.insert(self.target_counter, Point(x, dataline[2]-1.2*rr))

                        # Colidiu abaixo dda metade da mesa
                        else:
                            self.dx, self.dy = 0, 0
                            self.targets.insert(self.target_counter, Point(dataline[1]-1.2*rr, y))
                            self.targets.insert(self.target_counter, Point(dataline[1]-1.2*rr, dataline[4]+1.2*rr))
                            self.targets.insert(self.target_counter, Point(x, dataline[4]+1.2*rr))

                    # Bateu com o lado esquerdo da mesa
                    elif x < dataline[1] and dataline[2]-1.1*self.radius <= y <= dataline[4]+1.1*self.radius:
                        # Colidiu acima da metade da mesa
                        if y <= (dataline[2]+dataline[4])/2:
                            self.dx, self.dy = 0, 0
                            self.targets.insert(self.target_counter, Point(dataline[3]+1.2*rr, y))
                            self.targets.insert(self.target_counter, Point(dataline[3]+1.2*rr, dataline[2]-1.2*rr))
                            self.targets.insert(self.target_counter, Point(x, dataline[2]-1.2*rr))

                        # Colidiu abaixo dda metade da mesa
                        else:
                            self.dx, self.dy = 0, 0
                            self.targets.insert(self.target_counter, Point(dataline[3]+1.2*rr, y))
                            self.targets.insert(self.target_counter, Point(dataline[3]+1.2*rr, dataline[4]+1.2*rr))
                            self.targets.insert(self.target_counter, Point(x, dataline[4]+1.2*rr))


    def return_to_dock(self):
        '''Metodo que procura a docking station mas proxima e define-a como target'''
        dock_dist = None
        dock_pos = None
        for dataline in self.data:
            if dataline[0] == DockingStation:
                x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()
                dock_x, dock_y = dataline[1].getX(), dataline[1].getY()
                if dock_dist is None and dock_pos is None:
                    dock_pos = dataline[1]
                    dock_dist = sqrt((dock_x - x)**2 + (dock_y - y)**2)
                elif dock_dist > sqrt((dock_x - x)**2 + (dock_y - y)**2):
                    dock_pos = dataline[1]
        self.add_target(dock_pos)
        self.target_counter += 1


    def add_target(self, target):
        '''Metodo que adiciona pontos-objectivo ao robo'''
        self.targets.append(target)


    def move(self):
        '''Mexe o robo e o centro do robo de acordo com as velocidade adequadas'''
        self.robot.move(self.dx, self.dy)


    def reset(self, pos):
        '''Reset o robo para as configuracoes iniciais'''
        self.robot = Circle(pos, self.radius)
        self.robot.setFill("slategrey")


    def get_center(self):
        '''Retorna o centro do robo'''
        return self.robot.getCenter()


    def get_radius(self):
        '''Retorna o raio do robo'''
        return self.robot.getRadius()


    def draw(self, win):
        '''Funcao que desenha o robo'''
        self.robot.draw(win)


    def undraw(self):
        '''Apaga o robo'''
        self.robot.undraw()




class Waiter2:
    '''2a classe de robo para as implementacoes 2 e 3'''
    def __init__(self, starting_point, radius, room_resolution=(1280, 720)):
        self.radius = radius
        self.distance = 0
        self.data = []
        self.tasks = []
        self.task_tracker = 0
        self.room_resolution = room_resolution

        # Cordenadas do versor da velocidade
        self.dx, self.dy = 0, 0
        # Velocidade omnidirecional do robot
        self.velocity = 3

        self.robot = Circle(starting_point, self.radius)
        self.robot.setFill("slategray")
        self.battery = Battery(starting_point, self.radius)


    def process_task(self, obstacles):
        '''Metodo que orienta o robot as tarefas indicadas'''

        if 0 < len(self.tasks):
            if self.task_tracker + 1 <= len(self.tasks): 
                task = self.tasks[self.task_tracker]

                # O tipo de tarefa exigida e limpar
                if task[0] == "CLEANFLOOR":
                    target_x, target_y = task[1].getX(), task[1].getY()
                    x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

                    vec = [target_x-x, target_y-y]
                    norm = sqrt(vec[0]**2 + vec[1]**2)

                    if norm >= 3*self.radius/4:
                        self.dx = self.velocity*vec[0]/norm
                        self.dy = self.velocity*vec[1]/norm
                    else:
                        theta = 0
                        while theta < 2*pi:
                            x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()
                            vec = [target_x-x, target_y-y]
                            norm = sqrt(vec[0]**2 + vec[1]**2)
                            self.dx = 0.05*vec[1]/norm
                            self.dy = -0.05*vec[0]/norm

                            #print(((vec[0]*new_vec[0])+(vec[1]*new_vec[1]))/(norm*new_norm))
                            theta += 0.002
                            self.move()

                        self.dx, self.dy = 0, 0
                        task[2].undraw()
                        try:
                            if self.tasks[self.task_tracker+1][0] == "CLEANFLOOR":
                                self.task_tracker += 1
                        except:
                            task[0] = "TERMINATETASK"
                        

                # A tarefa e servir a mesa
                elif task[0] == "GETORDER":
                    x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

                    # A mesa a servir e circular
                    if isinstance(task[1], Table.Circular):
                        # Calcular vector tagente
                        table_x, table_y = task[1].get_center().getX(), task[1].get_center().getY()
                        vec = [table_x-x, table_y-y]
                        norm = sqrt(vec[0]**2 + vec[1]**2)
                        self.dx, self.dy = self.velocity*vec[0]/norm, self.velocity*vec[1]/norm
                        next_dist = sqrt((x+self.dx-table_x)**2 + (y+self.dy-table_y)**2)
                        # Robot colide com a mesa circular
                        if next_dist <= 1.1*self.radius+task[1].get_radius():
                            self.dx, self.dy = 0, 0
                            task[0] = "GETFOOD"
                            sleep(3)
                    
                    # A mesa a servir e rectangular
                    if isinstance(task[1], Table.Rectangular):
                        # Informacao relativa a mesa
                        table_x1, table_y1 = task[1].get_p1().getX(), task[1].get_p1().getY()
                        table_x2, table_y2 = task[1].get_p2().getX(), task[1].get_p2().getY()
                        table_x = (table_x1+table_x2)/2
                        table_y = (table_y1+table_y2)/2
                        vec = [table_x-x, table_y-y]
                        norm = sqrt(vec[0]**2 + vec[1]**2)
                        self.dx, self.dy = self.velocity*vec[0]/norm, self.velocity*vec[1]/norm

                        if table_x1-1.1*self.radius <= x+self.dx <= table_x2+1.1*self.radius and table_y1-1.1*self.radius <= y+self.dy <= table_y2+1.1*self.radius:
                            task[0] = "GETFOOD"
                            sleep(3)

                # Ir buscar comida
                elif task[0] == "GETFOOD":
                    # Identificar o balcao
                    for o in obstacles:
                        if isinstance(o, Counter):
                            counter = o

                    # Definir velocidade em direcao ao balcao
                    counter_x = (counter.get_p1().getX()+counter.get_p2().getX())/2
                    counter_y = (counter.get_p1().getY()+counter.get_p2().getY())/2
                    x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

                    vec = [counter_x-x, counter_y-y]
                    norm = sqrt(vec[0]**2 + vec[1]**2)
                    self.dx, self.dy = self.velocity*vec[0]/norm, self.velocity*vec[1]/norm

                    counter_x1, counter_y1 = counter.get_p1().getX(), counter.get_p1().getY()
                    counter_x2, counter_y2 = counter.get_p2().getX(), counter.get_p2().getY()

                    # Se o robot estiver a uma distancia proxima do balcao
                    if counter_x1-1.1*self.radius <= x+self.dx <= counter_x2+1.1*self.radius and counter_y1-1.1*self.radius <= y+self.dy <= counter_y2*1.1*self.radius:
                        self.dx, self.dy = 0, 0
                        sleep(2)
                        task[0] = "SERVE"

                # Servir a comida a mesa
                elif task[0] == "SERVE":
                    x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

                    # Se a mesa a servir for circular
                    if isinstance(task[1], Table.Circular):
                        table_x, table_y = task[1].get_center().getX(), task[1].get_center().getY()
                        vec = [table_x-x, table_y-y]
                        norm = sqrt(vec[0]**2 + vec[1]**2)
                        self.dx, self.dy = self.velocity*vec[0]/norm, self.velocity*vec[1]/norm

                        # Colisao com a mesa faz com que o robot sirva a mesa e retorne a dockingstation
                        next_dist = sqrt((x+self.dx-table_x)**2 + (y+self.dy-table_y)**2)
                        if next_dist <= 1.1*self.radius+task[1].get_radius():
                            self.dx, self.dy = 0, 0
                            # TODO: ver da comida dos pratos
                            #task[1].draw_food()
                            task[0] = "RETURNTODOCK"
                            sleep(2)

                    # Se a mesa a servir for rectangular
                    elif isinstance(task[1], Table.Rectangular):
                        # Informacao relativa a mesa
                        table_x1, table_y1 = task[1].get_p1().getX(), task[1].get_p1().getY()
                        table_x2, table_y2 = task[1].get_p2().getX(), task[1].get_p2().getY()
                        table_x = (table_x1+table_x2)/2
                        table_y = (table_y1+table_y2)/2
                        vec = [table_x-x, table_y-y]
                        norm = sqrt(vec[0]**2 + vec[1]**2)
                        self.dx, self.dy = self.velocity*vec[0]/norm, self.velocity*vec[1]/norm

                        if table_x1-1.1*self.radius <= x+self.dx <= table_x2+1.1*self.radius and table_y1-1.1*self.radius <= y+self.dy <= table_y2+1.1*self.radius:
                            task[0] = "RETURNTODOCK"
                            sleep(2)

                # Voltar a uma dockingstation
                elif task[0] == "RETURNTODOCK":
                    dock_dist = None
                    dock = None

                    # Verifica qual a docking station mais perto
                    for o in obstacles:
                        if isinstance(o, DockingStation):
                            ds_x, ds_y = o.get_center().getX(), o.get_center().getY()
                            x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()
                            dist = sqrt((x-ds_x)**2 + (y-ds_y)**2)
                            if dock_dist is None:
                                dock_dist = dist
                                dock = o
                            elif dist < dock_dist:
                                dock_dist = dist
                                dock = o

                    target_x, target_y = dock.get_center().getX(), dock.get_center().getY()
                    x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

                    vec = [target_x-x, target_y-y]
                    norm = sqrt(vec[0]**2 + vec[1]**2)
                    
                    if norm >= self.velocity:
                        self.dx, self.dy = self.velocity*vec[0]/norm, self.velocity*vec[1]/norm
                    else:
                        self.dx, self.dy = vec[0], vec[1]
                        if isinstance(task[1], Table.Circular):
                            task[0] = "CLEANTABLE"
                            sleep(3)
                        elif isinstance(task[1], Table.Rectangular):
                            '''task[0] = "CLEANTABLE"
                            sleep(3)'''
                            task[0] = "TERMINATETASK"

                # Pedido para limpar a mesa
                elif task[0] == "CLEANTABLE":
                    x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

                    # Se a mesa a limpar for circular
                    if isinstance(task[1], Table.Circular):
                        target_x, target_y = task[1].get_center().getX(), task[1].get_center().getY()
                        vec = [target_x-x, target_y-y]
                        norm = sqrt(vec[0]**2 + vec[1]**2)
                        self.dx, self.dy = self.velocity*vec[0]/norm, self.velocity*vec[1]/norm

                        # Colisao com a mesa faz com que o robot sirva a mesa e retorne a dockingstation
                        next_dist = sqrt((x+self.dx-target_x)**2 + (y+self.dy-target_y)**2)
                        if next_dist <= 1.1*self.radius+task[1].get_radius():
                            theta = 0
                            while theta < 2*pi:
                                x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

                                vec = [target_x-x, target_y-y]
                                norm = sqrt(vec[0]**2 + vec[1]**2)

                                self.dx = -0.15*vec[1]/norm
                                self.dy = 0.15*vec[0]/norm
                                #print(theta)
                                theta += 0.001
                                self.move()
                            
                            #task[1].erase_food()
                            task[0] = "TERMINATETASK"

                    # Se a mesa a limpar for rectangular
                    '''if isinstance(task[1], Table.Rectangular):
                        # Informacao relativa a mesa
                        table_x1, table_y1 = task[1].get_p1().getX(), task[1].get_p1().getY()
                        table_x2, table_y2 = task[1].get_p2().getX(), task[1].get_p2().getY()
                        table_x = (table_x1+table_x2)/2
                        table_y = (table_y1+table_y2)/2
                        vec = [table_x-x, table_y-y]
                        norm = sqrt(vec[0]**2 + vec[1]**2)
                        self.dx, self.dy = self.velocity*vec[0]/norm, self.velocity*vec[1]/norm

                        # O robot chegou a mesa
                        if table_x1-1.1*self.radius <= x+self.dx <= table_x2+1.1*self.radius and table_y1-1.1*self.radius <= y+self.dy <= table_y2+1.1*self.radius:
                            
                            distance = 0
                            # Enquanto o robot nao percorre o perimetro da mesa
                            while distance < 2*((table_x2-table_x1)+(table_y2-table_y1)):
                                x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

                                # Bate por cima
                                if y < table_y1-1.1*self.radius and table_x1-1.1*self.radius <= x <= table_x2+1.1*self.radius:
                                    self.dx, self.dy = -self.velocity, 0
                                    self.move()
                                    distance += sqrt(self.dx**2 + self.dy**2)
                                # Bate por baixo
                                elif y > table_y2+1.1*self.radius and table_x1-1.1*self.radius <= x <= table_x2+1.1*self.radius:
                                    self.dx, self.dy = self.velocity, 0
                                    self.move()
                                    distance += sqrt(self.dx**2 + self.dy**2)
                                # Bate pela esquerda
                                elif x < table_x1-1.1*self.radius and table_y1-1.1*self.radius <= y <= table_y2+1.1*self.radius:
                                    self.dx, self.dy = 0, self.velocity
                                    self.move()
                                    distance += sqrt(self.dx**2 + self.dy**2)
                                # Bate pelo direito
                                elif x > table_x2+1.1*self.radius and table_y1-1.1*self.radius <= y <= table_y2+1.1*self.radius:
                                    self.dx, self.dy = 0, -self.velocity
                                    self.move()
                                    distance += sqrt(self.dx**2 + self.dy**2)'''

                # Voltar a uma docking station e terminar a tarefa
                elif task[0] == "TERMINATETASK":
                    dock_dist = None
                    dock = None

                    # Verifica qual a docking station mais perto
                    for o in obstacles:
                        if isinstance(o, DockingStation):
                            ds_x, ds_y = o.get_center().getX(), o.get_center().getY()
                            x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()
                            dist = sqrt((x-ds_x)**2 + (y-ds_y)**2)
                            if dock_dist is None:
                                dock_dist = dist
                                dock = o
                            elif dist < dock_dist:
                                dock_dist = dist
                                dock = o

                    target_x, target_y = dock.get_center().getX(), dock.get_center().getY()
                    x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

                    vec = [target_x-x, target_y-y]
                    norm = sqrt(vec[0]**2 + vec[1]**2)
                    
                    if norm >= self.velocity:
                        self.dx, self.dy = self.velocity*vec[0]/norm, self.velocity*vec[1]/norm
                    else:
                        self.dx, self.dy = vec[0], vec[1]
                        if isinstance(task[1], Table.Circular):
                            # Garantir que o robot fica imobilizado na docking station
                            self.dx, self.dy = 0, 0
                            self.task_tracker += 1
                        elif isinstance(task[1], Table.Rectangular):
                            # Garantir que o robot fica imobilizado na docking station
                            self.dx, self.dy = 0, 0
                            self.task_tracker += 1
                        elif isinstance(task[1], Point):
                            # Garantir que o robot fica imobilizado na docking station
                            self.dx, self.dy = 0, 0
                            self.task_tracker += 1

                # O robot entrou em modo poupanca de energia e guardou a pouca energia q tem para ir carregar-se a docking station
                elif task[0] == "CHARGE":
                    dock_dist = None
                    dock = None

                    # Verifica qual a docking station mais perto
                    for o in obstacles:
                        if isinstance(o, DockingStation):
                            ds_x, ds_y = o.get_center().getX(), o.get_center().getY()
                            x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()
                            dist = sqrt((x-ds_x)**2 + (y-ds_y)**2)
                            if dock_dist is None:
                                dock_dist = dist
                                dock = o
                            elif dist < dock_dist:
                                dock_dist = dist
                                dock = o

                    target_x, target_y = dock.get_center().getX(), dock.get_center().getY()
                    x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

                    vec = [target_x-x, target_y-y]
                    norm = sqrt(vec[0]**2 + vec[1]**2)
                    
                    if norm >= self.velocity:
                        self.dx, self.dy = self.velocity*vec[0]/norm, self.velocity*vec[1]/norm
                    else:
                        self.dx, self.dy = vec[0], vec[1]
                        self.distance = 0
                        sleep(2)
                        self.battery.charge()
                        self.task_tracker += 1


    def check_collision(self, obstacles):
        '''Metodo que deteta colisoess'''
        x, y = self.robot.getCenter().getX(), self.robot.getCenter().getY()

        for o in obstacles:

            # Codigo de colisao com mesas circulares
            if type(o) == Table.Circular:
                next_x, next_y = x+self.dx, y+self.dy
                table_x, table_y = o.get_center().getX(), o.get_center().getY()
                next_dist = sqrt((next_x-table_x)**2 + (next_y-table_y)**2)
                norm = sqrt((x-table_x)**2 + (y-table_y)**2)

                if next_dist <= o.get_radius()+1.1*self.radius:
                    self.dx = self.velocity * (table_y-y) / norm 
                    self.dy = -self.velocity * (table_x-x) / norm

            # Codigo de colisao com mesas rectangulares
            elif type(o) == Table.Rectangular:
                table_x1, table_y1 = o.get_p1().getX(), o.get_p1().getY()
                table_x2, table_y2 = o.get_p2().getX(), o.get_p2().getY()

                #print(f"(xx) {table_x1-1.1*self.radius} <= {x+self.dx} <= {table_x2+1.1*self.radius}")
                #print(f"(yy) {table_y1-1.1*self.radius} <= {y+self.dy} <= {table_y2+1.1*self.radius}")
                # Robot colide
                if table_x1-1.1*self.radius <= x+self.dx <= table_x2+1.1*self.radius and table_y1-1.1*self.radius <= y+self.dy <= table_y2+1.1*self.radius:
                    
                    # Bateu com o lado direito da mesa
                    if x > table_x2 and table_y1-1.1*self.radius <= y <= table_y2+1.1*self.radius:
                        self.dx, self.dy = 0, -self.velocity
                            
                    # Bateu com o lado esquerdo da mesa
                    elif x < table_x1 and table_y1-1.1*self.radius <= y <= table_y2+1.1*self.radius:
                        self.dx, self.dy = 0, self.velocity

                    # Bateu com o lado de baixo da mesa
                    elif y > table_y2 and table_x1-1.1*self.radius <= x <= table_x2+1.1*self.radius:
                        self.dx, self.dy = self.velocity, 0

                    # Bateu com o lado de cima da mesa
                    elif y < table_y2 and table_x1-1.1*self.radius <= x <= table_x2+1.1*self.radius:
                        self.dx, self.dy = -self.velocity, 0


    def move(self):
        '''Metodo que movimenta o robot'''
        self.robot.move(self.dx, self.dy)
        self.battery.move(self.dx, self.dy)

        self.distance += sqrt((self.dx)**2 + (self.dy)**2)

        if self.battery.evaluate_distance(self.distance, 4*(self.room_resolution[0]+self.room_resolution[1])):
            self.tasks.insert(self.task_tracker, ["CHARGE"])
            pass


    def add_task(self, task):
        '''Metodo que adiciona tarefas ao robot'''
        self.tasks.append(task)


    def draw(self, win):
        '''Metodo que desenha o robot no ecra'''
        self.robot.draw(win)
        self.battery.draw(win)


    def undraw(self):
        '''Metodo que apaga o robot do ecra'''
        self.battery.undraw()
        self.robot.undraw()
