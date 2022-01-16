 Build an Adversarial Game Playing Agent

![Example game of isolation on a square board](viz.gif)
## Synopsis

In this project, I used adversarial search techniques to build an agent to play knights Isolation.
## Structure
First, I implemented a basic agent combining minimax search with alpha-beta pruning and iterative deepening.
Then I experimented various techniques to improve the efficiency of the alpha-beta pruning technique.<br/>
1- I added a Transposition Table <br>
2- Updated the Transposition table with PV-Nodes and Beta-Cut-Off Nodes <br>
3- Implemented Killer heuristic Technique <br>
4- Performed Move ordering.
## Agent
The agent is implemented in the `my_custom_player.py` file, within the `get_action` function.
## Evaluation
The agent is implemented in the `my_custom_player.py` file, within the `my_moves` function.
## Move Ordering    <br>    
The function responsiple for the scoring the moves is `score_moves`, it gives each move its own sort score,
the sorting is done as follows : a) The transposition table move comes first
<br> 
1- PV-Nodes : if the current move is a PV-Node in the transposition table.

2- Beta-Cut-Off Nodes :  if the current move is a Beta-Cut-Off Node in the transposition table.
<br>

b) After that, the two killer moves.

The move ordering is process is done using Selection-Sort in the `min_value`  `max_values` functions.




