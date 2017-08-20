# Implementation of classic arcade game Pong

import simplegui
import random

# Globals

"""Frame"""
WIDTH = 600
HEIGHT = 400

"""Paddles"""
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

paddle1_vel = 0
paddle2_vel = 0
paddle_general_vel = 4
paddle1_pos = [HALF_PAD_WIDTH, 200]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, 200]

"""Ball"""
BALL_RADIUS = 20
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
LEFT = False
RIGHT = True

"""Scores"""
begin_game = True
score1 = 0
score2 = 0

# Helper Functions

def spawn_ball(direction):
    """This function starts a new game, puts the ball in its default
    position and velocity, and decides to which side to throw the ball"""
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 140) / 60.0
        ball_vel[1] = - (random.randrange(60, 180) / 60.0)
    elif direction == LEFT:
        ball_vel[0] = - (random.randrange(120, 140) / 60.0)
        ball_vel[1] = - (random.randrange(60, 180) / 60.0)
    
    
# Event handlers

def first_game():
    """This button starts the first game and calls the spawn_ball() function"""
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  
    global score1, score2, begin_game
    if begin_game == True:
        score1 = 0
        score2 = 0
        first_ball = random.choice([LEFT, RIGHT])
        spawn_ball(first_ball)
        begin_game = False
    elif begin_game == False:
        return None

def new_game():
    """This button resets the scores and calls the spawn_ball() function"""
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  
    global score1, score2
    score1 = 0
    score2 = 0
    first_ball = random.choice([LEFT, RIGHT])
    spawn_ball(first_ball)  
               
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel, paddle_general_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if paddle1_pos[1] - 42 <= ball_pos[1] <= paddle1_pos[1] + 42:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += (ball_vel[0] * 0.1)
        else:
            spawn_ball(RIGHT)
            score1 += 1
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        if paddle2_pos[1] - 42 <= ball_pos[1] <= paddle2_pos[1] + 42:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += (ball_vel[0] * 0.1)
        else:
            spawn_ball(LEFT)
            score2 += 1
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
            
    # draw scores
    canvas.draw_text(str(score2), [135, 100], 60, "White")
    canvas.draw_text(str(score1), [425, 100], 60, "White")
    
    # draw ball and move it
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # update paddle's vertical position, keep paddle on the screen
    if 40 < paddle1_pos[1] + paddle1_vel < 360:
        paddle1_pos[1] += paddle1_vel
    else:
        paddle1_vel = 0
    if 40 < paddle2_pos[1] + paddle2_vel < 360:
        paddle2_pos[1] += paddle2_vel
    else:
        paddle2_vel = 0
    
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos[1] - 40], [8, paddle1_pos[1] - 40], [8, paddle1_pos[1] + 40], [0, paddle1_pos[1] + 40]], 1, "White", "White")
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos[1] - 40], [WIDTH, paddle2_pos[1] - 40], [WIDTH, paddle2_pos[1] + 40], [WIDTH - PAD_WIDTH, paddle2_pos[1] + 40]], 1, "White", "White") 
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle_general_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= paddle_general_vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += paddle_general_vel
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= paddle_general_vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += paddle_general_vel
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    

# Create frame

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Start Game", first_game, 100)
frame.add_button("Play Again!", new_game, 100)


# start frame

frame.start()
