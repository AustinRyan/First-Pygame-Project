import pygame
import os
pygame.font.init()

#Creating the window or main surface with the desired width and height, WIN = window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#Window name
pygame.display.set_caption("First Pygame Project!")
WHITE = (255,255,255)
BLACK = (0,0,0)
BORDER = pygame.Rect(WIDTH//2 -5,0,10,HEIGHT)
FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_AMMO = 3
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40
RED = (255,0,0)
YELLOW = (255,255,0)

HEALTH_FONT =  pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#How to create a new event +1 and +2 makes sure the event is different,
# if they were both +1 then it would be the same event
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT= pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
#Below line scales the image of space ship to a smaller size, so it is not extreamly large
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
#Below line scales the image of space ship to a smaller size, so it is not extreamly large
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

#Load new backround from Assets folder
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #RGB inside fill for color
        WIN.blit(SPACE,(0,0))
        pygame.draw.rect(WIN,BLACK, BORDER)
        red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        WIN.blit(yellow_health_text, (10, 10))


        #anytime you have text or images use WIN.blit
        WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
        WIN.blit(RED_SPACESHIP, (red.x,red.y))



        for bullet in red_bullets:
            pygame.draw.rect(WIN,RED, bullet)

        for bullet in yellow_bullets:
            pygame.draw.rect(WIN,YELLOW, bullet)
        pygame.display.update()


#if the a key is clicked then move yellows x axis to the left by 5 (constant velocity is set at 5)
def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: #Left Key
            yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VELOCITY < BORDER.x: #Right Key
            yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: #Up Key
            yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT -15: #Down Key
            yellow.y += VELOCITY

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: #Left Key
            red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VELOCITY < WIDTH: #Right Key
            red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: #Up Key
            red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT -15: #Down Key
            red.y += VELOCITY

#This function will handle the bullets and what they do when there is collision
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY

        if red.colliderect(bullet):
            #Making new event saying that red was hit by yellow
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY

        if yellow.colliderect(bullet):
            #Making new event saying that yellow was hit by red
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



 


#######LEAVING OFF RIGHT HERE. Next step is to create an event when the bullet collides with a spaceship







def main():
    #parameters are x,y, width, height, for rect, This will put where you want your redpaceship to control
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    #game loop (infinite loop until game ends) so the game doesnt open and close immediately 
    run = True
    while run:
        #This clock function makes sure the game doesnt go above the desired framerate we want
        clock.tick(FPS)

        for event in pygame.event.get():
            #if user quit the window
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_AMMO :
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_AMMO:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
            if event.type == RED_HIT:
                red_health -= 1
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <=0:
            winner_text = "Yellow wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text) #Theres a winner
            break




        #KEYS_PRESSED WILL RECOGNIZE AND READ WHICH KEYS ARE BEING PRESSED
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)
        handle_bullets(yellow_bullets, red_bullets, yellow,red)
        
        
        draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health)

            

    pygame.quit()

#If we run the file the game will load up, and not load up automatically if imported
if __name__ == "__main__":
    main()




