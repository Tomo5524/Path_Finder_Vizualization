import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import timeit
import time
import heapq

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255, 255, 255))


class spot:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = set()
        self.previous = None
        self.block = False
        self.closed = False
        self.opened = False
        self.value = 1
        self.visited = False

    def draw_line(self, color, st):
        # create cases for 8 directions
        if self.previous:
            pre_loc = grid[self.i][self.j].previous
            r = pre_loc.i * (WIDTH // row)
            c = pre_loc.j * (HEIGHT // cols)
            # r,c = self.i,self.j
            cur_loc_x = self.i * (WIDTH // row)
            cur_loc_y = self.j * (HEIGHT // cols)

            pygame.draw.line(screen, color, (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y + (HEIGHT // cols) // 2),
                             (r + ((WIDTH // row) // 2), c + (HEIGHT // cols) // 2), st)

            pygame.display.update()

    def show(self, color, size):

        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), size)
        pygame.display.update()

    def show_open_and_closed(self, color, size):
        # plus and minus 1 to show margin
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w - 1, h - 1), size)
        pygame.display.update()

    def is_diagonally_walkable(self, x, y):
        if (self.i, self.j) == (x - 1, y + 1) and grid[x - 1][y].block and grid[x][y + 1].block:
            return True

        elif (self.i, self.j) == (x + 1, y + 1) and grid[x + 1][y].block and grid[x][y + 1].block:
            return True

        elif (self.i, self.j) == (x + 1, y - 1) and grid[x + 1][y].block and grid[x][y - 1].block:
            return True

        elif (self.i, self.j) == (x - 1, y - 1) and grid[x - 1][y].block and grid[x][y - 1].block:
            return True

        return False


cols = 50
row = 50
openSet = []
closedSet = []
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
yellow = (255, 255, 0)
light_black = (70, 70, 70)
light_blue = (0, 255, 255)
black = (0, 0, 0)
w = WIDTH // cols
h = HEIGHT // row

# create 2d array
grid = [[0 for i in range(cols)] for i in range(row)]

# Create Spots
# create node for each coordinate
# SHOW RECT
for i in range(cols):
    for j in range(row):
        grid[i][j] = spot(i, j)
        grid[i][j].show(black, 1)

# to create frame around screen
for i in range(0, row):
    grid[0][i].show(grey, 0)
    grid[0][i].block = True
    grid[cols - 1][i].block = True
    grid[cols - 1][i].show(grey, 0)
    grid[i][row - 1].show(grey, 0)
    grid[i][0].show(grey, 0)
    grid[i][0].block = True
    grid[i][row - 1].block = True


def onsubmit():
    # make start and end node global
    global start
    global end
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()


window = Tk()
label = Label(window, text='Start(x,y): ')
startBox = Entry(window)
label1 = Label(window, text='End(x,y): ')
endBox = Entry(window)
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)
submit = Button(window, text='Submit', command=onsubmit)

showPath.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)

window.update()
mainloop()

pygame.init()


def mousePress(x):
    t = x[0]
    w = x[1]
    g1 = t // (WIDTH // cols)
    g2 = w // (HEIGHT // row)
    acess = grid[g1][g2]
    if acess != start and acess != end:
        if acess.block == False:
            acess.block = True
            acess.show(light_black, 0)


# push start node to a list
openSet.append([float('inf'), start.i, start.j])
start.seen = True
end.show((255, 8, 127), 0)
start.show((255, 8, 127), 0)

loop = True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break


def heurisitic(n, e):
    d = math.sqrt((n.i - e.i) ** 2 + (n.j - e.j) ** 2)
    return d


def Astar_finder():
    start_time = time.time()
    surroundings = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]

    while openSet:

        smallest_f, row, col = heapq.heappop(openSet)
        current = grid[row][col]
        closedSet.append(current)

        for sur in surroundings:
            r = sur[0] + current.i
            c = sur[1] + current.j
            neighbor = grid[r][c]

            # avoid checking duplicates
            if not neighbor.visited:
                neighbor.visited = True
                # g = the movement cost to move from the starting point to a given square on the grid, following the path generated to get there.
                neighbor.g = max(neighbor.g, current.g + 1)
                neighbor.h = heurisitic(neighbor, end)
                # ‘f’ which is a parameter equal to the sum of two other parameters – ‘g’ and ‘h’
                neighbor.f = neighbor.g + neighbor.h
                current.neighbors.add((r, c))
                if neighbor == end:
                    # end's node points to current
                    neighbor.previous = current

                    current.show(light_blue, 0)
                    print("--- %s seconds ---" % (time.time() - start_time))
                    get_steps(neighbor, start_time)

                # check if diagonally walkable
                if not neighbor.block:

                    # if diagonal move is not valid, ignore it and move on
                    if neighbor.is_diagonally_walkable(row, col):
                        continue

                    else:
                        heapq.heappush(openSet, [neighbor.f, neighbor.i, neighbor.j])

                    neighbor.previous = current

        # draw coordinates that are not visited
        for op in openSet:
            cur = grid[op[1]][op[2]]
            if not cur.opened:
                cur.opened = True
                cur.show_open_and_closed(green, 0)

        # draw coordinates that are visited
        for cl in closedSet:
            if cl != start and not cl.closed:
                cl.closed = True
                cl.show_open_and_closed(light_blue, 0)

    # when there is no path from start point to end point
    return []


def No_path():
    Tk().wm_withdraw()
    result = messagebox.askokcancel('Program Finished \n', 'There was no path from start point to end point :(')
    if result == True:
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        ag = True
        while ag:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.KEYDOWN:
                    ag = False
                    break
    pygame.quit()


def get_steps(current, start_time):
    # print('done', current.f)
    start.show((255, 8, 127), 0)
    temp = current.f
    for i in range(round(temp)):
        current.closed = False
        current.draw_line(yellow, 1)
        current = current.previous

    Tk().wm_withdraw()
    result = messagebox.askokcancel('Program Finished', (
            'The program finished, the shortest distance \n to the path is ' + str(
        temp) + ' blocks away, \n This program took ' + str(
        round((time.time() - start_time), 2)) + 'seconds. \n would you like to re run the program?'))

    if result == True:
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        ag = True
        while ag:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.KEYDOWN:
                    ag = False
                    break
    pygame.quit()


while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    Astar_finder()

