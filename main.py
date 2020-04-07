# reference
# https://www.geeksforgeeks.org/a-search-algorithm/

#make sure if the user's environment is all set
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

from collections import defaultdict
import heapq

screen = pygame.display.set_mode((800, 800))


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
        # cost start out with 1 because getting to start point takes one step
        self.cost = 1

    def show(self, color, size):
        if not self.closed:
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), size)
            pygame.display.update()

    def addNeighbors(self):
        # add 4 neighbors (four directions only (right, left, top, bottom)) to current node
        i = self.i
        j = self.j

        # 0 and 49 are on the grid but don't have neighbours as their neighbours are out of range
        if i < cols-1 and grid[i + 1][j].block == False:
            self.neighbors.append(grid[i + 1][j])
        if i > 0 and grid[i - 1][j].block == False:
            self.neighbors.append(grid[i - 1][j])
        if j < row-1 and grid[i][j + 1].block == False:
            self.neighbors.append(grid[i][j + 1])
        if j > 0 and grid[i][j - 1].block == False:
            self.neighbors.append(grid[i][j - 1])


cols = 50
row = 50
grid = [[0 for i in range(cols)] for i in range(row)]
openSet = []
closedSet = set()
path = set()
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
white = (255,255,255)
w = 800 // row # 16
h = 800 // cols # 16
cameFrom = []


# Create Spots
# display each coordinate
for i in range(cols):
    for j in range(row):
        grid[i][j] = spot(i, j)
        grid[i][j].show((255, 255, 255), 1)


# get 4 neighbours (right, left, top, bottom) to each coordinate
for i in range(cols):
    for j in range(row):
        grid[i][j].addNeighbors()

# create menu
class Menu:
    def __init__(self):
        self.root = Tk()
        self.root.title("Path finding vizualization")
        # w = Label(self.root, text='Please submit cordinates of stard and end points!')
        # w.place()
        # message = Entry(self.root,text="Please submit cordinates where you would like to start").pack()
        label = Label(self.root, text='Start Coordinate(x,y): ')
        self.startBox = Entry(self.root)
        label1 = Label(self.root, text='End Coordinate(x,y): ')
        self.endBox = Entry(self.root)
        var = IntVar()
        showPath = Checkbutton(self.root, text='Show Steps :', onvalue=1, offvalue=0, variable=var)

        # Submit(startBox,endBox)
        # you cannot pass in startbox as it only passes ".!entry",
        submit = Button(self.root, text='Submit',command=self.Submit)

        showPath.grid(columnspan=2, row=2)
        submit.grid(columnspan=2, row=3)
        label1.grid(row=1, pady=3)
        self.endBox.grid(row=1, column=1, pady=3)
        self.startBox.grid(row=0, column=1, pady=3)
        label.grid(row=0, pady=3)

        # Processes all pending events, calls event callbacks,
        # completes any pending geometry management,
        # redraws widgets as necessary,
        # and calls all pending idle tasks.
        self.root.update()

    def Submit(self):
        # print(self.startBox)
        s = self.startBox
        e = self.endBox
        global st
        global ed
        st = s.get().split(',')
        ed = e.get().split(',')
        # start and end coordinates
        # self.start = grid[int(st[0])][int(st[1])]
        # self.end = grid[int(ed[0])][int(ed[1])]
        self.start = grid[int(st[0])][int(st[1])] # [10,10]
        self.end = grid[int(ed[0])][int(ed[1])]
        self.root.quit()
        self.root.destroy()

# class Result:
#     def __init__(self,res):
#         self.res = res


menu = Menu()
mainloop()

# display start point
menu.start.show((255, 8, 127), 0)
menu.end.show((255, 8, 127), 0)

# put the starting node on the open
openSet.append(st)


def Mouse_Path(x,y):

    x = x // w
    y = y // h
    # fill grid
    grid[x][y].show(white,0) # how to fill each grid
    cur_loc = grid[x][y]
    if not cur_loc.block:
    #if (x,y) not in closedSet:
        # current location is marked as blocked
        cur_loc.block = True
        closedSet.add((x, y))

def Result_popup(res):
    Tk().wm_withdraw()
    messagebox.askokcancel('Program Finished', (
            'The program finished, the shortest distance \n to the path is ' + str(
        res) + ' blocks away, \n would you like to re run the program?'))

def show_path():
    for x,y in path:
        grid[x][y].show(blue, 0)


#m = Mouse_Path

def dijkstra():

    # how to keep track of fastest way

    r,c = int(st[0]),int(st[1])
    heap = [(0,r,c)]  # first verex has no cost
    surroundings = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
    #dic = defaultdict(list)

    while heap:

        dst,r,c = heapq.heappop(heap)  # spit the vertex with smallest cost(path)

        if r == int(ed[0]) and c == int(ed[1]):
            #print(closedSet)
            # including end coordinate so plus 1
            show_path()
            return Result_popup(dst+1)

        if r != int(st[0]) and c != int(st[1]):
            path.add((r, c))
        grid[r][c].show(green, 0)
        grid[r][c].has_neighbor = True
        # get surroundings
        for sur in surroundings:
            new_r = r+sur[0]
            new_c = c+sur[1]
            if 0 <= new_r < row and 0 <= new_c < cols and (new_r,new_c) not in closedSet:
                #grid[new_r][new_r].show(green, 0)
                #dic[dst].append([new_r,new_c])
                closedSet.add((new_r,new_c))
                heapq.heappush(heap, (dst+1, new_r, new_c))


def DFS():
    r,c = st
    cnt = 0
    res = dfs(int(r),int(c),cnt)

    # root probably should be outside of constructor
    # originally, I thought I was gonna call root (global) here but it is in a constructor so i can't
    # but created a helper function to solve this problem
    Result_popup(res)



#print(ed[0],ed[1])
def dfs(r, c,cnt):

    ### if start and end is too far,

    # check if current cell is valid cell
    # program returns [Previous line repeated 992 more times] and crashes
    # base case, constraints
    #print(r,c)
    if 0 > r or r >= row or 0 > c or c >= cols or (r, c) in closedSet:
        return False

    #print(r,c)
    if r == int(ed[0]) and c == int(ed[1]):

        return cnt

    closedSet.add((r, c))
    grid[r][c].show(green,0)
    return dfs(r + 1, c, cnt+1) or dfs(r, c+1, cnt+1) or dfs(r-1, c, cnt+1) or dfs(r, c - 1, cnt+1)


# pygame initiate
pygame.init()

def main():

    """
    algorithm
    1,
    :return:
    """

    while openSet:
        least_f = float('inf')
        # find the node with the least f
        # ‘f’ which is a parameter equal to the sum of two other parameters – ‘g’ and ‘h’
        for i in range(len(openSet)):
            if openSet[i].f < least_f:
                least_f = i

        q = openSet.pop(i)



# detect mouse coordinate
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # if user takes any mouse related actions
        #if event.type == pygame.MOUSEBUTTONDOWN:

        # mouse.get_pressed()[0] denotes left click
        if pygame.mouse.get_pressed()[0]:
            # get mouse current coordinate
            Mouse_x, Mouse_y = pygame.mouse.get_pos() #  # how to get current position
            cur_x = int(Mouse_x) // w
            cur_y = int(Mouse_y) // h

            # not to override start point and end point
            # if cur_x != int(st[0]) and cur_x != int(st[1]) and cur_x != int(ed[0]) and cur_x != int(ed[1]) and cur_y != int(st[0]) and cur_y != int(st[1]) and \
            #     cur_y != int(ed[0]) and cur_y != int(ed[0]):

            #print(Mouse_x,Mouse_y)
            #print(a,b)
            #Mouse_Path(Mouse_x,Mouse_y)
            # fill a,b with white
            Mouse_Path(Mouse_x,Mouse_y)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #print(closedSet)
                loop = False
                #DFS()
                dijkstra()
                break
        # when left click is not pressed any more
        # go to DFS

    pygame.display.update()


# import tkinter as tk
# import pygame
#
# # tk how to put widgt together
# # pack,
#
# H = 1200
# W = 800
# # to do list
# # create tile
#
# root = tk.Tk()
#
# class PathVisualization:
#     def __init__(self,H,W):
#         self.h = H
#         self.w = W
#
#     def create_frame(self):
#         # frame
#         canvas = tk.Canvas(root, height=self.h, width=self.w)
#         canvas.pack()

# class Mouse_Path:
#     def __init__(self,x,y):
#         # 0 denotes open, 1 denotes close
#         # self.path = [[0 for _ in range(cols)] for _ in range(row)]
#         self.x = x
#         self.y = y
#
#     def Visualizze_path(self):
#
#         # 2 ideas to check if next coordinate is an blocktacle or not,
#         # create 2d array, 0 denotes not 1 denotes it is,
#         # or create another array and put coordinator as tuple
#         # how can i access
#
#         grid[self.x][self.y].show(white,1)

# PathVisualization(H,W)
