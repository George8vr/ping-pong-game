from pygame import *

init()

# Window
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Ping Pong Game')

# Colors
BG = (200, 255, 255)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 180)

# Clock
clock = time.Clock()
FPS = 60

# Paddle
paddle_width = 15
paddle_height = 120
paddle_speed = 5

# Ball
ball_size = 50
ball_speed_x = 4
ball_speed_y = 4

# Speed limits
MAX_BALL_SPEED = 10
MAX_PADDLE_SPEED = 12

# Scores & Timer
score_p1 = 0
score_p2 = 0
WIN_SCORE = 5
start_time = 0
stop_time = 0

# Text
font.init()
game_font = font.SysFont('Arial', 30)
p1_wintext = game_font.render('Player 1 Wins!', True, RED)
p2_wintext = game_font.render('Player 2 Wins!', True, RED)
start_text = game_font.render('Press SPACE to start', True, BLUE)
restart_text = game_font.render('Press SPACE to restart', True, BLUE)

# Sprite classes
class GameSprite(sprite.Sprite):
    def __init__(self, color, x, y, width, height):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= paddle_speed
        if keys[K_s] and self.rect.y < win_height - paddle_height:
            self.rect.y += paddle_speed

    def update_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= paddle_speed
        if keys[K_DOWN] and self.rect.y < win_height - paddle_height:
            self.rect.y += paddle_speed

class Ball(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        img = transform.scale(image.load('ball.png').convert(), (ball_size, ball_size))
        img.set_colorkey((255, 255, 255))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Objects
player1 = Player(WHITE, 20, 190, paddle_width, paddle_height)
player2 = Player(WHITE, 665, 190, paddle_width, paddle_height)
ball = Ball(325, 225)

# Game variables
game = True
started = False
finish = False
end_text = None

in_menu = True
difficulty = 1

# Main loop
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        # Start or restart with SPACE
        if e.type == KEYDOWN:
            if in_menu:
                if e.key == K_1: difficulty = 1
                if e.key == K_2: difficulty = 2
                if e.key == K_3: difficulty = 3
            
            # Start or restart with SPACE
            if e.key == K_SPACE:
                if finish: # if the game has finished, go back to the menu
                    in_menu = True
                    started = False
                    finish = False
                elif in_menu: # if in menu, start the game
                    in_menu = False
                    started = True
                    finish = False
                    end_text = None
                    
                    score_p1 = 0
                    score_p2 = 0
                    start_time = time.get_ticks()
                    stop_time = 0

                    ball.rect.x = 325
                    ball.rect.y = 225
                    player1.rect.y = 190
                    player2.rect.y = 190
                    
                    paddle_speed = 5  # Reset paddle speed to default

                    # Set ball speed based on difficulty
                    if difficulty == 1:
                        ball_speed_x = 5
                        ball_speed_y = 5
                    elif difficulty == 2:
                        ball_speed_x = 5
                        ball_speed_y = 5
                    elif difficulty == 3:
                        ball_speed_x = 9
                        ball_speed_y = 9
                        paddle_speed = 12

    window.fill(BG)

    if started:
        draw.line(window, (150, 200, 200), (350, 0), (350, win_height), 3)

    # Draw paddles and ball
    player1.reset()
    player2.reset()
    ball.reset()

    if started and not finish:
        # Paddle movement
        player1.update_left()
        player2.update_right()

        # Ball movement
        ball.rect.x += ball_speed_x
        ball.rect.y += ball_speed_y

        # Bounce on top and bottom
        if ball.rect.y <= 0 or ball.rect.y >= win_height - ball_size:
            ball_speed_y *= -1

        # Bounce on paddles
        if sprite.collide_rect(player1, ball):
            ball_speed_x = abs(ball_speed_x) # direction change to right
            if difficulty == 2:
                ball_speed_x *= 1.15
                ball_speed_y *= 1.15
                paddle_speed *= 1.15
        
        # 2. Collision with Player 2 (Left)
        if sprite.collide_rect(player2, ball):
            ball_speed_x = -abs(ball_speed_x) # direction change to left
            if difficulty == 2:
                ball_speed_x *= 1.15
                ball_speed_y *= 1.15
                paddle_speed *= 1.15

        # Cap ball and paddle speeds to prevent them from exceeding maximum values
        if difficulty == 2:
            # Cap horizontal ball speed
            if abs(ball_speed_x) > MAX_BALL_SPEED:
                ball_speed_x = MAX_BALL_SPEED if ball_speed_x > 0 else -MAX_BALL_SPEED
            
            # Cap vertical ball speed
            if abs(ball_speed_y) > MAX_BALL_SPEED:
                ball_speed_y = MAX_BALL_SPEED if ball_speed_y > 0 else -MAX_BALL_SPEED
            
            # Cap paddle speed
            if paddle_speed > MAX_PADDLE_SPEED:
                paddle_speed = MAX_PADDLE_SPEED

            

        if ball.rect.x < 0:
            score_p2 += 1
            if score_p2 >= WIN_SCORE:
                finish = True
                end_text = p2_wintext
                stop_time = time.get_ticks()
            else:
                ball.rect.x = 325
                ball.rect.y = 225
                ball_speed_x *= -1

        if ball.rect.x > win_width - 50:
            score_p1 += 1
            if score_p1 >= WIN_SCORE:
                finish = True
                end_text = p1_wintext
                stop_time = time.get_ticks()
            else:
                ball.rect.x = 325
                ball.rect.y = 225
                ball_speed_x *= -1

    if started:
        score1_text = game_font.render(str(score_p1), True, BLACK)
        score2_text = game_font.render(str(score_p2), True, BLACK)
        window.blit(score1_text, (320, 10))
        window.blit(score2_text, (365, 10))

        current = stop_time if finish else time.get_ticks()
        elapsed = (current - start_time) // 1000
        minutes = elapsed // 60
        seconds = elapsed % 60
        timer_text = game_font.render(f'{minutes:02d}:{seconds:02d}', True, BLACK)
        window.blit(timer_text, (10, 10))

    if in_menu:
        # Display the difficulty selection menu
        title_txt = game_font.render("SELECT DIFFICULTY:", True, BLACK)
        
        # Highlight the selected difficulty
        c1 = BLUE if difficulty == 1 else BLACK
        c2 = BLUE if difficulty == 2 else BLACK
        c3 = BLUE if difficulty == 3 else BLACK
        
        txt_l1 = game_font.render("1. Easy (Normal)", True, c1)
        txt_l2 = game_font.render("2. Medium (Fast)", True, c2)
        txt_l3 = game_font.render("3. Hard (Dynamic)", True, c3)
        launch_txt = game_font.render("Press SPACE to Start", True, RED)
        
        # Blit the texts to the window
        window.blit(title_txt, (230, 130))
        window.blit(txt_l1, (250, 180))
        window.blit(txt_l2, (250, 220))
        window.blit(txt_l3, (250, 260))
        window.blit(launch_txt, (225, 330))
        
    elif finish:
        window.blit(end_text, (260, 210))
        # Display restart message
        restart_menu_txt = game_font.render('Press SPACE for Menu', True, BLUE)
        window.blit(restart_menu_txt, (220, 250))

    display.update()
    clock.tick(FPS)

quit()