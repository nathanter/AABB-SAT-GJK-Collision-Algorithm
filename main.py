import pygame,sys
import numpy as np
import random

import pygame.gfxdraw
import shapemodule
import sorting


OVERALL_WHITE = (255,255,255)
class ui():
    
    def __init__(self,functions) -> None:
        self.functions = []
        self.buttons = []
        for x in functions:
            self.functions.append(x)
    
    def button_init(self,screen):
        array_of_rects = []


        for x in range(len(self.functions)):
            array_of_rects.append(pygame.Rect(10,
                                              (((x) * 50 + (x+1)*10))
                                              ,100
                                              ,50))
       
        return array_of_rects

    def button_render(self,rects,screen,hover,width):#buttonrender

        sidebar = pygame.Rect(0,0,width,screen.get_size()[1])
        
        pygame.draw.rect(screen,(240,235,235),sidebar)
        f  = pygame.font.Font(None,14)
        for x in range(len(rects)) :
            if x != hover:
                pygame.draw.rect(screen,(255,255,255),rects[x])
            else:
                pygame.draw.rect(screen,(255,0,0),rects[x])
             
            text = f.render(self.functions[x],True,color = (0,0,0))
            location = rects[x]
            screen.blit(text,(location.x + location.w/2 - 20,location.y + location.h/2))
      
    
     
    def button_logic(self, screen,mouse,width):
        collision_rects =  self.button_init(screen)
        
        hover = -1
        for x in range(len(collision_rects)):
            if collision_rects[x].collidepoint(mouse)== True:
                hover = x
            
       
        self.button_render(collision_rects,screen,hover,width)
        return hover   

    #def onclick(self, button_hover,state):
      #  if button_hover == -1:
       #     return -1
       # else: 
         #   return self.functions[button_hover]
    
            #

        



def get_edges(vertices):

    return [(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]
    

def calc_onen(point1,point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    slop = -dx/dy if dy != 0 else float('inf')
    return slop


def calculate_normals(triangles):
    normals = []
    for tri in triangles:
       
        edges = get_edges(tri.vertices)
     
        for edge in edges:
            dx = edge[1][0] - edge[0][0]
            dy = edge[1][1] - edge[0][1]
            normal_slope = -dx / dy if dy != 0 else float('inf')  #ertical line 
            normals.append(normal_slope)

    return normals



##
pygame.init()

def aabbcol(rect1,rect2):
    if rect1.colliderect(rect2):
        overlap_x = min(rect1.right - rect2.left, rect2.right - rect1.left)
        overlap_y = min(rect1.bottom - rect2.top, rect2.bottom - rect1.top)
        
        if overlap_x < overlap_y:
            if rect1.centerx < rect2.centerx:
                rect1.x -= overlap_x
            else:
                rect1.x += overlap_x
        else:
            if rect1.centery < rect2.centery:
                rect1.y -= overlap_y
            else:
                rect1.y += overlap_y
    return [rect1,rect2]


def aabb(s, shapes,movement,viewsupports,active,colors):
    pygame.Surface.fill(s,OVERALL_WHITE)

    shapes[active].x += movement[0]/60
    shapes[active].y += movement[1]/60
   
    
    if viewsupports == True:
        
        projection = pygame.Surface((200,200),pygame.SRCALPHA)
        rect = pygame.Rect(0,0,shapes[0].w,shapes[0].h)
        pygame.draw.rect(projection,(255,0,0,128),rect)
        s.blit(projection,(shapes[0].x + movement[0] ,shapes[0].y+movement[1]))


    
    for x in range(len(shapes)):
        pygame.draw.rect(s,colors[x],shapes[x])
        for y in range(x + 1, len(shapes)):
            returnv = aabbcol(shapes[x],shapes[y])
            shapes[x] = returnv[0]
            shapes[y] = returnv[1]

    return [s,shapes]

def full_dot(vector1,vector2):
    dots = vector1[0] * vector2[0] + vector1[1]*vector2[1]
    return dots
            
        
def dot_product(shape,normal): 
    
    dots = [i[0] * 1 + i[1] * normal for i in shape.vertices]  
    return [min(dots),max(dots)]


def infcase(shape):
    range = [i[1] for i in shape.vertices]
    return [min(range),max(range)]

def checkforsatcol(shape1,shape2):

    normals = []
    shape1.calc_self_normals()
    shape1.calc_self_normals()
    for x in shape1.normals:
        normals.append(x)
    for y in shape2.normals:
        normals.append(y)
    
    
    for n in normals:

        if n != float("inf"):
            dots = dot_product(shape1,n)
            dots2 = dot_product(shape2,n)
            
            if(dots[0] < dots2[0] and dots[1] < dots2[0]):
                return False,normals
            elif(dots[0] > dots2[1] and dots[1] >dots2[1]):
                return False,normals
            
        else:
            yrange1 = infcase(shape1)
            yrange2 = infcase(shape2)
            if yrange1[0] < yrange2[0] and yrange1[1] < yrange2[0]:
                return False,normals
            elif yrange1[0] > yrange2[1] and yrange1[1] > yrange2[1]:
                return False,normals
            
    return True,normals
def rendercolax(s,normals):
    pass
def sat(s,triangles,mp,viewsupports,active):
    pygame.Surface.fill(s,OVERALL_WHITE)
   
    triangles[active].update(mp)
    colstat,normals = checkforsatcol(triangles[0],triangles[1])
    if colstat == True:
        triangles[active].update([(mp[0] * -1),(mp[1]*-1)])
  
    
    



        

    
    for tri in triangles:
             
        tri.render_shape(s,(255,0,0)) 
 
        if viewsupports == True:
                tri.rendercol(s)
    
    return s


def find_n_triple(vector1,vector2,vector3):
    perp_len = vector1[0] * vector2[1] - vector1[1]* vector2[0]    
    return[-perp_len*vector3[1],perp_len*vector3[0]] 

def passed_zero(direction,point):
    if full_dot(point,direction) < 0:
        return False
    else: return True

def support_gjk(shape1,normal):
   
    stored_vertix = shape1.vertices[0]
    min = full_dot(shape1.vertices[0],normal)
    for vertix in shape1.vertices:
        dot = full_dot(vertix,normal)
        if dot > min:
            stored_vertix = vertix
            min = dot

    

    return stored_vertix

def checkgjk(shape1, shape2 ):
    direction = [1,0]
    simplex_points = []
    for l in range(2):
        
        farpoint = support_gjk(shape1,direction)
        oppdirection = [x*-1 for x in direction]
        oppfarpoint = support_gjk(shape2,oppdirection)
        new_point = [farpoint[i] - oppfarpoint[i] for i in range(len(farpoint))]
    
        simplex_points.append(new_point)
        
        if new_point == [0,0]:
            return True
     
        if passed_zero(new_point,direction) == False:
                
                return False

    
        direction = [k * -1 for k in new_point]

    while True:
        
        resultOfCol = trianglecase(simplex_points,shape1,shape2)
        if resultOfCol[0] == True:
            
            return True
            
        else:
            if resultOfCol[1] == -1:
               return False
            else: simplex_points = resultOfCol[1]

           


def trianglecase(simplex,shape1,shape2):
    ab = [simplex[0][0] - simplex[1][0],simplex[0][1] - simplex[1][1]]
    ao = [-1 * i for i in simplex[1]]

    new_normal = find_n_triple(ab,ao,ab)
    point = support_gjk(shape1,new_normal)
    oppnewnormal = [i*-1 for i in new_normal]
    opp_point = support_gjk(shape2,oppnewnormal)
    new_point  = [point[0] - opp_point[0],point[1] - opp_point[1]]
    simplex.append(new_point)

    if passed_zero(new_point,new_normal) == False :
        return [False,-1]
    
    if simplex[0] == simplex[2] or simplex[1] == simplex[2]:
        return [False,-1]
    ab =[simplex[1][0] - simplex[2][0],simplex[1][1] - simplex[2][1]]
    ac =[simplex[0][0] - simplex[2][0],simplex[0][1] - simplex[2][1]]

    ab_perp = find_n_triple(ac,ab,ab)
    ac_perp = find_n_triple(ab,ac,ac)
    ao = [i * -1 for i in simplex[2]]
    if(full_dot(ab_perp,ao) > 0):
        return [False,[simplex[1],simplex[2]]]
    
    elif(full_dot(ac_perp,ao) > 0):
        return [False, [simplex[0],simplex[2]]]
    
    else: return [True,0]


    




    #using this find the normal
    #support to find support point
    #check whether it crosses and contains zero#
    #if support point already in simplex kill program
    #contain zero:
    #take normals relative to final point -> 0 vector
    #if both are < zero return true
    #else take best one and remove corresponding point from simplex
      
#more logic


    




    
    
    
    
    



        

def gfx(s,shapes,amp):

    pygame.Surface.fill(s,OVERALL_WHITE)
    shapes[0].update(amp)
    if(checkgjk(shapes[0],shapes[1])):
       amp = [k*-1 for k in amp]
       shapes[0].update(amp)

   
    for x in shapes:
        
        s = x.render(s)


    return s
def gfx__init():
    shapes1 = shapemodule.Polygon([200,200],50)
    shapes2 = shapemodule.Polygon([500,500],50)
    return [shapes1,shapes2]

def sat_init():
    tri = shapemodule.triangle(900,900)
    tri2 = shapemodule.triangle(500,500)
    
    return [tri,tri2] 

def aabb_init():
    rect1 = pygame.FRect(0,0,200,100)
    rect2 = pygame.FRect(700,300,200,100)
    return [rect1,rect2]

def particle_system_init():
    shape1 = shapemodule.particle([400,300],10,[0,20],[255,0,0])
    shape2 = shapemodule.particle([400,400],10,[0,20],[255,0,0])
    shape3 = shapemodule.particle([500,300],10,[-50,20],[255,0,0])
    #shape4 = shapemodule.particle([600,400],10,[50,40],[255,0,0])

    return[shape1,shape2,shape3]


def partcol(shapes1p,shapes2p):

    
    if ((shapes1p.coords[0] - shapes2p.coords[0])**2 + (shapes1p.coords[1] - shapes2p.coords[1])** 2 < (shapes1p.radius+ shapes2p.radius) **2):
               
                return True
                
    
    else: return False

  
def pruning(shapes):
    shapes = sorting.sort(shapes)
    
    temp = [shapes[0]]
    active = []
    
    for x in range(1,len(shapes)):
        
      
        
        if (shapes[x].coords[0] - shapes[x].radius <= temp[-1].coords[0] + temp[-1].radius):
                
                temp.append(shapes[x])
               
               

        else:
            if(len(temp) > 1):
                active.append(temp)
            temp = [shapes[x]]
            
    if(len(temp) > 1):
                active.append(temp)

    return active


def particles(s,shapes):
    pygame.Surface.fill(s,OVERALL_WHITE)

    indextracker = pruning(shapes)
    

    for x in indextracker:
        for y in range(len(x)):
            for z in range(y,len(x)):
           
                if partcol(x[y],x[z]) == True:
                
                    x[y].physics[0] *= -1
                    x[y].physics[1] *= -1
                    x[z].physics[0] *= -1
                    x[z].physics[1] *= -1
                    
                


                
        
    for shape in shapes:
        if shape.coords[0] <= 0 or shape.coords[0] >= s.get_size()[0]:
            shape.physics[0] *= -1
        if shape.coords[1] <= 0 or shape.coords[1] >= s.get_size()[1]:
            shape.physics[1] *= -1
        shape.coords[0] += shape.physics[0]/55
        shape.coords[1] += shape.physics[1]/55
        
       
        pygame.draw.aacircle(s,shape.color,shape.coords,shape.radius)
        #pygame.gfxdraw.filled_circle(s,particle[0][0],particle[0][1],particle[1],particle[3])

    return [s,shapes]
    
    


def masks_col():
    pass
screen = pygame.display.set_mode()
ui_width = 150
ui_space = pygame.Surface((ui_width,screen.get_size()[1]))
s = pygame.Surface((screen.get_size()[0]-ui_width, screen.get_size()[1]))

def main_loop():
    shapes = aabb_init()
    s = pygame.Surface((screen.get_size()[0]-ui_width, screen.get_size()[1]))
    state = 0
    clock = pygame.Clock()
    color_list = [(255,0,0),(0,255,0)]
    but = -1
    buttons = ui(["AABB","SAT","GJK","Masks","Particles","View Supports","Add Shape"])
    but = buttons.button_logic(s,pygame.mouse.get_pos(),240)
    mp = [0,0,0,0]
    active = 0
    rotate = False
    viewsupports = False
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
            
              
                if but != -1 and state != but:
                    if but == 0:
                        shapes = aabb_init()
                        state = 0
                    if but == 1:
                        shapes = sat_init()
                        state = 1

                    if but ==2:
                        shapes = gfx__init()
                        state = 2
                    if but  ==3:
                        pass
                    if but  ==4:
                        shapes = particle_system_init()
                        state = 4
                        
                if but == 5: 
                    if viewsupports== True:
                        viewsupports == False
                    else: viewsupports = True
                if but == 6:
                    if state == 4:
                        temp = shapemodule.particle([random.randint(1,7)*100,400],10,[random.randint(-1,1)*20,40],[random.randint(0,255),random.randint(0,255),random.randint(0,255)])
                        shapes.append(temp)

                    if state == 0:
                        temp = pygame.Rect(random.randint(0,s.size[0]),random.randint(0,s.size[1]),200,100)

                        shapes.append(temp)
                        color_list.append((0,0,255))

               

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rotate = True
                if event.key == pygame.K_RIGHT:
                    mp[0] = 1  
                if event.key == pygame.K_LEFT:
                    mp[1] = -1

                if event.key == pygame.K_UP:
                    mp[2] = -1
                if event.key == pygame.K_DOWN:
                    mp[3] = 1 

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    rotate = False
                if event.key == pygame.K_RIGHT:
                    mp[0] = 0
                if event.key == pygame.K_LEFT:
                    mp[1] = 0

                if event.key == pygame.K_UP:
                    mp[2] = 0
                if event.key == pygame.K_DOWN:
                    mp[3] = 0
            
                
            
            

        amp = [mp[0]*50 + mp[1] * 50,mp[2]*50 + mp[3] * 50]
    
        if state == 0:
            hel = aabb(s,shapes,amp,viewsupports,active,color_list)
            s =hel[0]
            shapes = hel[1]
       

               

        elif state == 1:
            if rotate == True:
                shapes[0].rotate(1)
           
            s = sat(s,shapes,amp,viewsupports,active)
        elif state == 2:
          
            if rotate== True:
                shapes[0].rotate(1)
            
            s = gfx(s,shapes,amp)
           
        elif state == 4:
            ar = particles(s,shapes)
            s = ar[0]

        clock.tick()
       
        but = buttons.button_logic(ui_space,pygame.mouse.get_pos(),240)
        screen.blit(ui_space,(0,0))
        screen.blit(s,(ui_width,0))

        pygame.display.flip()



main_loop()



