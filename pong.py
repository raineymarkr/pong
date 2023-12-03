import pygame
import time
import numpy as np

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Pong')
pygame.font.init()
myfont = pygame.font.SysFont('ocraext.ttf', 30)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
score = [0,0]

#Game Settings
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_size = (40,40)
start_time = None
delay_trigger = False
player_paddle_pos = pygame.Vector2(100, screen.get_height() / 2 - 40)
computer_paddle_pos = pygame.Vector2(screen.get_width() - 140, screen.get_height() / 2 - 40)
paddle_size = (40,120)

# Game Loop
running = True
reset = True
while running:

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill('black')
    score_text = myfont.render(f'Player: {score[0]}   Computer: {score[1]}',False,(0,255,0))
    screen.blit(score_text, (screen.get_width()/2-100, 50))
    #Reset Game
    if reset == True:
        player_paddle_pos = pygame.Vector2(100, screen.get_height() / 2 - 40)
        computer_paddle_pos = pygame.Vector2(screen.get_width() - 140, screen.get_height() / 2 - 40)
        ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        ball_vel = pygame.Vector2(-300 * dt, 0)
        reset = False

    #Draw paddles and ball
    player_paddle = pygame.draw.rect(screen, (0,255,0), (player_paddle_pos, paddle_size))
    computer_paddle = pygame.draw.rect(screen, (0,255,0), (computer_paddle_pos, paddle_size))
    ball = pygame.draw.rect(screen, (0,255,0), (ball_pos, ball_size))

    #Listen for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if player_paddle_pos.y > 0:
            player_paddle_pos.y -= 300 * dt
        else:
            player_paddle_pos.y = 0
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if player_paddle_pos.y < screen.get_height() - paddle_size[1]:
            player_paddle_pos.y += 300*dt
        else:
            player_paddle_pos.y = screen.get_height() - paddle_size[1]

    
    #Ball Collision Logic
    if ball.colliderect(player_paddle) or ball.colliderect(computer_paddle): 
        #Decide whether Player or Computer paddle      
        if ball.colliderect(player_paddle):
            paddle = player_paddle
        if ball.colliderect(computer_paddle):
            paddle = computer_paddle

        # Define regions
        middle_height = paddle.height / 6  # Smaller middle region
        top_height = (paddle.height - middle_height) / 2  # Adjust top and bottom regions
        bottom_height = top_height

        top = pygame.Rect(paddle.left, paddle.top, paddle.width, top_height)
        middle_region = pygame.Rect(paddle.left, paddle.top + top_height, paddle.width, middle_height)
        bottom = pygame.Rect(paddle.left, paddle.top + top_height + middle_height, paddle.width, bottom_height)


        #Define effects per region
        if ball.colliderect(top):
            ball_vel.x *= -1
            ball_vel.y -= 300 * dt
            if paddle == player_paddle:
                ball_pos.x += 5
            else:
                ball_pos.x -= 5
        elif ball.colliderect(bottom):
            ball_vel.x *= -1
            ball_vel.y += 300 * dt
            if paddle == player_paddle:
                ball_pos.x += 5
            else:
                ball_pos.x -= 5
        else:
            ball_vel.x *= -1
            if paddle == player_paddle:
                ball_pos.x += 5
            else:
                ball_pos.x -= 5
    
    #Interactions with top and bottom
    elif ball_pos.y < 0:
        ball_pos.y += 10
        ball_vel.y *= -1
    elif ball_pos.y > screen.get_height() - ball_size[0]:
        ball_pos.y -= 10
        ball_vel.y *= -1

    #Score regions and reset
    elif ball_pos.x < 100:
        score[1] += 1
        reset = True 
    elif ball_pos.x > screen.get_width() - 140:
        score[0] += 1
        reset = True        

    #Else the ball moves
    else:
        print(ball_vel)
        if ball_vel.y > 15 or ball_vel.y < -15:
            ball_vel.y = np.sign(ball_vel.y)*15
        ball_pos += ball_vel
    
    # Computer AI
    if ball_vel.x > 0:  # Move the paddle only if the ball is moving towards it
        if not delay_trigger:
            delay = np.abs(np.random.normal(1, 0.5))  # Delay in seconds
            delay_trigger = True

        else:
            delay = 0

        if start_time is None:
            start_time = time.time()

        if time.time() - start_time > delay:
            if ball_pos.y + ball_size[1] / 2 > computer_paddle_pos.y + paddle_size[1] / 2:
                # Ball is below the paddle's center, move paddle down
                if computer_paddle_pos.y + paddle_size[1] < screen.get_height():
                    computer_paddle_pos.y += 300 * dt
            elif ball_pos.y + ball_size[1] / 2 < computer_paddle_pos.y + paddle_size[1] / 2:
                # Ball is above the paddle's center, move paddle up
                if computer_paddle_pos.y > 0:
                    computer_paddle_pos.y -= 300 * dt
    else:
    # Reset the reaction time when the ball is not moving towards the AI paddle
        start_time = None
        delay_trigger = False

    # Update the screen
    pygame.display.flip()



# Quit Pygame
pygame.quit()
