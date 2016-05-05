from math import sin, cos, radians
import svgwrite
import random

#colours = [(0.1,[167,173,109]), (0.2,[97,104,71]), (0.4,[67,74,57]), (0.2,[118,74,47]), (0.1,[49,45,42]), (1,[255,0,127])]#fleck arma3
colours = [(0.7,[211,194,166]), (0.2,[119,87,53]), (0.1,[67,74,57]), (1,[255,0,127])]#tropen arma3
#colours = [(0.2,[30,34,33]), (0.4,[66,68,52]), (0.1,[100,100,89]), (0.1,[153,154,113]), (0.2,[113,81,52]), (1,[255,0,127])]#fleck arma2
minMult = 0.25
maxMult = 1.75

class Hex:
    def __init__(self):
        self.size=10
        self.lo = Point([-sin(radians(30))*self.size, -sin(radians(60))*self.size])
        self.ro = Point([sin(radians(30))*self.size, -sin(radians(60))*self.size])
        self.lu = Point([-sin(radians(30))*self.size, sin(radians(60))*self.size])
        self.ru = Point([sin(radians(30))*self.size, sin(radians(60))*self.size])
        self.l = Point([-1*self.size, 0*self.size])
        self.r = Point([1*self.size, 0*self.size])
        self.m = Point([0*self.size, 0*self.size])
        cumRnd = 0.0
        rnd = random.random()
        for c in colours:
            cumRnd += c[0]
            if (rnd <= cumRnd):
                for point in [self.lo,self.ro,self.r,self.ru,self.lu,self.l,self.m]:
                    point.colour = c[1]
                break
    def paint(self, dwg):
        colour = colourToString(mixColours(self.m.colour, self.lo.colour, self.ro.colour))
        dwg.add(dwg.polygon([self.m.pos, self.lo.pos, self.ro.pos], fill=colour, stroke=colour, stroke_width="1", stroke_linecap="round"))
        colour = colourToString(mixColours(self.m.colour, self.ro.colour, self.r.colour))
        dwg.add(dwg.polygon([self.m.pos, self.ro.pos, self.r.pos], fill=colour, stroke=colour, stroke_width="1", stroke_linecap="round"))
        colour = colourToString(mixColours(self.m.colour, self.r.colour, self.ru.colour))
        dwg.add(dwg.polygon([self.m.pos, self.r.pos, self.ru.pos], fill=colour, stroke=colour, stroke_width="1", stroke_linecap="round"))
        colour = colourToString(mixColours(self.m.colour, self.ru.colour, self.lu.colour))
        dwg.add(dwg.polygon([self.m.pos, self.ru.pos, self.lu.pos], fill=colour, stroke=colour, stroke_width="1", stroke_linecap="round"))
        colour = colourToString(mixColours(self.m.colour, self.lu.colour, self.l.colour))
        dwg.add(dwg.polygon([self.m.pos, self.lu.pos, self.l.pos], fill=colour, stroke=colour, stroke_width="1", stroke_linecap="round"))
        colour = colourToString(mixColours(self.m.colour, self.l.colour, self.lo.colour))
        dwg.add(dwg.polygon([self.m.pos, self.l.pos, self.lo.pos], fill=colour, stroke=colour, stroke_width="1", stroke_linecap="round"))
    def move(self, rel=[0,0]):
        for point in [self.lo,self.ro,self.r,self.ru,self.lu,self.l,self.m]:
            point.pos = [point.pos[0]+rel[0], point.pos[1]+rel[1]]
def colourToString(c):
    return "rgb("+str(c[0])+","+str(c[1])+","+str(c[2])+")"
def mixColours(a, b, c=None):
    if (c is None):
        return [round((a[0]+b[0])/2),round((a[1]+b[1])/2),round((a[2]+b[2])/2)]
    else:
        return [round((a[0]+b[0]+c[0])/3),round((a[1]+b[1]+c[1])/3),round((a[2]+b[2]+c[2])/3)]
        #return [round((a[0]+a[0]+b[0]+c[0])/4),round((a[1]+a[1]+b[1]+c[1])/4),round((a[2]+a[2]+b[2]+c[2])/4)]
class Point():
    def __init__(self, pos=[0,0], colour=[255,0,127]):
        self.colour = colour
        self.pos = pos
random.seed()
dwg = svgwrite.Drawing("HexPat.svg", profile="full")
hexes = []
width = 50
height = 100
#generate hexes
for y in range(height):
    hexLine = []
    for x in range(width):
        h = Hex()
        hexLine.append(h)
    hexes.append(hexLine)
#change shape
for y in range(height):
    for x in range(width):
        if (y%3==0):
            h = hexes[y][x]
                    
            #lo
            mult = random.random()*(maxMult-minMult)+minMult
            diffX = h.lo.pos[0]
            diffY = h.lo.pos[1]
            h.lo.pos = [h.lo.pos[0]*mult, h.lo.pos[1]*mult]
            diffX = h.lo.pos[0] - diffX
            diffY = h.lo.pos[1] - diffY
            xOffset = 0
            if (y%2==1):
                xOffset = 1
            if (x-1+xOffset >= 0):
                if (y-1>=0):
                    p = hexes[y-1][x-1+xOffset]
                    p.r.pos = [p.r.pos[0]+diffX, p.r.pos[1]+diffY]
            if (y-2>=0):
                p = hexes[y-2][x]
                p.lu.pos = [p.lu.pos[0]+diffX, p.lu.pos[1]+diffY]
                
            #ro
            mult = random.random()*(maxMult-minMult)+minMult
            diffX = h.ro.pos[0]
            diffY = h.ro.pos[1]
            h.ro.pos = [h.ro.pos[0]*mult, h.ro.pos[1]*mult]
            diffX = h.ro.pos[0] - diffX
            diffY = h.ro.pos[1] - diffY
            xOffset = 0
            if (y%2==1):
                xOffset = 1
            if (x+xOffset < width):
                if (y-1>=0):
                    p = hexes[y-1][x+xOffset]
                    p.l.pos = [p.l.pos[0]+diffX, p.l.pos[1]+diffY]
            if (y-2>=0):
                p = hexes[y-2][x]
                p.ru.pos = [p.ru.pos[0]+diffX, p.ru.pos[1]+diffY]
            
            #l
            mult = random.random()*(maxMult-minMult)+minMult
            diff = h.l.pos[0]
            h.l.pos = [h.l.pos[0]*mult, h.l.pos[1]*mult]
            diff = h.l.pos[0] - diff
            xOffset = 0
            if (y%2==1):
                xOffset = 1
            if (x+-1+xOffset < width):
                if (y-1>=0):
                    p = hexes[y-1][x-1+xOffset]
                    p.ru.pos = [p.ru.pos[0]+diff, p.ru.pos[1]]
                if (y+1<height):
                    p = hexes[y+1][x-1+xOffset]
                    p.ro.pos = [p.ro.pos[0]+diff, p.ro.pos[1]]
            
            #r
            mult = random.random()*(maxMult-minMult)+minMult
            diff = h.r.pos[0]
            h.r.pos = [h.r.pos[0]*mult, h.r.pos[1]*mult]
            diff = h.r.pos[0] - diff
            xOffset = 0
            if (y%2==1):
                xOffset = 1
            if (x+xOffset < width):
                if (y-1>=0):
                    p = hexes[y-1][x+xOffset]
                    p.lu.pos = [p.lu.pos[0]+diff, p.lu.pos[1]]
                if (y+1<height):
                    p = hexes[y+1][x+xOffset]
                    p.lo.pos = [p.lo.pos[0]+diff, p.lo.pos[1]]
                    
            #ru
            mult = random.random()*(maxMult-minMult)+minMult
            diffX = h.ru.pos[0]
            diffY = h.ru.pos[1]
            h.ru.pos = [h.ru.pos[0]*mult, h.ru.pos[1]*mult]
            diffX = h.ru.pos[0] - diffX
            diffY = h.ru.pos[1] - diffY
            xOffset = 0
            if (y%2==1):
                xOffset = 1
            if (x+xOffset < width):
                if (y+1<height):
                    p = hexes[y+1][x+xOffset]
                    p.l.pos = [p.l.pos[0]+diffX, p.l.pos[1]+diffY]
            if (y+2<height):
                p = hexes[y+2][x]
                p.ro.pos = [p.ro.pos[0]+diffX, p.ro.pos[1]+diffY]
                    
            #lu
            mult = random.random()*(maxMult-minMult)+minMult
            diffX = h.lu.pos[0]
            diffY = h.lu.pos[1]
            h.lu.pos = [h.lu.pos[0]*mult, h.lu.pos[1]*mult]
            diffX = h.lu.pos[0] - diffX
            diffY = h.lu.pos[1] - diffY
            xOffset = 0
            if (y%2==1):
                xOffset = 1
            if (x-1+xOffset >= 0):
                if (y+1<height):
                    p = hexes[y+1][x-1+xOffset]
                    p.r.pos = [p.r.pos[0]+diffX, p.r.pos[1]+diffY]
            if (y+2<height):
                p = hexes[y+2][x]
                p.lo.pos = [p.lo.pos[0]+diffX, p.lo.pos[1]+diffY]
#diffuse colour
#move mid
for y in range(height):
    for x in range(width):
        h = hexes[y][x]
        ang = random.random()*360
        dist = random.random()*minMult*h.size
        h.m.pos = [h.m.pos[0]+dist*sin(radians(ang)),h.m.pos[1]+dist*cos(radians(ang))]
        
        #lo
        colour = h.m.colour
        if (x-1+xOffset >= 0):
            if (y-1>=0):
                p = hexes[y-1][x-1+xOffset]
                colour = mixColours(colour, p.m.colour)
        if (y-2>=0):
            p = hexes[y-2][x]
            colour = mixColours(colour, p.m.colour)
        h.lo.colour = colour
        
        #ro
        colour = h.m.colour
        if (x+xOffset < width):
            if (y-1>=0):
                p = hexes[y-1][x+xOffset]
                colour = mixColours(colour, p.m.colour)
        if (y-2>=0):
            p = hexes[y-2][x]
            colour = mixColours(colour, p.m.colour)
        h.ro.colour = colour
        
        #l
        colour = h.m.colour
        if (x+-1+xOffset < width):
            if (y-1>=0):
                p = hexes[y-1][x-1+xOffset]
                colour = mixColours(colour, p.m.colour)
            if (y+1<height):
                p = hexes[y+1][x-1+xOffset]
                colour = mixColours(colour, p.m.colour)
        h.l.colour = colour
        
        #r
        colour = h.m.colour
        if (x+xOffset < width):
            if (y-1>=0):
                p = hexes[y-1][x+xOffset]
                colour = mixColours(colour, p.m.colour)
            if (y+1<height):
                p = hexes[y+1][x+xOffset]
                colour = mixColours(colour, p.m.colour)
        h.r.colour = colour
        
        #ru
        colour = h.m.colour
        if (x+xOffset < width):
            if (y+1<height):
                p = hexes[y+1][x+xOffset]
                colour = mixColours(colour, p.m.colour)
        if (y+2<height):
            p = hexes[y+2][x]
            colour = mixColours(colour, p.m.colour)
        h.ru.colour = colour
        
        #lu
        colour = h.m.colour
        if (x-1+xOffset >= 0):
            if (y+1<height):
                p = hexes[y+1][x-1+xOffset]
                colour = mixColours(colour, p.m.colour)
        if (y+2<height):
            p = hexes[y+2][x]
            colour = mixColours(colour, p.m.colour)
        h.lu.colour = colour
#paint
he = Hex()
for y in range(height):
    for x in range(width):
        h = hexes[y][x]
        pos = [x*(he.r.pos[0]*3),y*(he.ru.pos[1])]
        if (y%2 == 1):
            pos[0] += he.r.pos[0]+he.ru.pos[0]
        h.move(pos)
        h.paint(dwg)
dwg.save()