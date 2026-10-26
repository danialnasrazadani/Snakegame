from cProfile import label
from tkinter import *
from random import randint
import os
import sys


#-------------------------------
class snake:
    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares =[]

        for i in range(0 , BODY_SIZE):
            self.coordinates.append([0,0])

        for x,y in self.coordinates:
            square = canvas.create_rectangle(x, y , x + SPACE_SIZE , y + SPACE_SIZE , fill=SNAKE_COLOR, tag="snake" )
            self.squares.append(square)

class Food:
    def __init__(self):
        x = randint(0, (GAME_WIDTH // SPACE_SIZE) - 1 ) * SPACE_SIZE
        y = randint(0, (GAME_HIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x , y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x ,y =snake.coordinates[0]

    if DIRECTION == "up":
        y -= SPACE_SIZE
    elif DIRECTION == "down":
        y += SPACE_SIZE
    elif DIRECTION == "left":
        x -= SPACE_SIZE
    elif DIRECTION == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0 , [x,y])
    square= canvas.create_rectangle(x , y , x + SPACE_SIZE ,y + SPACE_SIZE ,fill= SNAKE_COLOR)
    snake.squares.insert(0 , square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text= f"score {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_game_over():
        game_over()
    else:
        window.after(SLOWNESS, next_turn,snake, food)


def change_direction(new_dir):
    global DIRECTION

    if new_dir == "left":
        if DIRECTION != "right":
            DIRECTION = new_dir
    elif new_dir == "right":
        if DIRECTION != "left":
            DIRECTION = new_dir
    elif new_dir == "up":
        if DIRECTION != "down":
            DIRECTION = new_dir
    elif new_dir == "down":
        if DIRECTION != "up":
            DIRECTION = new_dir


def check_game_over():
    x ,y =snake.coordinates[0]

    if x < 0 or x > GAME_WIDTH:
        return True

    if y < 0 or y > GAME_HIGHT:
        return True

    for sq in snake.coordinates[1:]:
        if x == sq[0] and y == sq[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() /2 , canvas.winfo_height() /2 , font= ("Terminal",60)
                       ,text ="GAME OVER!",fill = "#630303" ,tag="gameover")

def restart_program ():
    path = sys.executable
    os.execl(path ,path ,*sys.argv)


#-------------------------------

GAME_WIDTH = 1400
GAME_HIGHT = 700
SPACE_SIZE = 50
BODY_SIZE = 3
SLOWNESS = 200
SNAKE_COLOR ="green"
BACKGROUND_COLOR ="black"
FOOD_COLOR ="red"
score=0
DIRECTION="down"

#-------------------------------

window = Tk()
window.title("snake game")
window.resizable(False ,False)

label = Label(window, text=f"score:{score}" , font=("Sylfaen",30))
label.pack()

canvas= Canvas(window, bg=BACKGROUND_COLOR , width=GAME_WIDTH , height= GAME_HIGHT)
canvas.pack()

restart= Button(window,text="Restart" ,fg="blue", command=restart_program )
restart.pack()
window.update()

window_width= window.winfo_width()
window_height= window.winfo_height()

screen_width= window.winfo_screenwidth()
screen_height= window.winfo_screenheight()

x= int((screen_width /2)-(window_width /2))
y= int((screen_height /2)-(window_height /2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Left>", lambda event: change_direction("left") )
window.bind("<Right>", lambda event: change_direction("right") )
window.bind("<Up>" , lambda event: change_direction("up") )
window.bind("<Down>" , lambda event: change_direction("down") )

snake = snake()
food = Food()
next_turn(snake, food)

window.mainloop()


