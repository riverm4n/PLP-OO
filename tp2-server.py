# ======================================================================================== #
# -*- coding: utf-8 -*-                                                                    #
# Trabalho Pratico 2 de Paradigmas de Linguagens de Progracao, questao 7 da lista.         #
#                                         Descrição:                                       #
# Implemente um servidor socket em Python OO para manipulação de figuras geométricas em um #
# grid gráfico em ambiente X. Seu servidor deve iniciar um grid de 5x5 células, como visto #
# na figura abaixo e epserar por requisições para criação, remoção e movimentação de figu- #
# ras. Mais especificamente, o servidor deve reconhecer os seguintes comandos enviados por #
# clientes socket:                                                                         #
#   >> + id F C X Y: criar figura com identificador id(inteiro), forma F (s para quadrado e#
#      c para círculo), cor C (pelo menos black, red, green e blue) e coordenadas X e Y    #
#      (inteiros de 0 a 4).                                                                #
#   >> - id: apagar figura identificada por F C.                                           #
#   >> m F C X Y: mover figura identificada por F C para coordenadas X e Y.                #
# ======================================================================================== #

from socket import *
from threading import *
from tkinter import *
import random

HOST = '127.0.0.1' #hostname, in this case, localhost
PORT = 7778

class Grid:
    def __init__(self, master, lins, cols, cell_h = 50, cell_w = 50):
        self.cell_h  = cell_h
        self.cell_w  = cell_w
        self.maxlins = lins
        self.maxcols = cols
        
        h = lins * cell_h + 1
        w = cols * cell_w + 1

        # Possible slots controller
        self.controller = [[0 for x in range(lins)] for y in range(cols)]

        self.w = Canvas(master, height = h, width = w)
        self.w.configure(borderwidth=0, highlightthickness=0)
        self.w.pack()

        for i in range(0, h, cell_h):
            self.w.create_line([(i, 0), (i, h)])
        for i in range(0, w, cell_w):
            self.w.create_line([(0, i), (w, i)])

    def draw_circle(self, lin, col):
        circle = Circle(self, 20, lin, col, 'blue')

        self.controller[lin][col] = circle.get_id()
        
        print("Grid status: \n")
        for i in range(0, len(self.controller)):
            print(self.controller[i])

        print(circle.__repr__())
        circle.draw(lin, col)
        self.w.pack()

    def draw_square(self, lin, col):
        square = Square(self, 15, lin, col, 'red')
        self.controller[lin][col] = square.get_id()

        print("Grid status: \n")
        for i in range(0, len(self.controller)):
            print(self.controller[i])

        print(square.__repr__())
        square.draw(lin, col)
        self.w.pack()

class Geometrics:
    '''
    Implements a 2D geometric figure using TK
    '''
    def __init__(self, grid, id = random.randrange(0, 1000), x = 10, y = 10, color = "black"):
        self.grid  = grid
        self.id    = id
        self.x     = x
        self.y     = y
        self.color = color

    # Abstract methods:
    def draw(self):
        pass

    # Getters and Setters:
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def get_id(self):
        return self.id

    def remove(self):
        self.grid.delete(self.id)

    def move(self, x, y):
        self.remove()
        self.set_xy(x, y)
        self.draw()

class Circle(Geometrics):
    '''
    Implements a 2D circle using TK
    This class inherits the behaviour of the Geometrics class
    '''    
    def __init__(self, grid, id = random.randrange(0, 1000), x = 0, y = 0, color = "black"):
        super().__init__(grid, id, x, y, color)

    def __repr__(self):
        # Circle representation
        return 'Circle at (' + str(self.x) + ', ' + str(self.y) + ').'

    def draw(self, lin, col):
        x = col * self.grid.cell_h
        y = lin * self.grid.cell_w
        self.grid.controller[lin][col] = self.id

        return self.grid.w.create_oval(x + 10, y + 10, x + self.grid.cell_w - 10, y + self.grid.cell_h - 10, fill = self.color, outline = '')
    
class Square(Geometrics):
    '''
    Implements a 2D square using TK
    This class inherits the behaviour of the Geometrics class
    '''
    def __init__(self, grid, id = random.randrange(0, 1000), x = 0, y = 0, color = "black"):
        super().__init__(grid, id, x, y, color)

    def __repr__(self):
        # Square representation
        return 'Square at (' + str(self.x) + ', ' + str(self.y) + ').'

    def draw(self, lin, col):
        x = col * self.grid.cell_h
        y = lin * self.grid.cell_w
        self.grid.controller[lin][col] = self.id

        return self.grid.w.create_rectangle(x + 10, y + 10, x + self.grid.cell_w - 10, y + self.grid.cell_h - 10, fill = self.color, outline = '')

class Server(Thread):
    def __init__(self, grid):
        Thread.__init__(self)
        self.grid = grid
        
        self.server = socket()
        self.server.bind((HOST, PORT))

        self.server.listen(5)

        self.client, addr = self.server.accept()

    def process_cmd(self, cmd):
        # + id shape(c|s) color lin col
        # - id
        # m id lin cold
        # + shape(c|s) color lin col
        # - shape(c|s) color
        # m shape(c|s) color lin col

        reply = 'Done! \n'
        self.grid.draw_circle(0, 2)
        self.grid.draw_square(2, 1)
        return reply

    def run(self):
        while True:
            try:
                text = self.client.recv(1024)
                print(text)
                reply = self.process_cmd(text)
                self.client.sendall(reply.encode())
            except:
               print("Please, try again")
               break
        
        self.client.close()

if __name__ == '__main__':
    root = Tk()
    root.title('Grid World')
    grid = Grid(root, 5, 5, cell_h = 60, cell_w = 60)
    app  = Server(grid).start()
    print ('Server running on ' + str(HOST) + ' on port ' + str(PORT))
    root.mainloop()