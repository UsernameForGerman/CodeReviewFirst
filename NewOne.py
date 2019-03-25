import math
import os
from tkinter import *

class Aircraft():
    x, y = 0, 0                 #aircraft coordinates in the plane of aircraft
    a, b = 0, 0                 #speed vector coordinates in the plane of aircraft
    height = 0                  #height from the ground
    verticalSpeed = 0           #perpendicular to the plane
    mass = 0                    #mass of aircraft
    speed = 0

    def __init__(self, x_, y_, a_, b_, verticalSpeed_, mass_, height_):
        self.a, self.b = a_, b_
        self.x, self.y = x_, y_
        self.verticalSpeed = verticalSpeed_
        self.mass = mass_
        self.height = height_
        self.speed = math.sqrt(math.pow(x_, 2) + math.pow(y_, 2) + math.pow(verticalSpeed_, 2))

    #proble:directionVectora==0+coordinatesx==0
    def calculateLine(self):
        return [self.x, self.y, self.height, self.a, self.b, self.verticalSpeed]

    def getCoordinates(self):
        return [self.x, self.y, self.height]

#not used
def findWayPointCollision(firstAircraft, secondAircraft):
    # Если каноническое уравнение прямой 0:
    # (x-xo)/p=(y-yo)/q=(z-zo)/r
    # а каноническое уравнение прямой 1:
    # (x-x1)/p1=(y-y1)/q1=(z-z1)/r1

    # coordinates of waypoint collison
    # x=(xo*q*p1-x1*q1*p-yo*p*p1+y1*p*p1)/(q*p1-q1*p)
    # y=(yo*p*q1-y1*p1*q-xo*q*q1+x1*q*q1)/(p*q1-p1*q)
    # z=(zo*q*r1-z1*q1*r-yo*r*r1+y1*r*r1)/(q*r1-q1*r)

    lineOne = firstAircraft.calculateLine()
    lineTwo = secondAircraft.calculateLine()

    x0, y0, z0, p, q, r = lineOne[0], lineOne[1], lineOne[2], lineOne[3], lineOne[4], lineOne[5]
    x1, y1, z1, p1, q1, r1 = lineTwo[0], lineTwo[1], lineTwo[2], lineTwo[3], lineTwo[4], lineTwo[5]

    if (q * p1 - q1 * p == 0) or (p * q1 - p1 * q == 0) or (q * r1 - q1 * r == 0):
        return 0
        # think what will do in this case
    else:
        x = (x0 * q * p1 - x1 * q1 * p - y0 * p * p1 + y1 * p * p1) / (q * p1 - q1 * p)
        y = (y0 * p * q1 - y1 * p1 * q - x0 * q * q1 + x1 * q * q1) / (p * q1 - p1 * q)
        z = (z0 * q * r1 - z1 * q1 * r - y0 * r * r1 + y1 * r * r1) / (q * r1 - q1 * r)
        return [x, y, z]

#not used
def getTimeWayPointArrival(inputAircraft, listOfCoordinatesWPCollision):
    if (listOfCoordinatesWPCollision != 0):
        #x, y, z - waypoint of arrival
        line = inputAircraft.calculateLine()
        x0, y0, z0 = line[0], line[1], line[2]
        x, y, z = listOfCoordinatesWPCollision[0], listOfCoordinatesWPCollision[1], listOfCoordinatesWPCollision[2]
        distance = math.sqrt(math.pow(x - x0, 2) + math.pow(y - y0, 2) + math.pow(z - z0, 2))
        return distance / inputAircraft.speed
    else:
        return 0

def distanceAircrafts(mainAircraft, inputAircraft):
    mainCoordinates = mainAircraft.getCoordinates()
    inputCoordinates = inputAircraft.getCoordinates()
    x0, y0, height0 = mainCoordinates[0], mainCoordinates[1], mainCoordinates[2]
    x, y, height = inputCoordinates[0], inputCoordinates[1], inputCoordinates[2]
    return round(math.sqrt(math.pow((x - x0), 2) + math.pow((y - y0), 2) + math.pow((height - height0) * 165 / 1000000, 2)))

#not used
def willBeCollision(firstAircraft, secondAircraft):
    coordinatesWPCollision = findWayPointCollision(firstAircraft, secondAircraft)
    if (coordinatesWPCollision != 0):
        if (getTimeWayPointArrival(firstAircraft, coordinatesWPCollision) == getTimeWayPointArrival(secondAircraft, coordinatesWPCollision)):
            return True
        else:
            return False
    else:
        return False

#True mean up first and down second, False mean down first and up second
def wayToFlight(firstAircraft, secondAircraft):
    distance = distanceAircrafts(firstAircraft, secondAircraft)
    if distance < 5:
        if firstAircraft.mass >= secondAircraft.mass:
            return True
        else:
            return False
    else:
        return False

def testSystem(aircraftClassFirst, aircraftClassSecond):
    print(wayToFlight(aircraftClassFirst, aircraftClassSecond))

def generatorStrListToIntList(file):
    for line in file:
        yield [float(i) for i in line.split()]

def listOfAircraftFromInput(file, generatorStrListToIntList):
    list = []
    for aircraft in generatorStrListToIntList(file):
        list.append(aircraft)
    return list

def infoFromFile(name):
    file = open(name, "r")
    list = listOfAircraftFromInput(file, generatorStrListToIntList)
    listAircrafts = []
    for aircraft in list:
        listAircrafts.append(Aircraft(*aircraft))
    file.close()
    return listAircrafts

def showTCAS(listAircrafts, scale):
    #General options of output
    WORK_PATH = os.path.abspath(os.getcwd())
    root = Tk()
    root.geometry("410x410")

    #set the ND
    img = PhotoImage(file=os.path.join(WORK_PATH, 'ND.gif'))
    ND = Label(root, image=img)
    ND.pack()

    #put the info to ND
    mainAircraft = listAircrafts[0]

    #Height, speed and scale on ND putting
    text = "Height {2}\nSpeed {1}\nSCL {0}".format(scale, mainAircraft.speed, mainAircraft.height)
    textLb = Label(root, bg='black', fg='green', text=text, font=('Times New Roman', 12))
    textLb.place(x='10', y='10', in_=ND)

    #put Gross Weight(mass) of aircraft
    mass = "GW {0}".format(mainAircraft.mass)
    massLb = Label(root, bg='black', fg='green', text=mass, font=('Times New Roman', 12))
    massLb.place(anchor='nw', x='300', y='10', in_=ND)

    #put on ND Planes
    imgPlane = PhotoImage(file=os.path.join(WORK_PATH, 'plane.gif'))
    imgPlaneRed = PhotoImage(file=os.path.join(WORK_PATH, 'planeRed.gif'))
    imgPlaneYellow = PhotoImage(file=os.path.join(WORK_PATH, 'planeYellow.gif'))

    cautionWas = False
    planes = [[0, 0]]
    for i in range(1, len(listAircrafts)):
        distance = distanceAircrafts(listAircrafts[0], listAircrafts[i])
        xPlane, yPlane = str(200 + (listAircrafts[i].x - 0) * 247 / scale), str(337 - (listAircrafts[i].y - 0) * 247 / scale)
        xPlaneDistance = str(225 + (listAircrafts[i].x - 0) * 247 / scale)
        yPlaneDistance = str(345 - (listAircrafts[i].y - 0) * 247 / scale)
        textPlane = str(distance) + "nm"

        if (distance <= 3):     #put red caution and plane
            #put on ND plane
            planes.append([Label(root, image=imgPlaneRed)])
            planes[i][0].place(x=xPlane, y=yPlane, in_=ND)

            #put on ND distance
            planes[i].append(Label(root, bg='black', fg='red', text=textPlane, font=('Times New Roman', 10)))
            planes[i][1].place(x=xPlaneDistance, y=yPlaneDistance, in_=ND)

            #put Caution
            cautionWas = True
            caution = "CAUTION!"
            cautionLb = Label(root, bg='black', fg='red', text=caution, font=('Times New Roman', 14))
            cautionLb.place(anchor='nw', x='160', y='10', in_=ND)
            #put command-direction to fly
            if (wayToFlight(mainAircraft, listAircrafts[i])):
                direction = "UP!"
                directionBt = Button(root, text=direction, width='7', height='2', bg='black', fg='red',
                                     font=('Times New Roman', 30))
                directionBt.place(x='130', y='150', in_=ND)
            else:
                direction = "DOWN!"
                directionBt = Button(root, text=direction, width='7', height='2', bg='black', fg='red',
                                     font=('Times New Roman', 30))
                directionBt.place(x='130', y='150', in_=ND)
        elif (distance <= 5):    #put yellow caution and plane
            #put on ND plane
            planes.append([Label(root, image=imgPlaneYellow)])
            planes[i][0].place(x=xPlane, y=yPlane, in_=ND)

            #put on ND distance
            planes[i].append(Label(root, bg='black', fg='yellow', text=textPlane, font=('Times New Roman', 10)))
            planes[i][1].place(x=xPlaneDistance, y=yPlaneDistance, in_=ND)

            # put Caution
            if (cautionWas == False):
                caution = "CAUTION!"
                cautionLb = Label(root, bg='black', fg='yellow', text=caution, font=('Times New Roman', 14))
                cautionLb.place(anchor='nw', x='160', y='10', in_=ND)
        else:       #put ordinary plane without caution
            # put on ND plane
            planes.append([Label(root, image=imgPlane)])
            planes[i][0].place(x=xPlane, y=yPlane, in_=ND)

            #put on ND distance
            planes[i].append(Label(root, bg='black', fg='white', text=textPlane, font=('Times New Roman', 10)))
            planes[i][1].place(x=xPlaneDistance, y=yPlaneDistance, in_=ND)

    root.mainloop()

name = "input.txt"

showTCAS(infoFromFile(name), 20)


