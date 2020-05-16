
import tkinter as tk
import time
from time import sleep
from tkinter import *
from tkinter import filedialog
import json
import itertools
from heapq import heappush, heappop, heapify
globallayers = 1
board = []
old = []
Walls = 0
Wallist = set()
root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=600)
canvas.config(bg="white")

l = Label(root, text="Enter Grid Amount:")
l.grid(row=2, column=0)
mt = Label(root, text="First pick a grid size")
mt.grid(row=5, column=0)
m = Label(root, text="Left click to add Walls,")
m.grid(row=6, column=0)
mm = Label(root, text="Right click to toggle auto Walls on and off,")
mm.grid(row=7, column=0)
mmm = Label(root, text=" and press start to start the pathfinder")
mmm.grid(row=8, column=0)
mmmm = Button(root, text="Start", command=lambda:pathfind(board), state = "disabled")
mmmm.grid(row=9, column=0)
g = Button(root, text="Create Grid", command=lambda: creategrid(500, textvar.get()))
g.grid(row=4, column=0)
textvar = StringVar()
e = Entry(root, textvariable=textvar)
e.grid(row=3, column=0)
canvas.grid(row=0, column=1, rowspan=15)
canvas.old_coords = None
canvas.coord_db = []
canvas.lastline = []
Walls = 0
def start():
    roundedlisttemp = []
    global removefromroundedintersect
    canvas.create_line(50, 50, 550, 50)
    canvas.create_line(50, 550, 550, 550)
    canvas.create_line(50, 50, 50, 550)
    canvas.create_line(550, 50, 550, 550)
def creategrid(size, layers):
    for item in layers:
        if item not in ["0","1","2","3","4","5","6","7","8","9"]:
            layers = 10
    else:
        layers = int(layers)
    global globallayers
    globallayers = layers
    global removefromroundedintersect
    canvas.old_coords = None
    roundedlisttemp = []
    x = size + 50
    y = 50
    listtemp = []
    while x >= (size) / layers - 50:
        while y <= size + 50:
            canvas.create_line(x, y, 50, y)
            y += size / layers
        x -= size / layers

    x = size + 50
    y = 50
    while x >= size / layers - 50:
        while y <= size + 50:
            canvas.create_line(y, x, y, 50)
            y += size / layers
        x -= size / layers
    g["state"] = "disabled"
    e["state"] = "disabled"
    fill(0, 0, "green")
    fill(globallayers - 1, globallayers - 1, "red")
    global board
    board = [[0 for y in range(globallayers)] for x in range(globallayers)]
    mmmm["state"]= 'normal'
def mousefunctionhelper(event):
    global Walls
    Walls = 1
    mousefunction(event)
    Walls = 0
def mousefunction(event):
    x = event.x
    y = event.y
    newx = ((x-50))//(500/globallayers)
    newy = (y-50)//(500/globallayers)
    if Walls == 1 and newx >= 0 and newy >=0 and newx<globallayers and newy<globallayers and (newx, newy) != (0,0) and (newx,newy) != (globallayers-1, globallayers-1):
        u["state"] = "normal"
        fill(newx, newy, "black")
        global board
        board[int(newx)][int(newy)] = 999
        Wallist.add((newx,newy))
        global old
        old.append((newx, newy))
def fill(x,y, color):
    x = x + 0.0
    y = y + 0.0
    canvas.create_rectangle(50 + (500 * x)/globallayers, 50 + (500 * y)/globallayers, 50 + (500 * (x+1))/globallayers, 50 + (500 * (y+1))/globallayers, fill=color)
def setWalls(event):
    global Walls
    if Walls == 1: Walls = 0
    else: Walls = 1
def reset():
    global Wallist
    for item in range(0,globallayers):
        for item2 in range(0,globallayers):
          if( (item,item2) != (0,0) and (item, item2) != (globallayers-1, globallayers-1)):
            fill(item, item2, "white")
    Wallist = set()
    global board
    board = [[0 for y in range(globallayers)] for x in range(globallayers)]
    u["state"] = "disabled"

def removelast():
    global old
    fill(old[len(old)-1][0], old[len(old)-1][1], "white")
    global board
    board[int(old[len(old)-1][0])][int(old[len(old)-1][1])] = 0
    old = old[:len(old)-1:]
    if len(old) == 0:
        u["state"] = "disabled"
def dist(a,b,c,d):
    return ((c-a)**2 + (d-b)**2)**.5
def nextto(pos): # this function checks in every direction and adds a tuple of the index to a list that it returns if the direction is viable
    l = []
    global board
    if pos[0] > 0 and board[pos[0]-1][pos[1]] == 0: # checks if row is not zero, and if so adds the spot in the same column but one row above to our list
        l.append((pos[0]-1, pos[1]))
    if pos[1] > 0 and board[pos[0]][pos[1]-1] == 0:
        l.append((pos[0], pos[1]-1))
    if pos[0] < globallayers-1 and board[pos[0]+1][pos[1]] == 0:
        l.append((pos[0]+1, pos[1]))
    if pos[1] < globallayers-1 and board[pos[0]][pos[1]+1] == 0:
        l.append((pos[0], pos[1]+1))
    return l #returns a list of all the indicies next to pos
def pathfind(board):
    q = []
    cS = []
    dict = {}
    q.append((dist(0,0,globallayers-1,globallayers-1), (0,0)))
    while(len(q) != 0):
        current = heappop(q)
        if current[1] == (globallayers-1, globallayers-1):
            curr = current
            while curr[1]!= (0,0):
                if curr[1] != (globallayers-1, globallayers-1) and curr[1] != (0,0):
                  fill(curr[1][0], curr[1][1], "pink")
                curr = dict[curr]
            #fill(0,0, "green")
            return
        for item in nextto(current[1]):
            bool = 0
            num = 0
            for index, coord in enumerate(q):
                if coord[1] == item:
                    num = index
                    bool = 1
            bool2 = 0
            num2 = 0
            for index2, coord2 in enumerate(cS):
                if coord2[1] == item:
                    num2 = index
                    bool2 = 1
            if bool == 1:
                if q[num][0] <= 1 + current[0]: continue
            elif bool2 == 1:
                if q[num][0] <= 1 + current[0]: continue
                else:
                    cS = cS[:num2:] + cS[num2 +1::]
                    heappush(q, (1 + current[0], item))
            else:
                if(item!= (0,0) and item != (globallayers-1, globallayers-1)):
                    fill(item[0], item[1], "blue")

                heappush(q,(dist(item[0], item[1], globallayers-1, globallayers-1), item))
                if (dist(item[0], item[1], globallayers-1, globallayers-1), item) not in dict:
                    dict[(dist(item[0], item[1], globallayers-1, globallayers-1), item)] = current
        cS.append(current)
        #time.sleep(1)
canvas.bind("<Button-1>",mousefunctionhelper)
canvas.bind("<Button-3>", setWalls)
b = Button(root, text="reset", command=lambda:reset())
b.grid(row=0, column=0)
u = Button(root, text="undo", command=removelast, state = "disabled")
u.grid(row=1, column=0)
root.bind("<Motion>", mousefunction)
start()
root.mainloop()
