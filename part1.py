import pygame
from math import sin, cos
import math as math
import numpy as np
# Define some constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CAMERA_DISTANCE = 4
ROTATION_SPEED = 0.01
color = (0, 200, 95)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Define the camera position and orientation
camera_position = [0, 0, CAMERA_DISTANCE]
camera_rotation = [0, 0]


# Define a function to project 3D points onto the 2D screen
vertices = []
edges = []

# Load the vertices and edges of the 3D object from the file

# read the file
def read_file():
    # Ask the user for the name of the file to load
    filename = input("Enter the name of the 3D object file to load: ")
    with open(filename, 'r') as file:
        first_line = file.readline().strip().split(',')
        vert = int(first_line[0])
        edge = int(first_line[1])
        print(edge)
        # read the vertices
        for i in range(0, vert):
            l, x, y, z = file.readline().split(',')
            vertices.append((float(x), float(y), float(z)))
        print(vertices)
        for i in range(0, edge):
            pts = file.readline().split(',')
            for j in range(0, len(pts)):
                if ((int(pts[j])-1, int(pts[(j+1) % len(pts)])-1) not in edges):
                    edges.append((int(pts[j])-1, int(pts[(j+1) % len(pts)])-1))

        print(edges)

# Define a class to represent 3D objects
class Shape:
    def __init__(self, vertices, edges, color):
        self.vertices = vertices
        self.edges = edges
        self.color = color
        self.moving = False
    # Define a function to project 3D points onto the 2D screen
    def project(self, vertex):
        x = vertex[0] - camera_position[0]
        y = vertex[1] - camera_position[1]
        z = vertex[2] - camera_position[2]
        x, z = x*cos(camera_rotation[1]) - z*sin(camera_rotation[1]
                                                 ), z*cos(camera_rotation[1]) + x*sin(camera_rotation[1])
        y, z = y*cos(camera_rotation[0]) - z*sin(camera_rotation[0]
                                                 ), z*cos(camera_rotation[0]) + y*sin(camera_rotation[0])
        f = WINDOW_HEIGHT/2 / z
        return (int(x*f + WINDOW_WIDTH/2), int(-y*f + WINDOW_HEIGHT/2))
    
    # Define a function to draw the object
    def draw_object(self):
        for edge in self.edges:
            start = self.project(self.vertices[edge[0]])
            end = self.project(self.vertices[edge[1]])
            pygame.draw.line(screen, self.color, start, end)
        for vertex in vertices:
            point = self.project(vertex)
            pygame.draw.circle(screen, self.color, point, 5)
    # x-axis rotation
    def rotate_x(self, rot):
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            new_x = x*cos(rot) - z*sin(rot)
            new_z = z*cos(rot) + x*sin(rot)
            self.vertices[i] = (new_x, y, new_z)
    # y-axis rotation
    def rotate_y(self, rot):
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            new_y = y*cos(rot) - z*sin(rot)
            new_z = z*cos(rot) + y*sin(rot)
            self.vertices[i] = (x, new_y, new_z)


# initialize the shape
read_file()
shape = Shape(vertices, edges, color)

# Main loop
while True:
    # Handle events
    rel_x, rel_y = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the starting position of the mouse
            shape.moving = True
            start_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEMOTION and shape.moving:
            shape.rotate_x(ROTATION_SPEED * rel_x)
            shape.rotate_y(ROTATION_SPEED*rel_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            shape.moving = False

    # Calculate the distance and direction of the mouse drag
    distance = math.hypot(rel_x, rel_y)
    direction = math.atan2(rel_y, rel_x)

    # Print the distance and direction to the console
    screen.fill((80, 80, 80))

    # Draw the object
    shape.draw_object()

    # Update the display
    pygame.display.flip()
    clock.tick(60)
