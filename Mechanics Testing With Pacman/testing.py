''' Author: Richie Shi

    Date: 2 Apr 2017
    
    Description: Unit 5-7 #4
    practically pacman game
'''

# allSprites.clear( what are these parameters )
# layered group???

# I - import, initailize
import pygame, pacmanSprites, random
pygame.init()

def main():
    '''mainline logic'''
    
    #Display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pacman...kinda")
    
    #Entities
    root = pygame.Surface(screen.get_size())
    root.fill((255, 255, 255))
    
    #cherrie sprites
    cherry_count = 10
    cherries = []
    for c in range(10):
        cherries.append(pacmanSprites.Cherry(screen))
    
    #pacman sprites
    pacman = pacmanSprites.Pacman(screen) 
    
    #projectiles
    b = pacmanSprites.Projectile((0, 200), (200, 400))
    bulletGroup = []
    #for _ in range(10):    
        #bulletGroup.append(pacmanSprites.Projectile( (100, 200), (random.randint(150, 550), random.randint(150, 400))))
    
    #labels
    #topBar = pygame.Surface((screen.get_width(), 60))
    #topBar = topBar.convert()
    #topBar.fill((255, 255, 255))
    
    pmFont = pygame.font.Font("PAC-FONT.ttf", 30)
    impactFont = pygame.font.SysFont("Impact", 45)
    endPmFont = pygame.font.Font("PAC-FONT.ttf", 50)
    score = 0
    scoreLabel = pmFont.render("SCORE : ", 1, (255, 255, 0))
    #scoreNum = impactFont.render(str(score), 1, (255, 255, 0))
    
    game_over = endPmFont.render("GAME OVER", 1, (255, 255, 0))
    game_end_pic = endPmFont.render("1 2 3 4 5 6 7 8 9", 1, (255, 255, 0))
    
    timer = 20
    fracTick = 30
    
    #groups
    cherryGroup = pygame.sprite.Group(cherries)        
    allSprites = pygame.sprite.OrderedUpdates(pacman, cherryGroup, bulletGroup)

    #ACTION
    
    #Assign
    clock = pygame.time.Clock()
    gameRun = True
    ticker = fracTick
    
    #Looop
    while gameRun:
        #Time
        
        clock.tick(ticker)
        
        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRun = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.go_up()
                elif event.key == pygame.K_DOWN:
                    pacman.go_down()
                elif event.key == pygame.K_RIGHT:
                    pacman.go_right()                
                elif event.key == pygame.K_LEFT:
                    pacman.go_left()   
            if event.type == pygame.MOUSEBUTTONDOWN:
                bulletGroup.append(pacmanSprites.Projectile((320, 240), pygame.mouse.get_pos()))
                allSprites = pygame.sprite.OrderedUpdates(pacman, cherryGroup, bulletGroup)
                #print "hi"
        
        if pygame.sprite.spritecollide(pacman, cherryGroup, True):
            score += 1
            cherry_count -= 1                
        if cherry_count == 0:
            cherry_count = random.randint(1, 10)
            cherries = []
            for c in range(cherry_count):
                cherries.append(pacmanSprites.Cherry(screen))
            cherryGroup = pygame.sprite.Group(cherries)        
            allSprites = pygame.sprite.OrderedUpdates(pacman, cherryGroup, bulletGroup)                

        fracTick -= 1
        if fracTick < 0:
            timer -= 1
            fracTick = 30
        if timer < 0:
            for i in range(5):
                allSprites.clear(screen, root)
                pygame.display.flip()
                pygame.time.delay(250)
                allSprites.draw(screen)
                pygame.display.flip()
                pygame.time.delay(250)
            allSprites.clear(screen, root)
            screen.blit(game_over, (110, 175))
            screen.blit(game_end_pic, (135, 250))
            pygame.display.flip()
            pygame.time.delay(5000)
            break
        
        scoreNum = impactFont.render(str(score), 1, (255, 255, 0))
        timeLabel = impactFont.render(str(timer), 1, (255, 255, 0))
        
        #Refresh Screen
        screen.blit(root, (0, 0))
        #screen.blit(topBar, (0, 0))
        allSprites.clear(screen, root)
        allSprites.update()
        allSprites.draw(screen)
        screen.blit(scoreLabel, (10, 15))
        screen.blit(scoreNum, (185, 0))
        screen.blit(timeLabel, (570, 0))       
        
        pygame.display.flip()
        
    #close game
    pygame.quit()
    
main()