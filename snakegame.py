from tkinter import *
import random
import winsound  # Added for Windows sound support

# Global speed constants
SLOW_SPEED = 145
REGULAR_SPEED = 125
FAST_SPEED = 90

# Global game constants
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "purple"
GREEN_GRAPE_COLOR = "#32CD32"  # Lime green color for green grapes
RED_GRAPE_COLOR = "red"
BACKGROUND_COLOR = "#000000"

# Global variable to store selected speed
GAME_SPEED = REGULAR_SPEED

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self, is_green_grape=False, is_red_grape=False):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        self.is_green_grape = is_green_grape
        self.is_red_grape = is_red_grape

        if is_green_grape:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=GREEN_GRAPE_COLOR, tag="food")
        elif is_red_grape:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=RED_GRAPE_COLOR, tag="food")
        else:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, high_score

        # Play a beep sound when eating a grape
        winsound.Beep(500, 50)  # Added Windows sound effect

        # Check if it's a green grape or red grape or regular food
        if food.is_green_grape:
            score += 2  # Green grape is worth 2 points, double the purple grape
            # Add two body parts when green grape is eaten
            for _ in range(2):
                last_x, last_y = snake.coordinates[-1]
                new_body_part = (last_x, last_y)
                snake.coordinates.append(new_body_part)
                square = canvas.create_rectangle(last_x, last_y, last_x + SPACE_SIZE, last_y + SPACE_SIZE, fill=SNAKE_COLOR)
                snake.squares.append(square)
        
        elif food.is_red_grape:
            score += 4  # Red grape is worth 4 points, double the green grape
            # Add four body parts when red grape is eaten
            for _ in range(4):
                last_x, last_y = snake.coordinates[-1]
                new_body_part = (last_x, last_y)
                snake.coordinates.append(new_body_part)
                square = canvas.create_rectangle(last_x, last_y, last_x + SPACE_SIZE, last_y + SPACE_SIZE, fill=SNAKE_COLOR)
                snake.squares.append(square)
        else:
            score += 1  # Regular food is worth 1 point
            # Add one body part when purple grape is eaten
            last_x, last_y = snake.coordinates[-1]
            new_body_part = (last_x, last_y)
            snake.coordinates.append(new_body_part)
            square = canvas.create_rectangle(last_x, last_y, last_x + SPACE_SIZE, last_y + SPACE_SIZE, fill=SNAKE_COLOR)
            snake.squares.append(square)

        # Update high score if current score is higher
        if score > high_score:
            high_score = score

        label.config(text="Score:{} Hi Score:{}".format(score, high_score))

        canvas.delete("food")

        # Randomly decide food type
        random_value = random.random()
        if random_value < 0.1:  # 10% chance for red grape
            food = Food(is_red_grape=True)
        elif random_value < 0.3:  # 20% chance for green grape
            food = Food(is_green_grape=True)
        else:  # 70% chance for purple grape
            food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(GAME_SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="purple", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 100,
                       font=('consolas',20), text="Press Enter to Restart", fill="red", tag="restart")
    window.bind('<Return>', restart_game)


def restart_game(event=None):
    global snake, food, score, direction

    # Reset game state
    canvas.delete(ALL)
    score = 0
    direction = 'down'
    label.config(text="Score:{} Hi Score:{}".format(score, high_score))

    # Unbind the restart key
    window.unbind('<Return>')

    # Show speed selection screen
    show_speed_selection()


def select_speed(speed):
    global GAME_SPEED
    
    # Set game speed based on selection
    if speed == 'slow':
        GAME_SPEED = SLOW_SPEED
    elif speed == 'fast':
        GAME_SPEED = FAST_SPEED
    else:  # default to regular
        GAME_SPEED = REGULAR_SPEED
    
    # Proceed to start the game
    start_game()


def show_speed_selection():
    canvas.delete(ALL)
    
    # Title
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 - 150,
                       font=('consolas', 50), text="Worm & Grapes", fill="purple")
    
    # Speed Selection Instructions
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 - 50,
                       font=('consolas', 25), text="Select Game Speed", fill="white")
    
    # Speed Buttons
    slow_button = Button(window, text="Slow", font=('consolas', 20), 
                         command=lambda: select_speed('slow'))
    regular_button = Button(window, text="Regular", font=('consolas', 20), 
                            command=lambda: select_speed('regular'))
    fast_button = Button(window, text="Fast", font=('consolas', 20), 
                         command=lambda: select_speed('fast'))
    
    # Place buttons
    canvas.create_window(canvas.winfo_width()/2 - 150, canvas.winfo_height()/2 + 50, 
                         window=slow_button)
    canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 50, 
                         window=regular_button)
    canvas.create_window(canvas.winfo_width()/2 + 150, canvas.winfo_height()/2 + 50, 
                         window=fast_button)
    
    # Additional instructions
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 150,
                       font=('consolas', 15), text="Use WASD or Arrow Keys to Move", fill="yellow")


def show_title_screen():
    canvas.delete(ALL)
    # Title
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 - 100,
                       font=('consolas', 50), text="Worm & Grapes", fill="purple")
    # Instructions
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 50,
                       font=('consolas', 20), text="Press SPACE to Start", fill="white")
    
    # Add arrow key instructions
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 100,
                       font=('consolas', 15), text="Use WASD or Arrow Keys to Move", fill="yellow")
    
    # Bind space key to speed selection
    window.bind('<space>', lambda event: show_speed_selection())


def start_game(event=None):
    # Remove any existing buttons
    for widget in window.winfo_children():
        if isinstance(widget, Button):
            widget.destroy()
    
    # Reset game state
    global snake, food, score, direction
    canvas.delete(ALL)
    score = 0
    direction = 'down'
    label.config(text="Score:{} Hi Score:{}".format(score, high_score))

    # Create new snake and food - always start with regular food
    snake = Snake()
    food = Food()

    # Start game loop
    next_turn(snake, food)


# Set up the window
window = Tk()
window.title("Wow Such Wonderful Grapes!")
window.resizable(False, False)

# Initialize high score for the entire game session
high_score = 0

score = 0
direction = 'down'

label = Label(window, text="Score:{} Hi Score:{}".format(score, high_score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center the window on the computer screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind direction keys
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Add WASD controls
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))

# Show title screen initially
show_title_screen()

window.mainloop()