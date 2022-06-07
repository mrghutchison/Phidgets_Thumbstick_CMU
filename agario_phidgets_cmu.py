# Agario with Phidgets and CMU
# Version 1.0
# G. Hutchison
# June 7, 2022

from cmu_graphics import *
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.DigitalInput import *
import random

vertical = VoltageRatioInput()
vertical.setChannel(0)


horizontal = VoltageRatioInput()
horizontal.setChannel(1)

button = DigitalInput()

horizontal.openWaitForAttachment(1000)
vertical.openWaitForAttachment(1000)
button.openWaitForAttachment(1000)

vertical.setDataInterval(vertical.getMinDataInterval())
horizontal.setDataInterval(horizontal.getMinDataInterval())

# CMU graphics
app.background = gradient('white', 'aliceBlue')

#Size of canvas
HEIGHT = 400
WIDTH = 400

# Create a circle
dot = Circle(200, 200, 20, fill="blue")
dot.speed=5

circles = Group()
NUM_CIRCLES = 5

for _ in range(NUM_CIRCLES):
    c = Circle(random.randint(40,150),random.randint(50,350),15)
    c.speed = random.randint(1,3)
    c.xdir = random.choice((1,-1))
    c.ydir = random.choice((1,-1))
    c.radius = random.choice((12,15,25))
    circles.add(c)
    
for _ in range(NUM_CIRCLES):
    c = Circle(random.randint(260,350),random.randint(50,350),15)
    c.speed = random.randint(1,3)
    c.xdir = random.choice((1,-1))
    c.ydir = random.choice((1,-1))
    c.radius = random.choice((10,12,18,25))
    circles.add(c)
              
game_over = False
game_won = False

def onStep():
    global game_over
    global game_won
    
    if (not game_over and not game_won):
        
        v = vertical.getVoltageRatio()
        h = horizontal.getVoltageRatio()
        
        # the default joystick position will give h=0 and v=0
        # The default dot position should be (200,200)
        
        dot.centerX = ((h+1) * WIDTH)/2
        dot.centerY = ((v+1) * HEIGHT)/2
        
        # move the opponents
        for c in circles:
            c.centerX = c.centerX+(c.xdir*c.speed)
            c.centerY = c.centerY+(c.ydir*c.speed)
            
            # bounce for fun
            if c.right>WIDTH or c.left<0:
                c.xdir*=-1
                
            if c.bottom>HEIGHT or c.top<0 :
                c.ydir*=-1
                
        for c in circles:
            if (dot.hitsShape(c)):
                if dot.radius>c.radius:
                    circles.remove(c)
                    dot.radius +=1
                else:
                    # you hit an object that was too big
                    game_over = True
            
        # no more objects to consume... you must be a winner
        if (len(circles)==0):
            game_won = True
        
    if (game_over):
        dot.visible=False # Hide the player
        Label('GAME OVER', 200, 200, size=30, fill="red")
    if (game_won):
        dot.visible=False # Hide the player
        Label('WELL DONE', 200, 200, size=30, fill="green")
            
cmu_graphics.loop()