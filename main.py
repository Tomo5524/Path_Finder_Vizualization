
try:
    import pygame
    import sys
    import math
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os
except:
    import install_requirements  # install packages

    import pygame
    import sys
    import math
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os


WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255,255,255))


class spot:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.block = False
        self.closed = False
        self.value = 1

    def draw_line(self, color, st):
        # create cases for 8 directions
        pre_loc = grid[self.i][self.j].previous
        r = pre_loc.i * (WIDTH // row)
        c =  pre_loc.j * (HEIGHT // cols)
        #r,c = self.i,self.j
        cur_loc_x = self.i * (WIDTH // row)
        cur_loc_y = self.j * (HEIGHT // cols)

        pygame.draw.line(screen, color, (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y + (HEIGHT // cols) // 2),
                         (r + ((WIDTH // row) // 2),  c + (HEIGHT // cols) // 2), st)

        # end line goes into pre_loc
        # cur_locx and cur_loc_y denotes the topleft of the current grid
        # if pre_loc == grid[r - 1][c -1]:
        #     pygame.draw.line(screen, color, (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y + ((HEIGHT // cols) // 2)),
        #                      (cur_loc_x - ((WIDTH // row) // 2), cur_loc_y - ((HEIGHT // cols) // 2)), st)
        #
        # elif pre_loc == grid[r + 1][c]:
        #     pygame.draw.line(screen, color, (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y + ((HEIGHT // cols) // 2)),
        #                      (cur_loc_x + (WIDTH // row), cur_loc_y + (HEIGHT // cols)), st)
        #
        # elif pre_loc == grid[r - 1][c]:
        #     pygame.draw.line(screen, color, (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y + ((HEIGHT // cols) // 2)),
        #                      (cur_loc_x - (WIDTH // row), cur_loc_y + ((HEIGHT // cols) // 2)), st)
        #
        # elif pre_loc == grid[r + 1][c]:
        #     pygame.draw.line(screen, color, (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y + ((HEIGHT // cols) // 2)),
        #                      (cur_loc_x + (WIDTH // row), cur_loc_y), st)
        #
        # elif pre_loc == grid[r][c - 1]:
        #     pygame.draw.line(screen, color, (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y + ((HEIGHT // cols) // 2)),
        #                      (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y - (HEIGHT // cols)), st)
        #
        # elif pre_loc == grid[r][c + 1]:
        #     pygame.draw.line(screen, color, (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y + ((HEIGHT // cols) // 2)),
        #                      (cur_loc_x, cur_loc_y + (HEIGHT // cols)), st)
        #
        # elif pre_loc == grid[r + 1][c - 1]:
        #     pygame.draw.line(screen, color, (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y + ((HEIGHT // cols) // 2)),
        #                      (cur_loc_x + (WIDTH // row), cur_loc_y - ((HEIGHT // cols) // 2)), st)
        #
        # elif pre_loc == grid[r - 1][c + 1]:
        #     pygame.draw.line(screen, color, (cur_loc_x + ((WIDTH // row) // 2), cur_loc_y + ((HEIGHT // cols) // 2)),
        #                      (cur_loc_x - ((WIDTH // row) // 2), cur_loc_y + (HEIGHT // cols)), st)

        # if i > 0 and grid[self.i - 1][j].block == False:
        #     self.neighbors.append(grid[self.i - 1][j])
        # if j < row - 1 and grid[self.i][j + 1].block == False:
        #     self.neighbors.append(grid[self.i][j + 1])
        # if j > 0 and grid[self.i][j - 1].block == False:
        #     self.neighbors.append(grid[self.i][j - 1])
        #
        # # if there are only 4 neighbors, it is manhattan distance
        # # if there are 8, then that is diagonal
        # if j > 0 and i > 0 and grid[self.i-1][j - 1].block == False:
        #     self.neighbors.append(grid[self.i-1][j - 1])
        # if j < row -1 and i < cols-1 and grid[self.i+1][j + 1].block == False:
        #     self.neighbors.append(grid[self.i+1][j + 1])
        # if j > 0 and i < cols-1 and grid[self.i+1][j - 1].block == False:
        #     self.neighbors.append(grid[self.i+1][j - 1])
        # if j < row -1 and i > 0 and grid[self.i-1 ][j + 1].block == False:
        #     self.neighbors.append(grid[self.i-1][j + 1])

        # cur_loc_x = self.i * (WIDTH//row)
        # cur_loc_y = self.j * (HEIGHT//cols)

        # else:
        #     pygame.draw.line(screen, color, (cur_loc_x, cur_loc_y),(cur_loc_x + (WIDTH//row), cur_loc_y + (HEIGHT//cols)), st)

        pygame.display.update()

    def show(self, color, st):
        if self.closed == False:
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
            pygame.display.update()


    def addNeighbors(self, grid):
        i = self.i
        j = self.j
        if i < cols - 1 and grid[self.i + 1][j].block == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].block == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < row - 1 and grid[self.i][j + 1].block == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].block == False:
            self.neighbors.append(grid[self.i][j - 1])

        # if there are only 4 neighbors, it is manhattan distance
        # if there are 8, then that is diagonal
        if j > 0 and i > 0 and grid[self.i-1][j - 1].block == False:
            self.neighbors.append(grid[self.i-1][j - 1])
        if j < row -1 and i < cols-1 and grid[self.i+1][j + 1].block == False:
            self.neighbors.append(grid[self.i+1][j + 1])
        if j > 0 and i < cols-1 and grid[self.i+1][j - 1].block == False:
            self.neighbors.append(grid[self.i+1][j - 1])
        if j < row -1 and i > 0 and grid[self.i-1 ][j + 1].block == False:
            self.neighbors.append(grid[self.i-1][j + 1])



cols = 50
row = 50
openSet = []
closedSet = []
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
yellow = (255,255,0)
light_black = (70, 70, 70)
w = WIDTH // cols
h = HEIGHT // row
cameFrom = []

# create 2d array
grid = [[0 for i in range(cols)] for i in range(row)]

# Create Spots

for i in range(cols):
    for j in range(row):
        # create node for each coordinate
        grid[i][j] = spot(i, j)
        # SHOW RECT
        grid[i][j].show((0, 0, 0), 1)

# Set start and end node
# start = grid[12][5]
# end = grid[3][6]


# for i in range(cols):
#     for j in range(row):
            #grid[i][j].show((0, 0, 0), 1)


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
openSet.append(start)


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

for i in range(cols):
    for j in range(row):
        grid[i][j].addNeighbors(grid)


def heurisitic(n, e):
    d = math.sqrt((n.i - e.i) ** 2 + (n.j - e.j) ** 2)
    # d = abs(n.i - e.i) + abs(n.j - e.j)
    return d

light_blue = (0, 255, 255)

def main():

    if len(openSet) > 0:
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i

        current = openSet[lowestIndex]
        if current == end:
            print('done', current.f)
            start.show((255, 8, 127), 0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.draw_line(yellow, 1)
                current = current.previous

            #start.draw_line(yellow,1)
            end.show((255, 8, 127), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', (
                        'The program finished, the shortest distance \n to the path is ' + str(
                    temp) + ' blocks away, \n would you like to re run the program?'))
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

        openSet.pop(lowestIndex)
        closedSet.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                #g = the movement cost to move from the starting point to a given square on the grid, following the path generated to get there.
                tempG = current.g + 1
                if neighbor in openSet:
                    # important cuz when seeing bigger g, just break
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)

            # h = the estimated movement cost to move from that given square on the grid to the final destination.
            neighbor.h = heurisitic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous == None:
                neighbor.previous = current

    #if var.get():
    for i in range(len(openSet)):
        openSet[i].show(green, 0)

    for i in range(len(closedSet)):
        if closedSet[i] != start:
            closedSet[i].show((0,255,250), 0)

    current.closed = True


while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()
