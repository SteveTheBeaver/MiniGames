import pygame
import random
import sys
import winsound
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
PINK = (255, 192, 203)

# Difficulty settings
DIFFICULTY_SPEEDS = {
    "Easy": (2, 5),
    "Medium": (4, 8),
    "Hard": (6, 10)
}

class Basket:
    def __init__(self):
        self.width = 120
        self.height = 50
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - 70
        self.speed = 10
        
    def move(self, direction):
        self.x += direction * self.speed
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))
        
    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

class FruitType:
    def __init__(self, color, points, size, is_banana=False):
        self.color = color
        self.points = points
        self.size = size
        self.is_banana = is_banana

class PowerUp:
    def __init__(self):
        self.size = 20
        self.reset()
        self.active = False
        self.duration = 10 * FPS  # 10 seconds
        self.timer = 0
        self.glow_size = 25
        self.angle = 0
        
    def reset(self):
        self.x = random.randint(self.size, WINDOW_WIDTH - self.size)
        self.y = -self.size
        self.speed = 5
        
    def move(self):
        self.y += self.speed
        self.angle += 2  # Rotate the star
        
    def draw(self, screen):
        # Draw outer glow
        glow_points = []
        for i in range(10):
            angle = (i * math.pi / 5) + math.radians(self.angle)
            radius = self.glow_size if i % 2 == 0 else self.glow_size * 0.5
            glow_points.append((
                self.x + radius * math.cos(angle),
                self.y + radius * math.sin(angle)
            ))
        pygame.draw.polygon(screen, PINK, glow_points)
        
        # Draw star
        star_points = []
        for i in range(10):
            angle = (i * math.pi / 5) + math.radians(self.angle)
            radius = self.size if i % 2 == 0 else self.size * 0.5
            star_points.append((
                self.x + radius * math.cos(angle),
                self.y + radius * math.sin(angle)
            ))
        pygame.draw.polygon(screen, GOLD, star_points)

class Fruit:
    TYPES = {
        "apple": FruitType(RED, 1, 25),
        "orange": FruitType(ORANGE, 2, 20),
        "grape": FruitType(PURPLE, 3, 15),
        "banana": FruitType(YELLOW, 4, 22, True)
    }
    
    def __init__(self, difficulty="Medium"):
        self.difficulty = difficulty
        self.reset()
        
    def reset(self):
        fruit_type = random.choice(list(self.TYPES.keys()))
        self.current_type = self.TYPES[fruit_type]
        self.size = self.current_type.size
        self.x = random.randint(self.size, WINDOW_WIDTH - self.size)
        self.y = -self.size
        speed_min, speed_max = DIFFICULTY_SPEEDS[self.difficulty]
        self.speed = random.uniform(speed_min, speed_max)
        
    def move(self):
        self.y += self.speed
        
    def draw(self, screen):
        if self.current_type.is_banana:
            # Draw banana shape
            banana_rect = pygame.Rect(self.x - self.size, self.y - self.size//2, 
                                    self.size * 2, self.size)
            pygame.draw.arc(screen, self.current_type.color, banana_rect, 
                          math.pi/4, math.pi, 3)
            pygame.draw.arc(screen, self.current_type.color, banana_rect, 
                          math.pi/4, math.pi*1.2, 3)
        else:
            pygame.draw.circle(screen, self.current_type.color, 
                             (int(self.x), int(self.y)), self.size)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Fruit Catcher")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.difficulty = "Medium"
        self.reset_game()
        
    def play_sound(self, frequency, duration):
        try:
            winsound.Beep(frequency, duration)
        except:
            pass  # Silently fail if sound doesn't work
        
    def reset_game(self):
        self.basket = Basket()
        self.fruits = [Fruit(self.difficulty)]
        self.power_up = PowerUp()
        self.score = 0
        self.score_multiplier = 1
        self.game_over = False
        self.game_started = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if not self.game_started:
                    if event.key == pygame.K_1:
                        self.difficulty = "Easy"
                        self.game_started = True
                        # Update existing fruits with new difficulty
                        for fruit in self.fruits:
                            fruit.difficulty = self.difficulty
                            fruit.reset()
                    elif event.key == pygame.K_2:
                        self.difficulty = "Medium"
                        self.game_started = True
                        # Update existing fruits with new difficulty
                        for fruit in self.fruits:
                            fruit.difficulty = self.difficulty
                            fruit.reset()
                    elif event.key == pygame.K_3:
                        self.difficulty = "Hard"
                        self.game_started = True
                        # Update existing fruits with new difficulty
                        for fruit in self.fruits:
                            fruit.difficulty = self.difficulty
                            fruit.reset()
                elif self.game_over:
                    self.reset_game()
                    
        return True
        
    def update(self):
        if not self.game_started or self.game_over:
            return
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.basket.move(-1)
        if keys[pygame.K_RIGHT]:
            self.basket.move(1)
            
        # Update power-up
        if self.power_up.active:
            self.power_up.timer -= 1
            if self.power_up.timer <= 0:
                self.score_multiplier = 1
                self.power_up.active = False
        else:
            self.power_up.move()
            if (self.power_up.y + self.power_up.size > self.basket.y and 
                self.basket.x < self.power_up.x < self.basket.x + self.basket.width):
                self.score_multiplier = 2
                self.power_up.active = True
                self.power_up.timer = self.power_up.duration
                self.play_sound(1000, 100)  # High-pitched power-up sound
            elif self.power_up.y > WINDOW_HEIGHT:
                self.power_up.reset()
            
        # Update fruits
        for fruit in self.fruits:
            fruit.move()
            
            # Check for collision with basket
            if (fruit.y + fruit.size > self.basket.y and 
                self.basket.x < fruit.x < self.basket.x + self.basket.width):
                self.score += fruit.current_type.points * self.score_multiplier
                self.play_sound(440, 50)  # Catch sound
                fruit.reset()
                
            # Check if fruit is missed
            elif fruit.y > WINDOW_HEIGHT:
                self.play_sound(200, 100)  # Miss sound
                self.game_over = True
                
    def draw(self):
        self.screen.fill(WHITE)
        
        if not self.game_started:
            # Draw title screen with clearer instructions
            title = self.font.render("Fruit Catcher", True, BLACK)
            
            # Draw instruction box
            instruction_box = pygame.Rect(WINDOW_WIDTH//4, 220, WINDOW_WIDTH//2, 250)
            pygame.draw.rect(self.screen, (240, 240, 240), instruction_box)
            pygame.draw.rect(self.screen, BLACK, instruction_box, 2)
            
            # Instructions text
            instructions_title = self.small_font.render("HOW TO PLAY", True, BLACK)
            difficulty_text = self.small_font.render("Select Your Difficulty Level:", True, BLACK)
            easy_text = self.small_font.render("Press 1 - Easy Mode", True, GREEN)
            medium_text = self.small_font.render("Press 2 - Medium Mode", True, ORANGE)
            hard_text = self.small_font.render("Press 3 - Hard Mode", True, RED)
            
            # Game controls preview
            controls_text = self.small_font.render("Game Controls:", True, BLACK)
            arrow_text = self.small_font.render("← → Arrow keys to move basket", True, BLACK)
            
            # Position all text elements
            self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
            self.screen.blit(instructions_title, (WINDOW_WIDTH//2 - instructions_title.get_width()//2, 240))
            self.screen.blit(difficulty_text, (WINDOW_WIDTH//2 - difficulty_text.get_width()//2, 280))
            self.screen.blit(easy_text, (WINDOW_WIDTH//2 - easy_text.get_width()//2, 340))
            self.screen.blit(medium_text, (WINDOW_WIDTH//2 - medium_text.get_width()//2, 370))
            self.screen.blit(hard_text, (WINDOW_WIDTH//2 - hard_text.get_width()//2, 400))
            self.screen.blit(controls_text, (WINDOW_WIDTH//2 - controls_text.get_width()//2, 430))
            self.screen.blit(arrow_text, (WINDOW_WIDTH//2 - arrow_text.get_width()//2, 460))
            
        elif self.game_over:
            # Draw game over screen
            game_over_text = self.font.render("Game Over!", True, BLACK)
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            restart_text = self.font.render("Press any key to restart", True, BLACK)
            self.screen.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 200))
            self.screen.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, 300))
            self.screen.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, 400))
            
        else:
            # Draw game objects
            self.basket.draw(self.screen)
            for fruit in self.fruits:
                fruit.draw(self.screen)
            if not self.power_up.active:
                self.power_up.draw(self.screen)
                
            # Draw score and multiplier
            score_text = self.font.render(str(self.score), True, BLACK)
            self.screen.blit(score_text, (20, 20))
            
            if self.score_multiplier > 1:
                multiplier_text = self.small_font.render(f"{self.score_multiplier}x", True, GOLD)
                self.screen.blit(multiplier_text, (20, 80))
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()