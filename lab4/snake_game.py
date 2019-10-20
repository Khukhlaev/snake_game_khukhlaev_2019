# coding: UTF-8
from tkinter import *
from random import randrange as rnd

# make window
root = Tk()
root.title("Snake game")
root.geometry('1020x720')

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

# make global variables
game_over = False
gamer_name = ""
score = 0
tail = []  # It will be list of the tail, tail[i][0] - reference to part of the tail (rectangle),
# tail[i][1] - direction of each part of the tail at the moment
bonus_x = 0  # It will be bonus coordinates (x', y')
bonus_y = 0  # x' = 20 * x, y' = 20 * y
direction = ""
head = ""  # It will be reference to snake head
bonus = ""  # It will be reference to bonus
new_tail_x = 0  # It will be new part of tail coordinates (x', y')
new_tail_y = 0  # x' = 20 * x, y' = 20 * y
Pause = False
text = ""  # It will be reference to the text object which show score
button_new_game = ""  # It will be reference to the new game button
button_exit = ""  # It will be reference to the exit button
events = []  # It will be list of keypress events
enter_name = ""  # It will be reference to the text box where gamer will enter his nickname
label = ""  # It will be reference to the label
button_enter = ""  # It will be reference to the enter button
velocity = 0
max_score = 0
enter_velocity = ""  # It will be reference to the text box where gamer will enter velocity
file = open('leaderboard.txt', 'a')


def draw_bonus():
    """this function draw a bonus (circle) in a random place, radius of this circle is 10"""
    global bonus_x, bonus_y, bonus, head
    while True:  # To prevent bug if bonus will be drawn in the snake head or snake tail
        bonus_x = rnd(3, 50, 1)
        bonus_y = rnd(3, 35, 1)
        Breaking = True
        if 20 * bonus_x == canv.coords(head)[2] and 20 * bonus_y == canv.coords(head)[3]:
            Breaking = False
        for i in range(len(tail)):
            if tail[i][0] != "":
                if 20 * bonus_x == canv.coords(tail[i][0])[2] and 20 * bonus_y == canv.coords(tail[i][0])[3]:
                    Breaking = False
        if Breaking:
            break
    bonus = canv.create_oval(20 * bonus_x - 15, 20 * bonus_y - 15, 20 * bonus_x - 5, 20 * bonus_y - 5, fill="Red")


def setup():
    """this is setup function"""
    global game_over, score, head, direction, button_new_game, button_exit
    canv.delete(ALL)
    button_new_game.destroy()
    button_exit.destroy()
    game_over = False
    score = 0
    direction = ""
    tail.clear()
    events.clear()
    head = canv.create_oval(480, 340, 500, 360, fill="Yellow")
    draw_bonus()
    canv.create_line(20, 20, 20, 700)
    canv.create_line(20, 20, 1000, 20)
    canv.create_line(1000, 20, 1000, 700)
    canv.create_line(20, 700, 1000, 700)


def logic():
    """this is logic function which control almost everything in this game: if snake eat bonus draw new one,
    draw new part of the tail, make each  part of the tail moving right direction"""
    global head, bonus_x, bonus_y, bonus, score, tail, direction, new_tail_x, new_tail_y, game_over
    coordinates = canv.coords(head)
    if coordinates[2] == 20 * bonus_x and coordinates[3] == 20 * bonus_y:  # If snake eat bonus
        score += 1
        new_tail_x = bonus_x
        new_tail_y = bonus_y
        tail.append(["", direction])  # Make code knowing that it should draw a new part of the tail
        canv.delete(bonus)
        draw_bonus()
    # We will draw new part of the tail in the place where snake head eat bonus and when all snake pass this place
    if len(tail) != 0:  # To prevent error: "list index out of range"
        number_to_draw = 0
        for i in range(len(tail)):
            if tail[i][0] == "":
                number_to_draw = i
                break
        if tail[number_to_draw][0] == "" and (coordinates[2] != 20 * new_tail_x or coordinates[3] != 20 * new_tail_y):
            draw_tail = True
            for i in range(number_to_draw):
                if tail[i][0] != "":
                    coord = canv.coords(tail[i][0])
                    if coord[2] == 20 * new_tail_x and coord[3] == 20 * new_tail_y:
                        draw_tail = False
            if draw_tail:
                tail[number_to_draw][0] = \
                    canv.create_rectangle(20 * new_tail_x - 20, 20 * new_tail_y - 20, 20 * new_tail_x,
                                          20 * new_tail_y)  # Draw new part of the tail
    # Each part of the snake should move to the position of the previous part
    for i in range(len(tail) - 1, 0, -1):
        tail[i][1] = tail[i - 1][1]  # Give direction from previous part of the tail to next part
    if len(tail) != 0:
        tail[0][1] = direction  # Give direction from head of the snake to the first part of the tail
    # If snake head collide with the part of the tail - game over
    for i in range(len(tail)):
        if tail[i][0] != "":  # To prevent error: "list index out of range"
            if coordinates[2] == canv.coords(tail[i][0])[2] and coordinates[3] == canv.coords(tail[i][0])[3]:
                game_over = True
    if coordinates[2] == 20 or coordinates[2] == 1020 or coordinates[3] == 20 or coordinates[3] == 720:
        game_over = True


def moving():
    """this function move all snake (head and tail)"""
    global direction, head, tail
    if direction == "up":
        canv.move(head, 0, -20)  # Move up
    if direction == "down":
        canv.move(head, 0, 20)  # Move down
    if direction == "left":
        canv.move(head, -20, 0)  # Move left
    if direction == "right":
        canv.move(head, 20, 0)  # Move right
    for i in range(len(tail)):
        if tail[i][1] == "up" and tail[i][0] != "":
            canv.move(tail[i][0], 0, -20)  # Move part of the tail up
        if tail[i][1] == "down" and tail[i][0] != "":
            canv.move(tail[i][0], 0, 20)  # Move part of the tail down
        if tail[i][1] == "left" and tail[i][0] != "":
            canv.move(tail[i][0], -20, 0)  # Move part of the tail left
        if tail[i][1] == "right" and tail[i][0] != "":
            canv.move(tail[i][0], 20, 0)  # Move part of the tail right


def interpretate_events():
    """This function interpretate first event in queue and then clean all list of the events"""
    global direction, Pause, events
    if len(events) != 0:
        if events[0].keycode == 38 and direction != "down":
            direction = "up"
        if events[0].keycode == 40 and direction != "up":
            direction = "down"
        if events[0].keycode == 37 and direction != "right":
            direction = "left"
        if events[0].keycode == 39 and direction != "left":
            direction = "right"
        if events[0].keycode == 32:  # Put the game on pause if you push space button
            if Pause:
                Pause = False
            else:
                Pause = True
        events.clear()


def game():
    """main function of the game, is called every 50 ms"""
    global Pause, score, text, file, velocity
    interpretate_events()
    if not Pause:
        moving()
        logic()
        canv.delete(text)
        text = canv.create_text(950, 50, text="Score: " + str(score), font="Arial 14")
    if not game_over:
        root.after(velocity, game)
    else:
        canv.create_text(500, 350, text="Game over!\nYour score: " + str(score), justify=CENTER, font="Arial 30")
        file.writelines("Player " + gamer_name + " has scored " + str(score) + "\n")
        # TODO: записывать в лидербоард максимальное значение для каждого игрока (разобраться в работе с txt файлами в
        #  питоне)
        file.flush()
        main_menu()


def get_gamer_name():
    global gamer_name, enter_name, label, button_enter
    gamer_name = enter_name.get()
    enter_name.destroy()
    button_enter.destroy()
    label.destroy()
    new_game()


def get_velocity():
    global label, button_enter, enter_velocity, velocity
    velocity = int(50 / ((float(enter_velocity.get()) + 0.01)/100))
    if velocity < 50:
        velocity = 50
    enter_velocity.destroy()
    button_enter.destroy()
    label.destroy()
    new_game()


def new_game():
    """function which start new game and control gamer nickname and game speed"""
    global gamer_name, enter_name, label, button_enter, velocity, enter_velocity
    if velocity != 0:
        if gamer_name != "":
            setup()
            game()
        else:
            label = Label(canv, text="Enter your nickname:", font="Arial 26")
            label.pack()
            enter_name = Entry(canv, width=100)
            enter_name.pack()
            button_enter = Button(canv, text="Enter", width=15, height=3, command=get_gamer_name)
            button_enter.pack()
    else:
        label = Label(canv, text="Enter velocity of the snake in percents\n(100% - max speed, 90% - less speed etc.):"
                      , font="Arial 26")
        label.pack()
        enter_velocity = Entry(canv, width=100)
        enter_velocity.pack()
        button_enter = Button(canv, text="Enter", width=15, height=3, command=get_velocity)
        button_enter.pack()


# Interpretate key press

def key_interpretator(event):
    """this function interpretate pushing keys"""
    global direction, Pause, events
    events.append(event)


root.bind("<KeyPress>", key_interpretator)


# canv.bind("<Button-1>", pause)


# Make main menu
def Exit():
    sys.exit()


def main_menu():
    """This is function for main menu which produce 2 buttons: exit and new_game and
    interpretate clicks on this buttons"""
    global button_new_game, button_exit, velocity
    velocity = 0
    button_new_game = Button(canv, text="New game", width=15, height=3, command=new_game)
    button_new_game.pack()
    button_exit = Button(canv, text="Exit", width=15, height=3, command=Exit)
    button_exit.pack()


main_menu()

mainloop()
