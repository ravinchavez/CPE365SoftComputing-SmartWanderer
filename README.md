## PySimbot

PySimbot is a software for simple robot simulation

## Caption
Group Pocky | SSW

We used behavior-based control to balance reward-avoidance; maximizing food capture without planning.

PROCESS 

We set three states in the code. "HIT" means the robot will back off upon max(self.ir_values), which means it comes into contact with the sensor. "SEARCHING" means the robot will react depending on the food distance and wall proximity. "CHASING" means path is clear; the robot will commit to a direction, and the robot will sprint towards the food. "AVOIDANCE" are strict behaviors wherein obstacles are detected by smell proximity and hence backtracking or turning will occur to avoid collission.

LIMITATIONS

Since the robot is purely reactive, it struggles with planning.For example, if an item is behind the wall or across a section, it might struggle to react since there is no prediction element in the algorithm. At that point, the robot will get completely stuck. 

PS: The 5-second delay before the Kivy App instantiates are setup to open the logs during filming.

## Video

## Documentation

See this [Wiki](https://github.com/jetstreamc/PySimbot/wiki/)

## Copyleft license

This software is under the GPL-GNU License as declared in [LICENSE](/LICENSE) file.