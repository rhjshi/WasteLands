''' Author: Richie Shi

    Date: 2 Apr 2017
    
    Description: Sprites for a cherry and pacman :)
'''
import pygame, random, math

class Cherry(pygame.sprite.Sprite):
    '''Creates a sprite that represents a cherry'''
    def __init__(self, screen):
        '''initializes object, takes screen for dimensions to display itself 
        at a random location of the screen'''
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("cherries.gif")
        self.image = self.image.convert()
        self.image.set_colorkey((255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0 + self.rect.width/2,\
                                           screen.get_width() - self.rect.width/2)
        self.rect.centery = random.randint(80 + self.rect.height/2,\
                                           screen.get_height() - self.rect.height/2)
        
        
class Pacman(pygame.sprite.Sprite):
    '''Creates a sprite that represents pacman character'''
    def __init__(self, screen):
        '''initializes object, takes screen for dimension'''
        pygame.sprite.Sprite.__init__(self)
        
        #load images
        self.__left_image = pygame.image.load("pacman-left.gif")
        self.__left_image = self.__left_image.convert()
        
        self.__right_image = pygame.image.load("pacman-right.gif")
        self.__right_image = self.__right_image.convert()
        
        self.__up_image = pygame.image.load("pacman-up.gif")
        self.__up_image = self.__up_image.convert()         
        
        self.__down_image = pygame.image.load("pacman-down.gif")
        self.__down_image = self.__down_image.convert()         
        
        self.__screen = screen
        #load starting image, directions
        self.go_right()
        self.rect = self.image.get_rect()
        self.rect.center = (self.__screen.get_width()/2, self.__screen.get_height()/2)
        
    def go_left(self):
        '''sets the direction of the pacman to left'''
        self.__xdir = -3
        self.__ydir = 0
        self.image = self.__left_image
    
    def go_right(self):
        '''sets the direction of the pacman to right'''
        self.__xdir = 3
        self.__ydir = 0
        self.image = self.__right_image
        
    def go_up(self):
        '''sets the direction of the pacman to up'''
        self.__xdir = 0
        self.__ydir = -3
        self.image = self.__up_image    
        
    def go_down(self):
        '''sets the direction of the pacman to down'''
        self.__xdir = 0
        self.__ydir = 3
        self.image = self.__down_image
        
    def update(self):
        '''moves the sprite towards the direction and checks to see if the 
        sprite goes off the screen'''
        self.rect.centerx += self.__xdir
        self.rect.centery += self.__ydir
        
        if self.rect.left > self.__screen.get_width():
            self.rect.right = 0

        elif self.rect.right < 0:
            self.rect.left = self.__screen.get_width()

        elif self.rect.top > self.__screen.get_height():
            self.rect.bottom = 0

        elif self.rect.bottom < 0:
            self.rect.top = self.__screen.get_height()
        
class Projectile(pygame.sprite.Sprite):
    '''fdsf'''
    def __init__(self, start, end):
        '''fdsf'''
        pygame.sprite.Sprite.__init__(self)
        x = end[0] - start[0]
        y = end[1] - start[1]
        h = (x**2 + y**2)**0.5
        steps = h/20.0
        
        self.__xvel = math.floor(float(x)/steps)
        self.__yvel = math.floor(float(y)/steps)
        
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0))
        pygame.draw.circle(self.image, (255, 0, 0), (5, 5), 5, 0)
        self.rect = self.image.get_rect()
        self.rect.center = start
        self.__end = end
    
    def update(self):
        '''fdsf'''
        #if self.rect.centerx >= self.__end[0] or self.rect.centery >= self.__end[1]:
            #self.__xvel, self.__yvel = 0, 0
            #self.kill()
        self.rect.centerx += self.__xvel
        self.rect.centery += self.__yvel
        