from math import cos, acos, pi, sin
import time
from heapq import heappush, heappop, heapify
from tkinter import Tk, Canvas, Frame, BOTH
import sys
counvariable = 0
def calcdist(tuple1, tuple2):
    lat1 = tuple1[0]
    lat2 = tuple2[0]
    long1 = tuple1[1]
    long2 = tuple2[1]
    y1 = lat1
    x1 = long1
    y2 = lat2
    x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    #
    R = 3958.76  # miles = 6371 km
    #
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R


t0 = time.time()
numupdated = 0
count = 0
goal = ["Seattle","Miami"]#sys.argv[1:]
if len(goal)<2:
    print("not enough inputs")
    exit()
file = open("arrNodes.txt", "r")
list1 = file.readlines()
file = open("arrNames.txt", "r")
listt = file.readlines()
file = open("arrEdges.txt", "r")
listtt = file.readlines()
dict1 = {}
dict2 = {}
dict3 = {}
edgesum = 0.0
numimprovements = 0







for string in listt:
    if len(string.split()) == 1:
        dict3[string[0]] = ''.join(string.split())
    else:
        dict3[' '.join(string.split()[1::])] = string.split()[0]
        dict3[string.split()[0]] = ' '.join(string.split()[1::])
path = []
numsteps = 0
for string in list1:
    dict1[string.split()[0]] = (string.split()[1],string.split()[2])
for string in listtt:
  if string.split()[0] in dict2.keys():
      dict2[string.split()[0]].append(string.split()[1])
  else:
      dict2[string.split()[0]] = [string.split()[1]]
  if string.split()[1] in dict2.keys():
      dict2[string.split()[1]].append(string.split()[0])
  else:
      dict2[string.split()[1]] = [string.split()[0]]


for key in dict2.keys():
    for string in dict2[key]:
        edgesum += calcdist(dict1[key], dict1[string])
edgesum = edgesum / 2
kintdict = {}
root = Tk()
canvas = Canvas()

start = ''
end = ''
r = ' '.join(goal[0:2])
if ' '.join(goal[0:2]) in dict3.keys():
    start = ' '.join(goal[0:2])
    if len(goal) == 4:
        end = ' '.join(goal[2:4])
    else:
        end = goal[2]
else:
    start = goal[0]
    if len(goal) == 3:
        end = ' '.join(goal[1:3])
    else:
        end = goal[1]

for string in dict2.keys():
    for stringg in dict2[string]:
      a =(float(dict1[string][1])+145)*10
      b =(-5+float(dict1[string][0]))*10
      c = (float(dict1[stringg][1])+145)*10
      d =(-5+float(dict1[stringg][0]))*10
      canvas.create_line(a,abs(1000-b)-400,c,abs(1000-d)-400)
      canvas.pack(fill=BOTH, expand=.5)
      root.geometry("1000x1000")
#  canvas.create_oval((float(dict1[string][1])-15)*50-5,(130+float(dict1[string][0]))*50-5,(float(dict1[string][1])-15)*50+5,(130+float(dict1[string][0]))*50+5,fill = "#f12")
   #   canvas.create_oval((float(dict1[stringg][1])-15)*50-5,(130+float(dict1[stringg][0]))*50-5,(float(dict1[stringg][1])-15)*50+5,(130+float(dict1[stringg][0]))*50+5,fill = "#f12")







if start not in dict3.keys() :
    if     end not in dict3.keys():
        print("both " + start + " and " + end + " are not cities")
        exit()
    print(start + " is not a city")
    exit()
if end not in dict3.keys():
    print(end + " is not a city")
    exit()
summ = calcdist(dict1[dict3[start]], dict1[dict3[end]])
openSet = [(summ, dict3[start], summ)]
closedSet = {}
while len(openSet) != 0:
    takingLs = heappop(openSet)
    olddist = takingLs[2]
    string = takingLs[1]
    oldsum = takingLs[0]
    count += 1
    if string == dict3[end]:
        totaldist = 0
        print(start)
        while string != dict3[start]:
            path.append(string)
            a = (float(dict1[string][1]) + 145) * 10
            b = (-5 + float(dict1[string][0])) * 10
            c = (float(dict1[closedSet[string]][1]) + 145) * 10
            d = (-5 + float(dict1[closedSet[string]][0])) * 10
            canvas.create_line(a, abs(1000 - b) - 400, c, abs(1000 - d) - 400,fill = "#F012BE")
            string = closedSet[string]
            numsteps += 1
        path = path[::-1]
        for string in path:
            totaldist+=calcdist(dict1[string], dict1[closedSet[string]])
            if string in dict3.keys():
              print(string + " " + str(calcdist(dict1[string], dict1[closedSet[string]])) + " miles, also known as " + dict3[string])
            else:
              print(string + " " + str(calcdist(dict1[string], dict1[closedSet[string]])) + " miles")

        print("number of steps is " + str(numsteps))
        print("Open Set size is " + str(len(openSet)))
        print("Closed Set size is " + str(len(closedSet)))
        t1 = time.time()
        print("time elapsed = " + str((t1 - t0)) + " seconds")
        print("sum of all edges = " + str(edgesum) + " miles")
        print("number of imporvements is " + str(numimprovements))
        print("total distance traveled is " + str(totaldist) + " miles")
        canvas.pack(fill=BOTH, expand=.5)
        root.geometry("1000x1000")
        canvas.pack(fill=BOTH, expand=.5)
        root.geometry("1000x1000")
        root.mainloop()
        exit()
    for string1 in dict2[string]:
        counvariable +=1
        if string1 in closedSet:
            continue
        newsum = calcdist(dict1[string1], dict1[dict3[end]]) + olddist + calcdist(dict1[string],dict1[string1])
        newdist = olddist + calcdist(dict1[string],dict1[string1])
        booll = 0
        for x in range(0, len(openSet)):
            if openSet[x][1] == string1:
                booll = 1
                number = x
        if booll == 0:
            heappush(openSet, (newsum, string1, newdist))
            a = (float(dict1[string][1]) + 145) * 10
            b = (-5 + float(dict1[string][0])) * 10
            c = (float(dict1[string1][1]) + 145) * 10
            d = (-5 + float(dict1[string1][0])) * 10
            canvas.create_line(a, abs(1000 - b) - 400, c, abs(1000 - d) - 400, fill="#F12")
            for stringgg in dict2[string1]:
                a = (float(dict1[string1][1]) + 145) * 10
                b = (-5 + float(dict1[string1][0])) * 10
                c = (float(dict1[stringgg][1]) + 145) * 10
                d = (-5 + float(dict1[stringgg][0])) * 10
                canvas.create_line(a, abs(1000 - b) - 400, c, abs(1000 - d) - 400, fill="#F12")
            canvas.pack(fill=BOTH, expand=.5)
            root.geometry("1000x1000")
            if counvariable%500 == 0:
              root.update()

        elif oldsum > openSet[number][0]:
            numupdated += 1
            openSet[number][0] = (newsum, string1, 0)
            heapify(openSet)
            numimprovements+=1
        closedSet[string1] = string
        a = (float(dict1[string][1]) + 145) * 10
        b = (-5 + float(dict1[string][0])) * 10
        c = (float(dict1[string1][1]) + 145) * 10
        d = (-5 + float(dict1[string1][0])) * 10
        canvas.create_line(a, abs(1000 - b) - 400, c, abs(1000 - d) - 400, fill="#39CCCC")
        canvas.pack(fill=BOTH, expand=.5)
        root.geometry("1000x1000")
        if counvariable % 500 == 0:
            root.update()
