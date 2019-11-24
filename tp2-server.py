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
# Using python3:
from tkinter import *
import random

HOST = '127.0.0.1' #hostname, in this case, localhost
PORT = 7777

class Grid:
    def __init__(self, master, lins, cols, cell_h = 50, cell_w = 50):
        self.cell_h  = cell_h
        self.cell_w  = cell_w
        self.maxlins = lins
        self.maxcols = cols
        self.figures = Inventory()
        
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

    def draw_circle(self, lin, col, circle):
        self.controller[lin][col] = circle.get_id()
        self.figures.add_to_list(circle)
        
        print("Grid status: \n")
        for i in range(0, len(self.controller)):
            print(self.controller[i])

        print(circle.__repr__())
        circle.draw(lin, col)
        self.w.pack()

    def draw_square(self, lin, col, square):
        self.controller[lin][col] = square.get_id()
        self.figures.add_to_list(square)

        print("Grid status: \n")
        for i in range(0, len(self.controller)):
            print(self.controller[i])

        print(square.__repr__())
        square.draw(lin, col)
        self.w.pack()

    def delete_figure(self, figure):
        self.controller[figure.get_x()][figure.get_y()] = 0

        print("Figure removed. Grid status: \n")
        for i in range(0, len(self.controller)):
            print(self.controller[i])
        
        figure.remove()
        self.w.pack()

    def move_figure(self, figure, lin, col):
        self.controller[figure.get_x()][figure.get_y()] = 0
        self.controller[lin][col] = figure.get_id()

        print("Figure moved. Grid status: \n")
        for i in range(0, len(self.controller)):
            print(self.controller[i])

        figure.move(lin, col)
        self.w.pack()

        


class Geometrics:
    '''
    Implements a 2D geometric figure using TK
    '''
    def __init__(self, grid, id = random.randrange(0, 50), x = 10, y = 10, color = "black"):
        self.grid  = grid
        self.id    = id
        self.x     = x
        self.y     = y
        self.color = color
        self.shape = None # Image representation

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
        self.grid.w.delete(self.shape)

    def move(self, x, y):
        self.remove()
        self.set_xy(x, y)
        self.draw(x, y)

class Circle(Geometrics):
    '''
    Implements a 2D circle using TK
    This class inherits the behaviour of the Geometrics class
    '''    
    def __init__(self, grid, id = random.randrange(0, 50), x = 0, y = 0, color = "black"):
        super().__init__(grid, id, x, y, color)

    def __repr__(self):
        # Circle representation
        return 'Circle at (' + str(self.x) + ', ' + str(self.y) + ').'

    def draw(self, lin, col):
        x = col * self.grid.cell_h
        y = lin * self.grid.cell_w
        self.grid.controller[lin][col] = self.id

        self.shape = self.grid.w.create_oval(x + 10, y + 10, x + self.grid.cell_w - 10, y + self.grid.cell_h - 10, fill = self.color, outline = '')
        return self.shape
    
class Square(Geometrics):
    '''
    Implements a 2D square using TK
    This class inherits the behaviour of the Geometrics class
    '''
    def __init__(self, grid, id = random.randrange(0, 50), x = 0, y = 0, color = "black"):
        super().__init__(grid, id, x, y, color)

    def __repr__(self):
        # Square representation
        return 'Square at (' + str(self.x) + ', ' + str(self.y) + ').'

    def draw(self, lin, col):
        x = col * self.grid.cell_h
        y = lin * self.grid.cell_w
        self.grid.controller[lin][col] = self.id

        self.shape = self.grid.w.create_rectangle(x + 10, y + 10, x + self.grid.cell_w - 10, y + self.grid.cell_h - 10, fill = self.color, outline = '')
        return self.shape

class Inventory:
    def __init__(self):
        self.figures = list()

    def add_to_list(self, figure):
        self.figures.append(figure)

    def exists(self, lin, col):
        print("Buscando pela posição: " + str(lin) + ", " + str(col))
        for i in range(0, len(self.figures)):
            if self.figures[i].get_x() == lin and self.figures[i].get_y() == col:
                return self.figures[i]

        return None

    def exists_id(self, id):
        print("Verificando se existe a figura com o id " + str(id))
        for i in range(0, len(self.figures)):
            print("dentro do for ")
            if self.figures[i].get_id() == id:
                print("encontrei com o mesmo id!")
                return self.figures[i]
       
        return None

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

        cmd_array = cmd.split()
        print(cmd_array)

        reply = 'Done! \n'

        # cmd size checking:
        # + id shape color lin col
        if(len(cmd_array) == 6):
            #checking commands:
            if cmd_array[0] == b'+':
                if(cmd_array[2] == b'c'):
                    circle = Circle(self.grid, int(cmd_array[1]), int(cmd_array[4]), int(cmd_array[5]), cmd_array[3].decode())
                    self.grid.draw_circle(int(cmd_array[4]), int(cmd_array[5]), circle)
                elif(cmd_array[2] == b's'):
                    square = Square(self.grid, int(cmd_array[1]), int(cmd_array[4]), int(cmd_array[5]), cmd_array[3].decode())
                    self.grid.draw_square(int(cmd_array[4]), int(cmd_array[5]), square)
                else:
                    reply = 'Shape not recognized.'
        elif(len(cmd_array) == 5):
            # + shape color lin col
            if(cmd_array[0] == b'+'):
                if(cmd_array[1] == b'c'):
                    random_id = random.randrange(0,50)
                    circle = Circle(self.grid, random_id, int(cmd_array[3]), int(cmd_array[4]), cmd_array[2].decode())
                    print(circle.__repr__())
                    self.grid.draw_circle(int(cmd_array[3]), int(cmd_array[4]), circle)
                elif(cmd_array[1] == b's'):
                    random_id = random.randrange(0,50)
                    square = Square(self.grid, random_id, int(cmd_array[3]), int(cmd_array[4]), cmd_array[2].decode())
                    self.grid.draw_square(int(cmd_array[3]), int(cmd_array[4]), square)
                else:
                    reply = 'Shape not recognized.'
            # - shape color lin col
            elif(cmd_array[0] == b'-'):
                figure = self.grid.figures.exists(int(cmd_array[3]), int(cmd_array[4]))
                if (figure != None):
                    print(figure.__repr__())
                    self.grid.delete_figure(figure)
                else:
                    reply = 'Sorry, the shape you were looking for was not found.'
        elif(len(cmd_array) == 4):
            # m id lin col
            if(cmd_array[0] == b'm'):
                print("id " + str(int(cmd_array[1])))
                figure = self.grid.figures.exists_id(int(cmd_array[1]))
                if (figure != None):
                    print(figure.__repr__())
                    self.grid.move_figure(figure, int(cmd_array[2]), int(cmd_array[3]))
                else:
                    reply = 'Sorry, the shape you were looking for was not found.'
        elif(len(cmd_array) == 2):
            # - id
            if(cmd_array[0] == b'-'):
                figure = self.grid.figures.exists_id(int(cmd_array[1]))
                if(figure != None):
                    print(figure.__repr__())
                    self.grid.delete_figure(figure)
                else:
                    reply = 'Sorry, the shape you were looking for was not found.'
            else:
                reply = 'Sorry, I didn\'t understand'
        else:
            reply = 'Sorry, I didn\'t understand'

        return reply

    def run(self):
        while True:
            try:
                text = self.client.recv(1024)
                reply = self.process_cmd(text)
                self.client.sendall(reply.encode())
            except:
               print("Something went wrong. Shutting down the server.")
               break
        
        self.client.close()

if __name__ == '__main__':
    root = Tk()
    root.title('Grid World')
    grid = Grid(root, 5, 5, cell_h = 60, cell_w = 60)
    app  = Server(grid).start()
    print ('Server running on ' + str(HOST) + ' on port ' + str(PORT))
    root.mainloop()