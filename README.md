# Fall20-Projects
## First Capture GO
In this project, a AI player is created using the minimax algorithm combined with move randomizer to play against a human player.
The game is played in a 5x5 grid.
It is a simple variation of the GO game, where the first player to capture opponent's stone(s) wins.
The rule fo Ko is not applicable in this game as its impossible to repeat game states


## Minimax:
The minimax algorithm is implemented to get the best moves implemented by a player. 
The minimax algorithm and the corresponding functions such as evaluate, empty_cells and game over were referred from the below link. It was modified and adapted for the first capture game that is implemented in this project
https://github.com/Cledersonbc/tic-tac-toe-minimax/tree/master/py_version

The heuristic evaluation of the score is done in the evaluate function where winning the game is awarded 3 points, losing the game costs 2 points, and a draw results in -1 points.
![alt text](https://github.com/siddharthshetty08/Fall20-Projects/blob/main/images/minimax1.PNG)
<br>
![alt text](https://github.com/siddharthshetty08/Fall20-Projects/blob/main/images/minimax2.PNG)
## Randomized Moves:
Due to the long processing time of the minimax algorithm, its not feasible to run it with the complete depth. Hence, I have combined the minimax algorithm with a randomized moves funciton, which randomly plays some more moves before evaluating the final score.

## Time complexity analysis of the Minimax Algorithm:
For every cell a move is calculated based on the current player and minimax algorithm is run again with a (depth -1) and with the opposite player's turn.
Hence the time complexity for the minimax algorithm is O(N^D) where N  is number of remaining legal moves and D is the maximum depth of the tree.

The evaluate function calls the randomized_moves function. Here the Loop runs until all the legal moves are exhausted or when the game is over. Hence, in the worst cases scenario complexity for this function is O(N) where N is the number of remaining legal moves

## Data Structure
Class
FirstCaptureGo:
* Board : List of lists representing the game state
* human : Boolean to represent the colour of human (True if black, False if white)
* bot : Boolean to represent the colour of bot (True if black, False if white)

## Game States:
![alt text](https://github.com/siddharthshetty08/Fall20-Projects/blob/main/images/game_snapshot.PNG)
<br>
![alt text](https://github.com/siddharthshetty08/Fall20-Projects/blob/main/images/game_snapshot1.PNG)
![alt text](https://github.com/siddharthshetty08/Fall20-Projects/blob/main/images/game_snapshot3.PNG)

## References:
https://github.com/Cledersonbc/tic-tac-toe-minimax/tree/master/py_version
<br>
https://www.youtube.com/watch?v=l-hh51ncgDI&t=2s&ab_channel=SebastianLague
<br>
https://www.usgo.org/sites/default/files/pdf/rules_trifold.pdf
