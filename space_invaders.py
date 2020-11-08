#Space Invaders
#python 2.7.12 on Mac
# Thanks to Christian Thompson 
# Python Game Programming Tutorial: Space Invaders
# http://christianthompson.com/

import turtle
import os
import math
import random
import winsound
#Set up the 
# screen

win = turtle.Screen()
win.bgcolor("black")
win.title("Space Invaders")
win.bgpic("space_invaders_background.gif")

#Register the graphics for the game
turtle.register_shape("invader.gif")
turtle.register_shape("red_invader.gif")
turtle.register_shape("player.gif")

#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pensize(3)
border_pen.pendown()
for side in range(4):
  border_pen.fd(600)
  border_pen.lt(90)
border_pen.hideturtle()

#Set the score to 0
score = 100

#Draw the score on stage
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,280)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font = ("Arial", 14, "bold"))
score_pen.hideturtle()

#Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.speed(0)
player.penup()
player.setposition(0, -250)
player.setheading(90)

playerspeed = 15

#Choose number of enemies
number_of_enemies = 4

#Create an empty list of enemies
enemiesList = []

#Add enemies to the list
#We need to create more turtle objects

for i in range(number_of_enemies):
  #Create the enemy
  enemiesList.append(turtle.Turtle())

for enemy in enemiesList:
  enemy.color("red")
  enemy.shape("invader.gif")
  enemy.speed(random.randint(1,3))
  enemy.penup()
  x = random.randint(-200, 200)
  y = random.randint(100, 200)
  enemy.setposition(x, y)

enemyspeed = 2

#Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.speed(0)
bullet.penup()
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 20

#Define bullet state
#we have 2 states:
#ready - ready to fire bullet
#fire - bullet is firing

bulletstate = "ready"



#spawn new invader
def spawn_invader():
  enemy = turtle.Turtle()
  enemy.color("red")
  enemy.shape("red_invader.gif")
  enemy.speed(random.randint(1,3))
  enemy.penup()
  x = random.randint(-200, 200)
  y = random.randint(100, 200)
  enemy.setposition(x, y)
  enemiesList.append(enemy)

#Move the player left and right

def move_left():
  x = player.xcor()
  x = x - playerspeed
  if x < -280:
    x = -280
  player.setx(x)

def move_right():
  x = player.xcor()
  x = x + playerspeed
  if x > 280:
    x = 280
  player.setx(x)

def fire_bullet():
  #Declare bulletstate as a global if it needs change
  global bulletstate,score
  if bulletstate == "ready":
    os.system("afplay laser.wav&")
    winsound.PlaySound("laser.wav",winsound.SND_ASYNC)
    #for linux use os.system("aplay laser.wav&")
    #Move the bullet to just above the player
    score=score -1
    scorestring = "Score: %s" %score
    score_pen.clear()
    score_pen.write(scorestring, False, align="left", font = ("Arial", 14, "bold"))
    x = player.xcor()
    y = player.ycor() + 10
    bullet.setposition(x,y)
    bullet.showturtle()
    bulletstate = "fire"


def isCollision(t1,t2):
  distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(),2))
  if distance < 15:
    return True
  else:
    return False



#create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")


#Main game loop
while True:
  if len(enemiesList) < 1:
    player.hideturtle()
    print("YOU WON")
    break
  
  for enemy in enemiesList:
    #This is a forever loop
    #Move the enemy
    x = enemy.xcor()

    if enemy.heading() == 0:
      x = x + enemy.speed()
    elif enemy.heading() == 180:
      x = x - enemy.speed()

    enemy.setx(x)

    #Move enemy back and down
    if enemy.xcor() > 280:
      enemy.setheading(180)
      y = enemy.ycor()
      y = y - 40
      enemy.sety(y)
    if enemy.xcor() < -280:
      enemy.setheading(0)
      y = enemy.ycor()
      y = y - 40
      enemy.sety(y)

    #Check for collision between bullet and enemy
    if isCollision(bullet, enemy):
      os.system("afplay explosion.wav&")
      #for linux use os.system("aplay explosion.wav&") 
      #Reset the bullet
      bullet.hideturtle()
      bulletstate = "ready"
      bullet.setposition(0, -400)
      #Reset the enemy
      x = random.randint(-200, 200)
      y = random.randint(100, 200)
      enemy.setposition(x, y)

      #Update scores & spawn invaders when green invader is hit
      if (enemy.shape() == "invader.gif"):
        score += 10
        spawn_invader()
        spawn_invader()
      else:
        score += 20

      enemy.hideturtle()
      enemiesList.remove(enemy)

      scorestring = "Score: %s" %score
      score_pen.clear()
      score_pen.write(scorestring, False, align="left", font = ("Arial", 14, "bold"))

    #Check for collision between enemy and player
    if isCollision(player, enemy):
      #os.system("afplay explosion.wav&")
      #for linux use os.system("aplay explosion.wav&") 
      player.hideturtle()
      enemy.hideturtle()
      print("GAME OVER")
      break

  #Move the bullet only when bulletstate is "fire"
  if bulletstate == "fire":
    y = bullet.ycor()
    y = y + bulletspeed
    bullet.sety(y)

  #Check to see if bullet has reached the top
  if bullet.ycor() > 275:
    bullet.hideturtle()
    bulletstate = "ready"


#delay = raw_input("Press enter to finish")
#win.mainloop()