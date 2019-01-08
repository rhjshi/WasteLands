''' Author: Richie Shi

    Date: 6 May 2017
    
    Description: module for sprites that are going to be used in main game loop
'''
import pygame, math

class Crosshair(pygame.sprite.Sprite):
    '''crosshair for player to aim with'''
    def __init__(self):
        '''This initializer takes a screen surface as parameters'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set the image rect attributes
        self.image = pygame.image.load("./Cursor/crosshair.png")
        self.rect = self.image.get_rect()
        
    def update(self):
        '''called automatically to move mouse based on mouse position'''
        self.rect.center = pygame.mouse.get_pos()

class Player(pygame.sprite.Sprite):
    '''class for main character of game'''
    def __init__(self, screen, floor):
        '''takes screen as parameter to use in attributes, initializes object'''
        
        #parent __init__
        pygame.sprite.Sprite.__init__(self)
        
        #key variables
        self.__jumps_left = 0
        self.__dead = False        
        self.__floor = floor
        
        # image and rect attributes
        self.__faceright = pygame.image.load("./Player/Character Face Right.png")
        self.__faceleft = pygame.image.load("./Player/Character Face Left.png")
        self.image = self.__faceright
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_width()/2
        self.rect.bottom = 0
        
        #velocity attributes
        self.__yvel = 0
        self.__yacc = 2
        
        #player stats
        self.__health = 50
        self.__lives = 3
        
    def get_health(self):
        '''returns hitpoints player has'''
        return self.__health
    
    def get_lives(self):
        '''returns the number of lives the player has'''
        return self.__lives
    
    def take_dmg(self, dmg):
        '''takes the amount of damage is dealt to the player'''
        self.__health -= dmg
        
    def jump(self):
        '''tells player to jump by changing y velocity'''
        if self.__jumps_left:    
            self.__yvel = -25
            self.__yacc = 2
            self.__jumps_left -= 1
        
    def respawn(self):
        '''respawns the character'''
        self.__health = 50
        self.rect.bottom = 0
        self.__yvel = 0
        self.__yacc = 1
        self.__jumps_left = 0
    
    def get_dead(self):
        '''returns if player is dead or not'''
        return self.__dead
        
    def update(self):
        '''automatically called to update position of player sprite''' 
        #check which way player is facing
        if pygame.mouse.get_pos()[0] < self.rect.centerx:
            self.image = self.__faceleft
        else:
            self.image = self.__faceright
        
        #only if player is alive
        if not self.__dead:
            #to make sure the player doesn't keep falling
            if self.rect.colliderect(self.__floor.rect):
                self.__yvel = 0
                self.__yacc = 0
                self.rect.bottom = self.__floor.rect.top
                self.__jumps_left = 3
                
            #check health and lives
            if self.__health <= 0:
                self.__lives -= 1
                if self.__lives > 0:
                    self.respawn()
                else:
                    self.__health = 0
                    self.__yvel = -20
                    self.__yacc = 1
                    self.__dead = True
        else:
            self.__health = 0
        
        self.__yvel += self.__yacc
        self.rect.centery += self.__yvel   
        
        
class HealthNum(pygame.sprite.Sprite):
    '''used to keep track of the player's health in a numerical value'''
    def __init__(self, player, healthbar):
        '''takes the player that the health is associated with, and healthbar for location'''
        
        #parent __init__
        pygame.sprite.Sprite.__init__(self)
        
        # key attributes
        self.__healthbar = healthbar
        self.__player = player
        self.__maxHP = self.__player.get_health()
        
        #load font 
        self.__font = pygame.font.Font("./Fonts/Zorque/zorque.ttf", 30)
        
    def update(self):
        '''called automatically to update health value'''
        self.__currentHP = self.__player.get_health()
        message = "%d / %d " %(self.__currentHP, self.__maxHP)
        
        self.image = self.__font.render(message, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.top = 25
        self.rect.right = self.__healthbar.rect.left

class HealthBar(pygame.sprite.Sprite):
    '''gives a visual representation of health in a bar'''
    def __init__(self, player):
        '''takes the player for health stats'''
        #parent __init__
        pygame.sprite.Sprite.__init__(self)
        
        #set key attributes
        self.__player = player
        self.__maxHP = self.__player.get_health()
        
        self.image = pygame.Surface((350, 20))
        self.rect = self.image.get_rect()
        self.rect.top = 35
        self.rect.left = 140
        
    def update(self):
        '''called automatically to redraw bar and set bar in correct position'''
        #calculate the length of the red bar
        length = 342 * float(self.__player.get_health())/self.__maxHP
        pygame.draw.rect(self.image, (0, 0, 0), ((4, 4) ,(342, 12)))
        if length:
            pygame.draw.rect(self.image, (255, 0, 0), ((4, 4) ,(length, 12)))
        
class Lives(pygame.sprite.Sprite):
    '''displays the number of lives the player has'''
    def __init__(self, player):
        '''takes the player sprite that the lives is associated with'''
        #parent __init__ method
        pygame.sprite.Sprite.__init__(self)
        
        #key attributes
        self.__player = player
     
        #load images
        self.__images = []
        for num in range(0, 4):
            self.__images.append(pygame.image.load("./Stats/"+str(num)+"Lives.png"))
    
    def update(self):
        '''used to update the number of lives the player has'''
        lives = self.__player.get_lives()
        if lives > 0:
            self.image = self.__images[lives]
        else:
            self.image = self.__images[0]
        self.rect = self.image.get_rect()
        self.rect.top = 60
        self.rect.left = 25
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''class that keeps track of score in game'''
    def __init__(self):
        '''takes screen for dimensions'''
        #parent init
        pygame.sprite.Sprite.__init__(self)
        
        #key variables
        self.__font = pygame.font.SysFont("Impact", 40)
        self.__score = 0
        
    def add_score(self, plus):
        '''increases score by given amount'''
        self.__score += plus
        
    def update(self):
        '''automatically displays the score at top right of screen'''
        message = "Score: %d" %self.__score
        self.image = self.__font.render(message, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.top = 60
        self.rect.left = 230
        
class Background(pygame.sprite.Sprite):
    '''class for scrolling background'''
    def __init__(self, screen):
        '''takes screen so to make sure background doesn't go off screen'''
        
        #parent __init__ method
        pygame.sprite.Sprite.__init__(self)
        
        #image and rect attributes
        self.image = pygame.image.load("./Background/Scrolling Background.png")
        self.rect = self.image.get_rect()
        self.rect.centery = 500
        self.rect.left = 0
        
        self.__xvel = 0
        self.__yvel = 0
        
        #states
        self.__moving_left = False
        self.__moving_right = False
        
        self.__screen = screen
        
        #how far it has moved in the last frame so that other sprites can use it
        self.__camera_offset = 0
        
    def go_left(self):
        '''moves to the left'''
        self.__moving_left = True  
        self.__moving_right = False
        
    def go_right(self):
        '''moves to the right'''
        self.__moving_right = True
        self.__moving_left = False
            
    def left_idle(self):
        '''stops the left movement'''
        self.__moving_left = False
    
    def right_idle(self):
        '''stops the right movement'''
        self.__moving_right = False
        
    def get_offset(self):
        '''returns camera offset'''
        return self.__camera_offset
        
    def update(self):
        '''automatically called to update the position of the background'''
        oldx = self.rect.centerx
        
        #check if background is out of screen
        if self.rect.right <= self.__screen.get_width()+15:
            self.rect.right = self.__screen.get_width()+15
        elif self.rect.left >= -15:
            self.rect.left = -15
        
        if self.__moving_right:
            self.__xvel = 15
        elif self.__moving_left:
            self.__xvel = -15
        else:
            self.__xvel = 0
        
        self.rect.centerx += self.__xvel
        self.rect.centery += self.__yvel
        
        newx = self.rect.centerx
        self.__camera_offset = newx - oldx
        
class Floor(pygame.sprite.Sprite):
    '''This class defines the sprite for our ground so the player doesn't just
    fall through the bottom of the screen'''
    def __init__(self, screen, background):
        '''This initializer takes a screen surface and background as parameter'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #key variables
        self.__background = background
        
        #image and rect attributes
        self.image = pygame.image.load("./Background/Scrolling Floor.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = screen.get_height()
        
    def update(self):
        '''called automatically to move'''
        self.rect.left = self.__background.rect.left
        
class PlayerBullet(pygame.sprite.Sprite):
    '''class that creates bullet objects that hit other sprites'''
    def __init__(self, screen, background, weapon, end):
        '''takes screen to kill itself when out of screen, takes background to
        keep up with camera offset, takes weapon to know the amount of dmg the 
        bullet should do and also for where to begin the bullet path, end is tuple
        value that is where the mouse was at when it is clicked'''
        
        #call parent __init__ method
        pygame.sprite.Sprite.__init__(self)  

        #if the weapon is primary
        if weapon.get_num() == 1:
            speed = 35.0
            self.__damage = 3
            #image attributes
            self.__imagelist = [pygame.image.load("./Bullets/Primary/Bullet2.png")]
        #if secondary weapon is out
        else:
            speed = 15.0
            self.__damage = 9
        
        #stuffs to calculate speed of projectile so it travels where you want it
        start = weapon.rect.center
        x = end[0] - start[0]
        y = end[1] - start[1]
        h = (x**2 + y**2)**0.5
        steps = h/speed
        
        try:
            self.__xvel = math.floor(float(x)/steps)
            self.__yvel = math.floor(float(y)/steps)    
        except ZeroDivisionError:
            self.__xvel = 0
            self.__yvel = speed
        
        #if secondary, left or right image attributes
        if weapon.get_num() == 2:
            if self.__xvel < 0:
                self.__imagelist = []
                for num in range(1,3):
                    image = pygame.image.load("./Bullets/Secondary/RocketLeft"+str(num)+".png")
                    #image.set_colorkey((255, 255, 255))
                    #image.convert()
                    self.__imagelist.append(image)
            else:        
                self.__imagelist = []
                for num in range(1,3):
                    image = pygame.image.load("./Bullets/Secondary/RocketRight"+str(num)+".png")
                    #image.set_colorkey((255, 255, 255))
                    #image.convert()
                    self.__imagelist.append(image)
        
        #positioning the projectile
        self.image = self.__imagelist[0]
        self.rect = self.image.get_rect()
        self.rect.center = start
        
        #other key attributes
        self.__background = background
        self.__screen = screen
        self.__imagenum = 0
 
    def get_dmg(self):
        '''returns bullet dmg'''
        return self.__damage
        
    def update(self):
        '''called to move bullet and keep up with background'''
        #image updates
        self.__imagenum += 1
        if self.__imagenum > (len(self.__imagelist)-1):
            self.__imagenum = 0
        original_image = self.__imagelist[self.__imagenum]
        
        #rotate image
        try:
            degree = math.degrees(math.atan(float(-self.__yvel)/self.__xvel))
        except ZeroDivisionError:
            if self.__yvel > 0:
                degree = 90
            elif self.__yvel < 0:
                degree = -90
            else:
                degree = 0
        self.image = pygame.transform.rotate(original_image, degree)         
        self.image.convert()
        self.image.set_colorkey((255, 255, 255))
        #checks if the bullet is out of screen
        if (self.rect.centerx > self.__screen.get_width()) or\
           (self.rect.centerx < 0) or\
           (self.rect.centery > self.__screen.get_height()) or\
           (self.rect.centery < 0):
            self.kill()
        self.rect.centerx += self.__xvel + self.__background.get_offset()
        self.rect.centery += self.__yvel
        
class Weapon(pygame.sprite.Sprite):
    '''class for weapon that looks like it's shooting'''
    def __init__(self, screen, character):
        '''takes the screen and character object that it is associated with'''
        pygame.sprite.Sprite.__init__(self)
        
        #set key attributes first
        self.__player_attr = character
        self.__screen = screen
        self.__can_fire = True
        
        #set primary weapon first
        self.set_primary()
        
    def set_primary(self):
        '''sets the weapon to be the primary weapon'''
        self.__weapon_num = 1
        self.__firerate_clock = 1
        
        self.__point_right = pygame.image.load("./Weapons/Pistol Right.png")
        self.__point_left = pygame.image.load("./Weapons/Pistol Left.png")
        
        self.image = self.__point_right
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width()/2        
        
    def set_secondary(self):
        '''sets the weapon to be the secondary weapon'''
        self.__weapon_num = 2
        self.__firerate_clock = 3
        
        self.__point_right = pygame.image.load("./Weapons/Rocket Right.png")
        self.__point_left = pygame.image.load("./Weapons/Rocket Left.png")
        
        self.image = self.__point_right
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width()/2           
        
    def fire(self):
        '''shoots the weapon and sets certain variables to have a firerate'''    
        self.__can_fire = False
        self.__temp_clock = self.__firerate_clock
        
    def get_can_fire(self):
        '''returns boolean value determining whether or not the weapon can shoot'''
        return self.__can_fire
        
    def get_num(self):
        '''returns the weapon type'''
        return self.__weapon_num
    
    def update(self):
        '''automatically called to update position'''
        #pick left or right
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < self.rect.centerx:
            original_image = self.__point_left
        else:
            original_image = self.__point_right
        
        #rotate image so weapon points to mouse
        x = mouse_pos[0] - self.rect.centerx
        y = -mouse_pos[1] + self.rect.centery
        
        try:
            degree = math.degrees(math.atan(float(y)/x))
        except ZeroDivisionError:
            if y > 0:
                degree = 90
            elif y < 0:
                degree = -90
            else:
                degree = 0
        self.image = pygame.transform.rotate(original_image, degree)
        
        #checks to see if weapon can fire
        if not self.__can_fire:
            self.__temp_clock -= 1
            if self.__temp_clock == 0:
                self.__can_fire = True
        self.rect.centery = self.__player_attr.rect.centery + 5
        
class EnemyProjectile(pygame.sprite.Sprite):
    '''class that creates bullet objects that hit other sprites'''
    def __init__(self, background, enemy, player):
        '''takes screen to kill itself when out of screen, takes background to
        keep up with camera offset, takes enemy for where to begin the bullet path, 
        player to know where to shoot to'''
        
        #call parent __init__ method
        pygame.sprite.Sprite.__init__(self)
       
        #stuffs to calculate speed of projectile so it travels where you want it
        self.__background = background
        self.__enemy = enemy
        self.__player = player
        
        x = self.__player.rect.centerx - self.__enemy.rect.centerx
        steps = abs(x)/30.0
        try:
            self.__xvel = x/steps
        except ZeroDivisionError:
            self.__xvel = 30
        #image and rect attributes
        self.image = pygame.image.load("./Bullets/Yeti Bullet1.gif")
        self.image.set_colorkey((0, 0, 0))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = self.__enemy.rect.center
        
    def update(self):
        '''called to move bullet and keep up with background'''
        #checks if the bullet is out of screen
        if (self.rect.centerx > self.__background.rect.right) or\
           (self.rect.centerx < self.__background.rect.left):
            self.kill()
        self.rect.centerx += self.__xvel + self.__background.get_offset()

class Yeti(pygame.sprite.Sprite):
    '''class that creates an enemy to be shot'''
    def __init__(self, background, floor, player, centerx):
        '''background for positioning with offset, centerx for x location'''
        #parent init
        pygame.sprite.Sprite.__init__(self)
        
        #image and rect attributes
        self.__idleimagelist = []
        self.__attackimagelist = []
        for num in range(1, 3):
            self.__idleimagelist.append(pygame.image.load("./Enemy/Yeti/Yeti "+ str(num)+".png"))
        for num in range(3, 5):
            self.__attackimagelist.append(pygame.image.load("./Enemy/Yeti/Yeti "+ str(num)+".png"))    
        self.__imagelist = self.__idleimagelist
        self.image = self.__imagelist[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = 0
        
        #stats and key variables
        self.__player = player
        self.__xvel = 2
        self.__yvel = 1
        self.__yacc = 1
        self.__paceclock = 120
        self.__health = 100        
        self.__background = background
        self.__floor = floor
        self.__melee_dmg = 8
        
        #states
        self.__attackmode = False
        self.__can_melee = True
        self.__melee_timer = 30       
 
    def take_dmg(self, damage):
        '''reduces health by amount of damage taken'''
        self.__health -= damage   
    
    def attack(self):
        '''returns damage enemy deals when contact with player'''
        #change images and stuff
        if self.__can_melee:
            self.__can_melee = False        
            return self.__melee_dmg
        else:
            return 0
        
    def get_attackmode(self):
        '''returns attack state'''
        return self.__attackmode
    
    def get_health(self):
        '''returns sprite health'''
        return self.__health
    
    def update(self):
        '''automatically called to move sprite'''
        #so the yeti doesn't keep hitting player every frame
        if not self.__can_melee:
            self.__imagelist = self.__attackimagelist
            self.__melee_timer -= 1
            if self.__melee_timer == 0:
                self.__can_melee = True
                self.__melee_timer = 30
        else:
            self.__imagelist = self.__idleimagelist
        #left or right image       
        if self.__xvel < 0:
            self.image = self.__imagelist[0]
        else:
            self.image = self.__imagelist[1]       
            
        #check to see if player is in close proximity to enemy
        if abs(self.__player.rect.centerx - self.rect.centerx) < 400:
            self.__attackmode = True
        else:
            self.__attackmode = False
            
        #used to pace sprite back and forth when idle
        if not self.__attackmode:    
            self.__paceclock -= 1
            if self.__paceclock == 0:
                self.__paceclock = 120
                self.__xvel = -self.__xvel
                
        #when attacking player
        else:
            delta_x = self.__player.rect.centerx - self.rect.centerx
            try:
                self.__xvel = (delta_x/abs(delta_x))*6
            except ZeroDivisionError:
                self.__xvel = 0
        
        #stop falling down
        if self.rect.colliderect(self.__floor.rect):
            self.__yvel = 0
            self.__yacc = 0
            self.rect.bottom = self.__floor.rect.top
        else:
            self.__yvel += self.__yacc

        #movement to keep up with background
        self.rect.centerx += self.__xvel + self.__background.get_offset()
        self.rect.centery += self.__yvel
        