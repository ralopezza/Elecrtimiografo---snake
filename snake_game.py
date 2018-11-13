# Simple Snake Game in Python 3 for Beginners
# By @TokyoEdTech

import turtle
import time
import random
import board
import busio
import math

from adafruit_ads1x15.single_ended import ADS1115

def millis():
    return time.time()*1000

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
adc = ADS1115(i2c)
deltaT = 0
time2 = millis()

N = 0
sum = 0
RMS = 0
i=0

delay = 0.05 #Controla la velocidad de la "culebra"

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game by @TokyoEdTech")
wn.bgcolor("green")
wn.setup(width=800, height=600)
wn.tracer(0) # Turns off the screen updates

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
  #  print(head.direction)
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
time2 = millis()
time3 = millis()
time4=millis()
deltaT2 = 0
mover = 0
mover2 = 0
NN = 0
# Main game loop
while True:
    wn.update()
    time1 = millis()
    time3 = millis()
    deltaT = time1 - time2
    deltaT2 = time3 - time4
    v0 = adc[0].volts
    v1 = adc[1].volts
    #rint(deltaT2)
    if deltaT2 > 100:
        if NN == 0 and mover2 == 1:
            RMS = 0
        elif N!= 0: 
            RMS = math.sqrt(sum/N)
        else:
            RMS = 0
        if RMS > 0.5:
            
            mover = 1
        mover2 = mover 
            #print(mover2)
        NN += 1
        print(RMS)
        time4 = millis()
        N = 0
        sum=0
    else:
        sum = sum + (v0-2.3)*(v0-2.3)
        N = N + 1
    
    if deltaT > 500:
        time2 = millis()
        NN  = 0
        #print("Sumatoria={:>5.3f}\tN={:>3d}\tRMS={:>5.3f}" .format(sum,N,RMS))
        

                
                #print(i)
    # Check for a collision with the border
        if head.xcor()>390 or head.xcor()<-390 or head.ycor()>290 or head.ycor()<-290:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"

        # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)
        
        # Clear the segments list
            segments.clear()

        # Reset the score
            score = 0

        # Reset the delay
            delay = 0.1

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 


    # Check for a collision with the food
        if head.distance(food) < 20:
        # Move the food to a random spot
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            food.goto(x,y)

        # Add a segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)

        # Shorten the delay
            delay -= 0.001

        # Increase the score
            score += 10

            if score > high_score:
                high_score = score
        
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

    # Move the end segments first in reverse order
        for index in range(len(segments)-1, 0, -1):
            x = segments[index-1].xcor()
            y = segments[index-1].ycor()
            segments[index].goto(x, y)

    # Move segment 0 to where the head is
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x,y)
        #print(mover)
        if mover == 1:
            print("chiunga tu madre")
            i+=1
            if head.direction == "down":
                go_left()
            elif head.direction == "left":
                go_up()
            elif head.direction == "up":
                go_right()
            elif head.direction == "right":
                go_down()
        
        move()    
        mover = 0
    # Check for head collision with the body segments
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.goto(0,0)
                head.direction = "stop"
            
            # Hide the segments
                for segment in segments:
                    segment.goto(1000, 1000)
        
            # Clear the segments list
                segments.clear()

            # Reset the score
                score = 0

            # Reset the delay
               #delay = 0.1
        
            # Update the score display
                pen.clear()
                pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
    
   


wn.mainloop()