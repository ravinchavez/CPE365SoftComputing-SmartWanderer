#!/usr/bin/python3

import os, platform
import time
if platform.system() == "Linux" or platform.system() == "Darwin":
    os.environ["KIVY_VIDEO"] = "ffpyplayer"

from pysimbotlib.core import PySimbotApp, Robot
from kivy.config import Config

Config.set('kivy', 'log_level', 'info')

FAR_DISTANCE     = 60.0067   
SAFETY_DISTANCE  = 30.0067   
CLOSED_DISTANCE  = 10.0067   
HIT_DISTANCE     =  3.0067    

SMELL_ALIGNED    =  5.0067    
SMELL_CENTER     = 30.0067   
SMELL_HARD       = 45.0067   

class ReactiveRobot(Robot):
    def __init__(self, **kwargs):
        super(ReactiveRobot, self).__init__(**kwargs)
        self.state = "searching"

    def update(self):
        self.ir_values = self.distance()
        self.target = self.smell()

        front       = self.ir_values[0]
        front_right = self.ir_values[1]
        right       = self.ir_values[2]
        left        = self.ir_values[6]
        front_left  = self.ir_values[7]

        if min(self.ir_values) < HIT_DISTANCE:
            print("HIT - backing off.")
            self.state = "hit"
            self.move(-20)
            self.turn(60)
            return

        if self.target is None:
            print("No scent - sweeping.")
            self.state = "searching"
            self.move(8)
            self.turn(25)
            return

        smell = self.target 

        if front < SAFETY_DISTANCE:
            if left > right:
                self.state = "searching"
                print("Front near, more room left -> turn left.")
                self.turn(-60)
                self.move(8)
            else:
                self.state = "searching"
                print("Front near, more room right -> turn right.")
                self.turn(60)
                self.move(8)
            return

        if (abs(smell) <= SMELL_ALIGNED and
            front > FAR_DISTANCE and
            front_left > FAR_DISTANCE and
            front_right > FAR_DISTANCE):
            print("Food aligned, path clear -> sprint.")
            self.state = "chasing"
            self.turn(smell)
            self.move(25)
            return

        if (smell >= SMELL_HARD and
            front > FAR_DISTANCE and
            front_right > FAR_DISTANCE and
            front_left > FAR_DISTANCE):
            print("Scent hard right, path clear -> commit right.")
            self.state = "chasing"
            self.turn(35)
            self.move(16)
            return

        if (smell <= -SMELL_HARD and
            front > FAR_DISTANCE and
            front_right > FAR_DISTANCE and
            front_left > FAR_DISTANCE):
            print("Scent hard left, path clear -> commit left.")
            self.state = "chasing"
            self.turn(-35)
            self.move(16)
            return

        if front_right < SAFETY_DISTANCE and front_left > front_right:
            self.state = "avoidance"
            print("Obstacle front-right -> steer left.")
            self.turn(-45)
            self.move(10)
            return

        if front_left < SAFETY_DISTANCE and front_right > front_left:
            self.state = "avoidance"
            print("Obstacle front-left -> steer right.")
            self.turn(45)
            self.move(10)
            return
        
        if right < CLOSED_DISTANCE and left > right:
            self.state = "avoidance"
            print("Right wall near -> nudge left.")
            self.turn(-23)
            self.move(6.7)
            return

        if left < CLOSED_DISTANCE and right > left:
            self.state = "avoidance"
            print("Left wall near -> nudge right.")
            self.turn(23)
            self.move(6.7)
            return

        if (front > FAR_DISTANCE and
            front_left > FAR_DISTANCE and
            front_right > FAR_DISTANCE):
            print(f"Weak scent ({smell:.1f}) -> sweep toward it.")
            self.state = "searching"
            if smell > 0:
                self.turn(25)
            else:
                self.turn(-25)
            self.move(9)
            return

        print("Fallback - creep toward smell.")
        self.state = "searching"
        self.turn(smell)
        self.move(8)

    def path_clear_ahead(self):
        return (self.ir_values[0] > FAR_DISTANCE and
                self.ir_values[1] > FAR_DISTANCE and
                self.ir_values[7] > FAR_DISTANCE)


if __name__ == '__main__':
    app = PySimbotApp(ReactiveRobot)
    app.run()