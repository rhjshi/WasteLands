''' Author: Richie Shi

    Date: 6 May 2017
    
    Description: This is the main program that includes the main game loop for
    the Wastelands, explore the map, complete the objectives, kill enemies and win!
    
    v.1 - Added basic background, floor and player object
    v.1a - Added player jumping, and background moving left/right, no camera up/down screw that
    v.1b - Adjusted graphics of player sprite to move based on mouse position, not movement,
    made to move more efficiently
    
    v.2 - Added Projectile Sprites and Weapon Sprite to follow mouse
    v.2a - adjusted update to kill bullet when off screen
    v.2b - adjusted projectile class to be associated with a weapon class
    
    v.3a - added moving enemies and contact damage
    v.3b - added health and lives stat, renamed Projectile class to PlayerBullet
    
    v.4a - changed primary weapon and added secondary weapon
    v.4b - enemy takes damage and dies, gun has fire rates and different projectile
    v.4c - yeti nerf, lower agro range, less speed in agro, less damage
    
    v.5a - added health bar and adjusted rect orientations to be more solid rather
           than based off of each other
    v.5b - added mobs
    
    v.6a - jk gonna spawn tons o' cows, player can jump 3 times now
    v.6b - now every yeti you kills spawns two, adjusted group logic or enemy sprites
           player respawns now
    v.6c - adjusted guns to shoot fast, floor scrolls with new image
    
'''
# I - import and initialize
import pygame, mySprites, random
pygame.init()
pygame.mixer.init()

# D - Display
screen = pygame.display.set_mode((960, 720))
pygame.display.set_caption("Wastelands")
root = pygame.Surface(screen.get_size())
root.fill((255, 255, 255))
root = root.convert()

def game_over(screen, root, allSprites):
    '''displays game over/win message takes screen, background surface, group with
    all the sprites, game over and game end pic, and sound to play, returns none'''
    sound = pygame.mixer.Sound("./Music/Mario Death Sound Effect.ogg")
    sound.set_volume(0.4)    
    #flashes screen then plays music and displays msg
    for i in range(5):
        allSprites.clear(screen, root)
        pygame.display.flip()
        pygame.time.delay(250)
        allSprites.draw(screen)
        pygame.display.flip()
        pygame.time.delay(250)
    sound.play()
    pygame.time.delay(3000)

def instructions():
    '''game loop for instruction screen'''
    # E - entities
    instructions = pygame.image.load("instructions.gif")
    screen.blit(instructions, (0, 0))
    # A - Action
        
    # A - Assign key variables
    clock = pygame.time.Clock()
    gameRun = True
        
    # L - Loop
    while gameRun:
        # T - Time
        clock.tick(10)
        
        # E - Event    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                else:
                    return False
            
        # R - Refresh
        pygame.display.flip()

def game():
    '''actual game loop'''
    # E - Entities   
    
    # sound effects
    gunshot = pygame.mixer.Sound("./Music/Gun Shot.ogg")
    gunshot.set_volume(0.1)
    spawn_yeti = pygame.mixer.Sound("./Music/Kobe.ogg")
    spawn_yeti.set_volume(0.35)
    
    #crosshair
    crosshair = mySprites.Crosshair()
    
    #background
    background = mySprites.Background(screen)
    floor = mySprites.Floor(screen, background)
    
    #moving characters
    player = mySprites.Player(screen, floor)
    gun = mySprites.Weapon(screen, player)

    #player stats    
    health_bar = mySprites.HealthBar(player)
    health_num = mySprites.HealthNum(player, health_bar)
    lives = mySprites.Lives(player)
    score_keeper = mySprites.ScoreKeeper()
    
    #enemy sprites
    yetiGroup = []
    for i in range(2):
        yetiGroup.append(mySprites.Yeti(background, floor, player, random.randint(1000, 2000)))
     
    #groups
    statGroup = pygame.sprite.Group(health_bar, health_num, lives, score_keeper)
    bulletGroup = pygame.sprite.Group()
    enemyBullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group(yetiGroup)
    
    allSprites = pygame.sprite.OrderedUpdates(background, enemies, player, floor, bulletGroup, enemyBullets, gun, statGroup, crosshair)
    
    # A - Action
    
    # A - Assign key variables
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    gameRun = True
    
    # L - Loop
    while gameRun:
        # T - Time
        clock.tick(30)
        
        # E - Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                #if player not dead
                if not player.get_dead():
                    #movement things
                    if event.key == pygame.K_a:
                        background.go_right()
                    if event.key == pygame.K_d:
                        background.go_left()
                    if event.key == pygame.K_w:
                        player.jump()
                    #changing weapon
                    if event.key == pygame.K_1:
                        gun.set_primary()
                    if event.key == pygame.K_2:
                        gun.set_secondary()
                
            #stoping movement things    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    background.right_idle()
                if event.key == pygame.K_d:
                    background.left_idle()
            
            #player shooting
            if pygame.mouse.get_pressed() == (1, 0, 0) and gun.get_can_fire():
                gunshot.play()
                gun.fire()
                bulletGroup.add(mySprites.PlayerBullet(screen, background, gun, pygame.mouse.get_pos()))
                allSprites = pygame.sprite.OrderedUpdates(background, enemies, player, floor, bulletGroup, enemyBullets, gun, statGroup, crosshair)
        
        #yeti randomly shoots
        for enemy in enemies:
            if enemy.get_attackmode():
                if random.randint(1, 40) == 1:
                    enemyBullets.add(mySprites.EnemyProjectile(background, enemy, player))
                    allSprites = pygame.sprite.OrderedUpdates(background, enemies, player, floor, bulletGroup, enemyBullets, gun, statGroup, crosshair)
        
        #if player contacts yetienemy   
        player_hit_yeti = pygame.sprite.spritecollide(player, enemies, False)
        if player_hit_yeti:
            for enemy in player_hit_yeti:
                player.take_dmg(enemy.attack())     
        
        #player getting hit by enemy bullet   
        bullet_hit_player = pygame.sprite.spritecollide(player, enemyBullets, False)        
        for bullet in bullet_hit_player:
            player.take_dmg(3)  
            bullet.kill()
            enemyBullets.remove(bullet)
        
        #bullet hitting enemy
        for bullet in bulletGroup:   
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies, False)        
            for enemy in enemy_hit_list:
                enemy.take_dmg(bullet.get_dmg())
                #kill yeti and spawn two more
                if enemy.get_health() <= 0:
                    spawn_yeti.play()
                    xlocation = enemy.rect.centerx
                    enemy.kill()
                    yetiGroup.remove(enemy)
                    score_keeper.add_score(420)
                    for i in range(2):
                        yetiGroup.append(mySprites.Yeti(background, floor, player, random.randint(xlocation-500, xlocation+500)))
                    enemies = pygame.sprite.Group(yetiGroup)
                    allSprites = pygame.sprite.OrderedUpdates(background, enemies, player, floor, bulletGroup, enemyBullets, gun, statGroup, crosshair)
                bullet.kill()
                bulletGroup.remove(bullet)
        
        #if player has fallen thru bottom of screen and died
        if player.rect.top > screen.get_height():
            gameRun = False
            game_over(screen, root, allSprites)
         
        # R - Refresh Screen
        allSprites.clear(screen, root)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
        
    #close game
    pygame.mouse.set_visible(True)
    return False


def main():
    '''loop that runs instruction screen and main game loop'''
    quitGame = False

    #music
    pygame.mixer.music.load("./Music/At Night.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)    
    
    while not quitGame:
        quitGame = instructions()
        
        if not quitGame:
            quitGame = game()
            
    pygame.mixer.fadeout(2000)        
    pygame.time.delay(2000)
    pygame.quit()
    
main()