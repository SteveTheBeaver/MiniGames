import pygame, sys, random
 
pygame.init()
 
WIDTH, HEIGHT = 1280, 720
 
GAME_FONT = pygame.font.SysFont("Consolas", int(WIDTH/20))
TITLE_FONT = pygame.font.SysFont("Consolas", int(WIDTH/10))
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
CLOCK = pygame.time.Clock()

# Game states
TITLE_SCREEN = 0
GAME_SCREEN = 1
END_SCREEN = 2
current_state = TITLE_SCREEN

# paddles
player = pygame.Rect(WIDTH-110, HEIGHT//2-50, 10, 100)
opponent = pygame.Rect(100, HEIGHT//2-50, 10, 100)
player_score, opponent_score = 0, 0

# ball
ball = pygame.Rect(WIDTH//2-10, HEIGHT//2-10, 20, 20)
x_speed, y_speed = 1, 1

def reset_game():
    global player_score, opponent_score, current_state, ball, x_speed, y_speed
    player_score = 0
    opponent_score = 0
    ball.center = (WIDTH//2, HEIGHT//2)
    x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
    current_state = GAME_SCREEN

def draw_title_screen():
    SCREEN.fill("black")
    # Draw title
    title_text = TITLE_FONT.render("PONG", True, "white")
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    SCREEN.blit(title_text, title_rect)
    
    # Draw instructions
    instruction_text1 = GAME_FONT.render("Press SPACE to start", True, "white")
    instruction_text2 = GAME_FONT.render("Use the UP and DOWN arrows to move", True, "white")
    instruction_text3 = GAME_FONT.render("First to 20 points wins!", True, "white")
    
    # Position instructions with some spacing between them
    instruction_rect1 = instruction_text1.get_rect(center=(WIDTH//2, HEIGHT*2//3))
    instruction_rect2 = instruction_text2.get_rect(center=(WIDTH//2, HEIGHT*2//3 + 50))
    instruction_rect3 = instruction_text3.get_rect(center=(WIDTH//2, HEIGHT*2//3 + 100))
    
    SCREEN.blit(instruction_text1, instruction_rect1)
    SCREEN.blit(instruction_text2, instruction_rect2)
    SCREEN.blit(instruction_text3, instruction_rect3)

def draw_game_screen():
    SCREEN.fill("black")
    pygame.draw.rect(SCREEN, "white", player)
    pygame.draw.rect(SCREEN, "white", opponent)
    pygame.draw.circle(SCREEN, "white", ball.center, 10)
    
    player_score_text = GAME_FONT.render(str(player_score), True, "white")
    opponent_score_text = GAME_FONT.render(str(opponent_score), True, "white")
    SCREEN.blit(player_score_text, (WIDTH//2+50, 50))
    SCREEN.blit(opponent_score_text, (WIDTH//2-50, 50))

def draw_end_screen():
    SCREEN.fill("black")
    winner = "Player" if player_score >= 20 else "Opponent"
    
    # Draw winner announcement
    winner_text = TITLE_FONT.render(f"{winner} Wins!", True, "white")
    winner_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    SCREEN.blit(winner_text, winner_rect)
    
    # Draw final score
    score_text = GAME_FONT.render(f"Final Score: {opponent_score} - {player_score}", True, "white")
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(score_text, score_rect)
    
    # Draw restart instruction
    restart_text = GAME_FONT.render("Press SPACE to play again", True, "white")
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT*2//3))
    SCREEN.blit(restart_text, restart_rect)

while True:
    keys_pressed = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if current_state == TITLE_SCREEN:
                current_state = GAME_SCREEN
            elif current_state == END_SCREEN:
                reset_game()
    
    if current_state == TITLE_SCREEN:
        draw_title_screen()
    
    elif current_state == GAME_SCREEN:
        # Game logic
        if keys_pressed[pygame.K_UP]:
            if player.top > 0:
                player.top -= 2
        if keys_pressed[pygame.K_DOWN]:
            if player.bottom < HEIGHT:
                player.bottom += 2

        if ball.y >= HEIGHT:
            y_speed = -1
        if ball.y <= 0:
            y_speed = 1
        if ball.x <= 0:
            player_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
        if ball.x >= WIDTH:
            opponent_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
        if player.x - ball.width <= ball.x <= player.x and ball.y in range(player.top-ball.width, player.bottom+ball.width):
            x_speed = -1
        if opponent.x - ball.width <= ball.x <= opponent.x and ball.y in range(opponent.top-ball.width, opponent.bottom+ball.width):
            x_speed = 1

        ball.x += x_speed * 2
        ball.y += y_speed * 2

        if opponent.y < ball.y:
            opponent.top += 1
        if opponent.bottom > ball.y:
            opponent.bottom -= 1
        
        # Check for winner
        if player_score >= 20 or opponent_score >= 20:
            current_state = END_SCREEN
        
        draw_game_screen()
    
    elif current_state == END_SCREEN:
        draw_end_screen()

    pygame.display.update()
    CLOCK.tick(300)