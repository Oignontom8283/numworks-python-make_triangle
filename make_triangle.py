# -*- coding: utf-8 -*-
# version : v1.0.3
# development started in 09/2024.
# numworks shop repot : https://my.numworks.com/python/546f6d/make_triangle/
# github repot : https://github.com/Oignontom8283/make-a-triangle_numworks-python/

from math import *
from time import *
import ion

### Custom libraries ###


### Numworks Python 2D Engine - Start module definition ###

# Version : v1.0.0
# Author(s) : https://github.com/Oignontom8283/

import kandinsky as kd
from time import *
from math import *

color = kd.color

camera = (0, 0)
zoom = 1

# pixels per unit
scale = 1

# diap^lay grid
grid = False

debug = False

class screen: 
    width = 320
    height = 222


class coord:
    def __init__(self, x, y, rounder=1):
        self.x = x
        self.y = y
        self.rounder = rounder
    def tuple(self):
        return (self.x, self.y)
    def __str__(self):
        return "(x: " + str(round(self.x, self.rounder)) + ", y: " + str(round(self.y, self.rounder)) + ")"
    def __repr__(self):
        return "(x: " + str(round(self.x, self.rounder)) + ", y: " + str(round(self.y, self.rounder)) + ")"


def set_camera(x, y):
    global camera
    camera = (x, y)

def get_camera():
    global camera
    return camera

def center_camera_on(x, y):
    global camera
    
    px = x * scale * zoom
    py = y * scale * zoom

    # Centrer la caméra sur le point
    camera = (px, py)

def set_scale(s):
    global scale
    scale = s

def get_scale():
    global scale
    return scale

def set_zoom(z):
    global zoom
    zoom = z

def get_zoom():
    global zoom
    return zoom


def set_grid(g:bool):
    global grid
    grid = g

def get_grid():
    global grid
    return grid


def set_debug(d:bool):
    global debug
    debug = d

def get_debug():
    global debug
    return debug

def normalize_coord(x, y):
    """
    Transform the coordinates (x, y) in the world to the screen coordinates.
    The zoom is centered on the screen center.
    """
    # Position du point dans le monde (avant zoom)
    dx = x * scale
    dy = y * scale

    # Décale selon la caméra (toujours en unités monde)
    dx -= camera[0]
    dy -= camera[1]

    # Applique le zoom autour du centre de l'écran
    screen_x = int(dx * zoom + screen.width / 2)
    screen_y = int(dy * zoom + screen.height / 2)

    return coord(screen_x, screen_y)

def bresenham(x1, y1, x2, y2):
    points = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1

    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    if dx > dy:
        err = dx / 2.0
        while x != x2:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

    points.append((x, y))
    return points

def trace_line(x1, y1, x2, y2, color=color(0, 0, 0)):
    points = bresenham(x1, y1, x2, y2)
    for point in points:
        kd.set_pixel(point[0], point[1], color)

def draw_line(x1, y1, x2, y2, color=color(0, 0, 0)):
    a = normalize_coord(x1, y1)
    b = normalize_coord(x2, y2)
    trace_line(a.x, a.y, b.x, b.y, color)

def draw_rect(x, y, w, h, color=color(0, 0, 0)):
    a = normalize_coord(x, y)
    b = normalize_coord(x + w, y + h)
    kd.fill_rect(a.x, a.y, b.x - a.x, b.y - a.y, color)

def draw_cross(x, y, size:tuple=(5, 5), color=color(0, 0, 0), diagonal=False, absolute=False):
    a = normalize_coord(x, y)
    sizeX = int(size[0] * zoom * scale if not absolute else size[0] * zoom)
    sizeY = int(size[1] * zoom * scale if not absolute else size[1] * zoom)

    if diagonal:
        # Draw diagonal lines
        trace_line(a.x - sizeX, a.y - sizeY, a.x + sizeX, a.y + sizeY, color)
        trace_line(a.x - sizeX, a.y + sizeY, a.x + sizeX, a.y - sizeY, color)
    else:
        kd.fill_rect(a.x - int(sizeX / 2), a.y, sizeX, 1, color)
        kd.fill_rect(a.x, a.y - int(sizeY / 2), 1, sizeY, color)



def draw_circle(x, y, r, color=color(0, 0, 0), fill=False, absolute=False):
    a = normalize_coord(x, y)
    r = int(r * zoom * scale if not absolute else r)
    x0 = a.x
    y0 = a.y
    x = 0
    y = r
    d = 3 - 2 * r

    def draw_circle_points(xc, yc, x, y):
        if fill:
            # Draw horizontal lines between symmetric points
            for i in range(xc - x, xc + x + 1):
                kd.set_pixel(i, yc + y, color)
                kd.set_pixel(i, yc - y, color)
            for i in range(xc - y, xc + y + 1):
                kd.set_pixel(i, yc + x, color)
                kd.set_pixel(i, yc - x, color)
        else:
            kd.set_pixel(xc + x, yc + y, color)
            kd.set_pixel(xc - x, yc + y, color)
            kd.set_pixel(xc + x, yc - y, color)
            kd.set_pixel(xc - x, yc - y, color)
            kd.set_pixel(xc + y, yc + x, color)
            kd.set_pixel(xc - y, yc + x, color)
            kd.set_pixel(xc + y, yc - x, color)
            kd.set_pixel(xc - y, yc - x, color)

    while x <= y:
        draw_circle_points(x0, y0, x, y)
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1

def draw_point(x, y, r, color=color(0, 0, 0), fill=False):
    draw_circle(x, y, r, color, fill, True)

def draw_circle_arc(x, y, r, start_angle, end_angle, color=color(0, 0, 0), fill=False, absolute=False):
    """"fill=True is not optimal for now"""
    a = normalize_coord(x, y)
    r = int(r * zoom * scale if not absolute else r)
    x0 = a.x
    y0 = a.y
    start_angle = start_angle % 360
    end_angle = end_angle % 360

    if fill:
        for angle in range(start_angle, end_angle + 1):
            radian = angle * (pi / 180)
            x1 = int(x0 + r * cos(radian))
            y1 = int(y0 + r * sin(radian))
            # Draw line from center to arc point
            points = bresenham(x0, y0, x1, y1)
            for px, py in points:
                kd.set_pixel(px, py, color)
    else:
        for angle in range(start_angle, end_angle + 1):
            radian = angle * (pi / 180)
            x1 = int(x0 + r * cos(radian))
            y1 = int(y0 + r * sin(radian))
            kd.set_pixel(x1, y1, color)

def draw_text(x, y, text, offset=(0, 0), color=color(0, 0, 0)):
    a = normalize_coord(x, y)
    kd.draw_string(text, a.x + offset[0], a.y + offset[1], color)

def clear(backgroundColor=color(255, 255, 255), scale_min=10):
    """
    Its recomended to not change the scale minimum value for the grid to be displayed
    """
    kd.fill_rect(0, 0, screen.width, screen.height, backgroundColor)

    if grid and scale > 10:
        gap = int(scale * zoom)

        # Calcule la position du point (0,0) à l'écran
        origin = normalize_coord(0, 0)
        offset_x = origin.x % gap
        offset_y = origin.y % gap

        grid_color = color(220, 220, 220)

        # Lignes verticales (rectangles fins de 1 pixel de large)
        for x in range(offset_x, screen.width, gap):
            kd.fill_rect(x, 0, 1, screen.height, grid_color)

        # Lignes horizontales (rectangles fins de 1 pixel de haut)
        for y in range(offset_y, screen.height, gap):
            kd.fill_rect(0, y, screen.width, 1, grid_color)

    if debug:
        # display zoom and camera
        kd.draw_string("Zoom: " + str(round(zoom, 3)),0, 0, color(0, 0, 0))
        kd.draw_string("Scale: " + str(round(scale, 3)),0, 15, color(0, 0, 0))
        kd.draw_string("Camera: (x:" + str(round(camera[0])) + " ,y:" + str(round(camera[1])) + ")", 0, 30, color(0, 0, 0))

def draw_angle_arc(p1x, p1y, vertexX, vertexY, p2x, p2y, radius, color=color(0, 0, 0)):
    from math import atan2, degrees

    # Vectors
    v1 = (p1x - vertexX, p1y - vertexY)
    v2 = (p2x - vertexX, p2y - vertexY)

    # Calcule of the angle of each vector
    angle1 = degrees(atan2(v1[1], v1[0])) % 360
    angle2 = degrees(atan2(v2[1], v2[0])) % 360

    # Calculation of the angle between v1 and v2 in the trigonometric direction
    angle = (angle2 - angle1) % 360
    if angle > 180:
        angle = 360 - angle  # On veut le plus petit angle entre les deux vecteurs

    # Determining the limits for drawing the arc
    if (angle2 - angle1) % 360 > 180:
        start_angle, end_angle = angle2, angle1
    else:
        start_angle, end_angle = angle1, angle2

    # Write the arc
    draw_circle_arc(vertexX, vertexY, radius, start_angle, end_angle, color, False, True)

    return angle


### Numworks Python 2D Engine - End module definition ###



### Script start ###

a = int(input("distance A : "))
b = int(input("distance B : "))
c = int(input("distance C : "))

#a = 5
#b = 4
#c = 3

try:
    A = coord(0, 0)
    B = coord(a, 0)
    C = coord((a**2 + c**2 - b**2) / (2 * a), sqrt(c**2 - ((a**2 + c**2 - b**2) / (2 * a))**2))
except:
    print("[ERROR]: Impossible to create the triangle with these values")
    raise NameError("exit by erro")


ABp = coord(x=(A.x + B.x) / 2, y=(A.y + B.y) / 2)
BCp = coord(x=(B.x + C.x) / 2, y=(B.y + C.y) / 2)
CAp = coord(x=(C.x + A.x) / 2, y=(C.y + A.y) / 2)

# Calculating the distance between points
ABd = sqrt(abs(A.x - B.x) ** 2 + abs(A.y - B.y) ** 2)
BCd = sqrt(abs(B.x - C.x) ** 2 + abs(B.y - C.y) ** 2)
CAd = sqrt(abs(C.x - A.x) ** 2 + abs(C.y - A.y) ** 2)

# Calculathe the center of the trangle
G = coord(x=(A.x + B.x + C.x) / 3, y=(A.y + B.y + C.y) / 3)

# Calculate the distances from the points to the center
Ra = sqrt(abs(A.x - G.x) ** 2 + abs(A.y - G.y) ** 2)
Rb = sqrt(abs(B.x - G.x) ** 2 + abs(B.y - G.y) ** 2)
Rc = sqrt(abs(C.x - G.x) ** 2 + abs(C.y - G.y) ** 2)

# Find the point farthest from the center
R = max(Ra, Rb, Rc)

# Calculat the surface of the triangle
S = sqrt((ABd + BCd + CAd) * (-ABd + BCd + CAd) * (ABd - BCd + CAd) * (ABd + BCd - CAd)) / 4

# set_zoom(0.9 * (screen.width / (R * 2)))
set_zoom(1)
set_scale(0.9 * (screen.width / (R * 2)))
set_grid(True)
center_camera_on(G.x, G.y)

points_size = 5
speed = 1
info = False

def main():

    black = color(0, 0, 0)
    red = color(255, 0, 0)
    blue = color(0, 0, 255)
    green = color(0, 150, 0)
    majenta = color(255, 0, 255)
    grey = color(200, 200, 200)
    
    if info:
        kd.draw_string("A = " + str(A), 0, 0, red)
        kd.draw_string("B = " + str(B), 0, 15, red)
        kd.draw_string("C = " + str(C), 0, 15*2, red)

        kd.draw_string("a (AB) = " + str(ABd), 0, 15*4, black)
        kd.draw_string("b (BC) = " + str(BCd), 0, 15*5, black)
        kd.draw_string("c (CA) = " + str(CAd), 0, 15*6, black)

        kd.draw_string("G = " + str(G), 0, 15*8, green)
        kd.draw_string("Rayon = " + str(round(R, 3)), 0, 15*9, blue)
        kd.draw_string("Surface = " + str(round(S,3)), 0, 15*10, majenta)
        
        return

    draw_point(A.x, A.y, points_size, blue, True)
    draw_point(B.x, B.y, points_size, blue, True)
    draw_point(C.x, C.y, points_size, blue, True)

    draw_line(A.x, A.y, B.x, B.y, black)
    draw_line(B.x, B.y, C.x, C.y, black)
    draw_line(C.x, C.y, A.x, A.y, black)

    radius = 20
    AB_angle = draw_angle_arc(C.x, C.y, A.x, A.y, B.x, B.y, radius, red)  # angle en A
    AC_angle = draw_angle_arc(A.x, A.y, B.x, B.y, C.x, C.y, radius, red)  # angle en B
    BA_angle = draw_angle_arc(B.x, B.y, C.x, C.y, A.x, A.y, radius, red)  # angle en C

    draw_text(A.x, A.y, "A " + str(round(AB_angle, 1)) + "°", color=red, offset=(10, 0))
    draw_text(B.x, B.y, "B " + str(round(AC_angle, 1)) + "°", color=red, offset=(10, 0))
    draw_text(C.x, C.y, "C " + str(round(BA_angle, 1)) + "°", color=red, offset=(10, 0))

    draw_text(ABp.x, ABp.y, "a " + str(round(ABd, 1)), black)
    draw_text(BCp.x, BCp.y, "b " + str(round(BCd, 1)), black)
    draw_text(CAp.x, CAp.y, "c " + str(round(CAd, 1)), black)

    draw_cross(G.x, G.y, (points_size * 2, points_size * 2), green, False, True)
    draw_text(G.x, G.y, "G", (2, 2), color=green)

    #draw_circle(G.x, G.y, R, grey)

set_debug(False)
clear()
main()
delay = 0
while True:
    change = False
    if ion.keydown(ion.KEY_UP):
        camera = (camera[0], camera[1] - speed)
        change = True
    if ion.keydown(ion.KEY_DOWN):
        camera = (camera[0], camera[1] + speed)
        change = True
    if ion.keydown(ion.KEY_LEFT):
        camera = (camera[0] - speed, camera[1])
        change = True
    if ion.keydown(ion.KEY_RIGHT):
        camera = (camera[0] + speed, camera[1])
        change = True
    if ion.keydown(ion.KEY_PLUS):
        if zoom < 4:
            zoom += 0.01
            change = True
    if ion.keydown(ion.KEY_MINUS):
        if zoom > 0.01:
            zoom -= 0.01
            change = True

    if ion.keydown(ion.KEY_SINE) and speed > 1:
        speed -= 1
        change = True
    
    if ion.keydown(ion.KEY_COSINE) and speed < 10:
        speed += 1
        change = True
    
    if ion.keydown(ion.KEY_EXE):
        info = not info
        set_grid(not info)
        change = True
        delay = 3
    
    if change == True:
        change = False
        clear()
        main()
        if delay > 0:
          sleep(delay)
          delay = 0
