To used a version of python 2.7.X to compile. To run simply:

$ python GameManager.py

This will run instance of the 2048-puzzle game played on a 4×4 grid, with numbered tiles that slide
in all four directions when a player moves them. Every turn, a new tile will randomly appear
in an empty spot on the board, with a value of either 2 or 4. Per the input direction given by
the player, all tiles on the grid slide as far as possible in that direction, until they either (1)
collide with another tile, or (2) collide with the edge of the grid. If two tiles of the same
number collide in flight, they merge into a single tile, valued at the sum of the two original
tiles that collided. 

Normally in the 2048 game you have control of which direction to move every turn but to implement
alpha-beta pruning and min-max algorithms every other turn is controlled by my PlayerAI.py
and its heuristic function. And the other turn is randomly chosen in any of the 4 possible directions.
This is controlled by ComputerAI.py. There is also an imposed .2 second time limit for the computer for each
turn to decide what direction to take in the algorithm.

Typically my AI program achieves around 512 on average, however when the restriction is removed of the
other AI randomly choosing a direction the program achieves 2048 a majority of the time. Implementing
Expecti-mini-max algorithm might be an alternative to further improve this AI, as well as adjusting the
weights in the heuristic found in getMove() in PlayerAI.py.