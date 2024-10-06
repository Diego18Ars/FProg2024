'''
file_reader.py

Realizado por (GRUPO 44):
    Diego Araujo (No. 110050)
    Francisco Afonso (No. 109466)

Módulo que contém a classe que lê os ficheiros .txt    

IST - LEMec - 2023/2024
'''





class FileReader:  
    '''Classe que lê e interpreta o ficheiro de texto a utilizar na terceira implementação'''

    def __init__(self, filepath):
        self.plan = open(filepath, 'r')
        self.plan.readline()
        self.size = (self.plan.readline().split())
        self.plan.readline()
        self.docking_station()
        self.table()
        self.coordinates()
        self.plan.close()
        #print(self.size[0])
        #print(self.size[1])

    def docking_station(self):
        '''Método que lê e armazena os dados relativos às docking stations'''
        ds1p = self.plan.readline()   #ds1p = docking station one (point)
        ds2p = self.plan.readline()   #ds2p = docking station two (point)
        ds1p = ds1p[15:-1] #lê desde o caracter 22 até ao final, desprezando o \n e os () finais
        ds2p = ds2p[15:-1]
        self.dspoints = []
        self.dspoints.append(ds1p)
        self.dspoints.append(ds2p)
        #print(self.dspoints[0])
        #print(self.dspoints[1])
        
    def table(self):
        '''Método que lê e armazena os dados relativos às mesas'''
        self.TableList = []        
        for line in self.plan.readlines():
            shp = line[6:10] #shp = formato (shape) da mesa 
            self.TableList.append(shp)
            
            if shp == "Circ":
                tablexy = line[13:-2] #lê desde o caracter 14 até ao final, desprezando o \n e os () finais
                self.TableList.append(tablexy)
                # adicionam as coordenadas das mesas à lista de mesas

            elif shp == "Rect":
                tablexy = line[16:-2] #lê desde o caracter 17 até ao final, desprezando o \n e os () finais
                self.TableList.append(tablexy)
                # adicionam as coordenadas das mesas à lista de mesas

    def coordinates(self):
        '''Função que armazena as coordenadas das mesas numa lista de coordenadas'''
        self.XYList = []
        null = 0
        self.XYList.append(null)
        l = len(self.TableList)
        
        for i in range(0, l, 2):
            if self.TableList[i] == "Rect":
                self.XYList.append(self.TableList[i])
                coordx, coordy = eval(self.TableList[i+1])
                self.XYList.append(int(coordx)), self.XYList.append(int(coordy))
                #print(self.TableList[i+1])
                #print(coordx)
                #print(coordy)

            else:
                self.XYList.append(self.TableList[i])
                coordx, coordy = eval(self.TableList[i+1])
                self.XYList.append(int(coordx)), self.XYList.append(int(coordy))
                #print(self.TableList[i+1])
                #print(coordx)
                #print(coordy)
        #print(self.XYList)
    def return_values(self):
        '''Método que devolve os valores armazenados'''
        return self.size, self.dspoints, self.TableList, self.XYList
'''
def main():
    fr = FileReader("Sala01.txt")
main()
'''