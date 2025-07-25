import tkinter as tk
import random
import os

# Constants
GAME_WIDTH = 600
GAME_HEIGHT = 400
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BG_COLOR = "#000000"
HIGH_SCORE_FILE = "highscore.txt"

# Initialize global values
score = 0
high_score = 0
speed = 100
direction = "right"

# Load high score
if os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, "r") as f:
        high_score = int(f.read())

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global score, speed, high_score

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
        score += 1
        if score > high_score:
            high_score = score
            with open(HIGH_SCORE_FILE, "w") as f:
                f.write(str(high_score))
        update_score()
        canvas.delete("food")
        food = Food()
        # Increase speed every 5 points
        if score % 5 == 0:
            increase_speed()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)

def change_direction(new_dir):
    global direction
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
    if new_dir != opposites.get(direction):
        direction = new_dir

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for part in snake.coordinates[1:]:
        if x == part[0] and y == part[1]:
            return True
    return False

def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, text=f"Game Over\nScore: {score}", fill="red", font=("Arial", 24))

def update_score():
    label.config(text=f"Score: {score}   High Score: {high_score}")

def increase_speed():
    global speed
    if speed > 30:
        speed -= 5

def start_game():
    global snake, food, score, speed, direction
    score = 0
    speed = 100
    direction = "right"
    canvas.delete(tk.ALL)
    update_score()
    snake = Snake()
    food = Food()
    next_turn(snake, food)

# Setup window
window = tk.Tk()
window.title("Enhanced Snake Game")
window.resizable(False, False)

label = tk.Label(window, text=f"Score: {score}   High Score: {high_score}", font=("Arial", 16))
label.pack()

canvas = tk.Canvas(window, bg=BG_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

start_button = tk.Button(window, text="Start Game", font=("Arial", 14), command=start_game)
start_button.pack(pady=10)

# Controls
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))

# Launch the window
window.mainloop()
