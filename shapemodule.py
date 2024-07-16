import pygame,sys
import numpy as np
import random

import pygame.gfxdraw
def get_edges(vertices):

    return [(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]
class particle():
    def __init__(self,coords,radius,physics,color):
        self.coords = coords
        self.radius = radius
        self.physics = physics
        self.color = color
class triangle():

    
    
    def __init__(self,x,y):
        
        self.vertex1 =[]
        self.vertex2 =[]
        self.vertex3 =[]
        self.col_axis = []
        self.col_lines = []
        self.vertex1 = [x,y]
        
        self.vertex2.append(self.vertex1[0]+ 100)
        self.vertex2.append(self.vertex1[1]+ 100)
        self.vertex3.append(self.vertex1[0]+ 200)
        self.vertex3.append(self.vertex1[1])
        self.vertices = [self.vertex1, self.vertex2,self.vertex3]
        self.normals = []
        self.calc_self_normals()
        
    def calc_self_normals(self):
        edges = get_edges(self.vertices)
        normals = []
        for edge in edges:
            dx = edge[1][0] - edge[0][0]
            dy = edge[1][1] - edge[0][1]
            normal_slope = -dx / dy if dy != 0 else float('inf')  #ertical line 
            normals.append(normal_slope)

        self.normals = normals
    def update(self,changes):
        self.vertex1[0] += changes[0]/40
        self.vertex1[1] += changes[1]/40
        self.vertex2[0] += changes[0]/40
        self.vertex2[1] += changes[1]/40

        self.vertex3[0] += changes[0]/40
        self.vertex3[1] += changes[1]/40
        self.vertices = [self.vertex1, self.vertex2,self.vertex3]#this line wasnt here before how did it remotely work


        
    def render_shape(self,surface,color):#Trianglerender
         pygame.gfxdraw.aapolygon(surface,(self.vertex1,self.vertex2,self.vertex3),color)
         pygame.gfxdraw.filled_polygon(surface,(self.vertex1,self.vertex2,self.vertex3),color)
    #def check_for_col():
        
    #def rotate():
    def rendercol(self,surface):
       height = surface.get_size()[1]
       width = surface.get_size()[0]
       color = (230,230,40)
       for x in self.normals:
            if x == float('inf'):
               
                pygame.draw.aaline(surface,color,(width/2,0),(width/2,height))
            if x > 0:
                pygame.draw.aaline(surface,color,(0,0),(height/x,height))
            elif x < 0:
                pygame.draw.aaline(surface,color,(width,0),(width-height/x * -1,height))

            elif x == 0:
                pygame.draw.aaline(surface,color,(0,height/2),(width,height/2))
           
               
    def collision_check(self,surface,object):
        axes = np.add(self.col_axis,object.col_axis)
        for x in axes:
            pass
        #col_axis2 = (self.vertex2[1] - self.vertex1[1])/(self.vertex2[0] - self.vertex1[0])
       
    def rotate(self, angle, pivot=None):
        if pivot is None:
            pivot = self.calculate_centroid()
        
        angle_rad = np.radians(angle)
        cos_theta = np.cos(angle_rad)
        sin_theta = np.sin(angle_rad)
        
        rotation_matrix = np.array([
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta]
        ])
        
        def rotate_point(point):
            translated_point = np.array(point) - np.array(pivot)
            rotated_point = np.dot(rotation_matrix, translated_point)
            return rotated_point + np.array(pivot)
        
        self.vertex1 = rotate_point(self.vertex1).tolist()
        self.vertex2 = rotate_point(self.vertex2).tolist()
        self.vertex3 = rotate_point(self.vertex3).tolist()
        self.vertices = [self.vertex1, self.vertex2, self.vertex3]
    
    def calculate_centroid(self):
        x_coords = [vertex[0] for vertex in self.vertices]
        y_coords = [vertex[1] for vertex in self.vertices]
        centroid_x = sum(x_coords) / 3
        centroid_y = sum(y_coords) / 3
        return [centroid_x, centroid_y]



class Polygon:
    def __init__(self,first_point,side_length):

        root_number_thing = np.sqrt(side_length*side_length/2)
        self.vertices = [first_point]
        self.vertices.append([first_point[0]+side_length,first_point[1]])
        self.vertices.append([first_point[0]+side_length + root_number_thing,first_point[1] + root_number_thing])
        self.vertices.append([first_point[0] + side_length,2* root_number_thing + first_point[1]])
        self.vertices.append([first_point[0],2* root_number_thing + first_point[1]])
        self.vertices.append([first_point[0] - root_number_thing,first_point[1]+ root_number_thing])
        self.color = (255,0,0)  

    def update(self, changes):
        for vertex in self.vertices:
            vertex[0] += changes[0]/40
            vertex[1] += changes[1]/40  

    def render(self, surface):#polygonerender
        pygame.gfxdraw.aapolygon(surface, self.vertices, self.color)
        pygame.gfxdraw.filled_polygon(surface, self.vertices, self.color)
        return surface

    def rotate(self, angle, pivot=None):
        if pivot is None:
            pivot = self.calculate_centroid()
        
        angle_rad = np.radians(angle)
        cos_theta = np.cos(angle_rad)
        sin_theta = np.sin(angle_rad)
        
        rotation_matrix = np.array([
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta]
        ])
        
        def rotate_point(point):
            translated_point = np.array(point) - np.array(pivot)
            rotated_point = np.dot(rotation_matrix, translated_point)
            return rotated_point + np.array(pivot)
        
        self.vertices = [rotate_point(vertex).tolist() for vertex in self.vertices]
    
    def calculate_centroid(self):
        x_coords = [vertex[0] for vertex in self.vertices]
        y_coords = [vertex[1] for vertex in self.vertices]
        centroid_x = sum(x_coords) / len(self.vertices)
        centroid_y = sum(y_coords) / len(self.vertices)
        return [centroid_x, centroid_y]

    def set_color(self, color):
        self.color = color
