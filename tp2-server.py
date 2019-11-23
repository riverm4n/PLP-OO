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
from Tkinter import *
import random

HOST = '127.0.0.1' #hostname, in this case, localhost
PORT = 7777

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
        x = col * self.cell_h
        y = lin * self.cell_w
        self.controller[lin][col] = 1

        print("Grid status: \n")
        for i in range(0, len(self.controller)):
            print(self.controller[i])

        return self.w.create_oval(x + 10, y + 10, x + self.cell_w - 10, y + self.cell_h - 10, fill = 'blue', outline = '')

class Geometrics:
    def __init__(self, grid, id = random.randrange(0, 1000), x = 10, y = 10, color = "black"):
        self.grid  = grid
        self.id    = id
        self.x     = x
        self.y     = y
        self.color = color

    # Abstract methods:
    def draw(self, lin, col):
        pass

    def area(self):
        pass

    # Getters and Setters:
    def get_xy(self):
        return [self.x, self.y]

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def remove(self):
        self.grid.delete(self.id)

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
        # m id lin col
        # + shape(c|s) color lin col
        # - shape(c|s) color
        # m shape(c|s) color lin col

        reply = 'Done! \n'
        self.grid.draw_circle(2, 2)
        return reply

    def run(self):
        while True:
            try:
                text = self.client.recv(1024)
                print(text)
                reply = self.process_cmd(text)
                self.client.sendall(reply)
            except:
               print("try again")
               break
        
        self.client.close()

if __name__ == '__main__':
    root = Tk()
    root.title('Grid World')
    grid = Grid(root, 5, 5, cell_h = 60, cell_w = 60)
    app  = Server(grid).start()
    print ('Server running on ' + str(HOST) + ' on port ' + str(PORT))
    root.mainloop()