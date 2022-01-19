 Build an Adversarial Game Playing Agent

![Example game of isolation on a square board](viz.gif)
## Synopsis

In this project, I used adversarial search techniques to build an agent to play knights Isolation.
### Isolation

In the game Isolation, two players each control their own single token and alternate taking turns moving the token from one cell to another on a rectangular grid.  Whenever a token occupies a cell, that cell becomes blocked for the remainder of the game.  An open cell available for a token to move into is called a "liberty".  The first player with no remaining liberties for their token loses the game, and their opponent is declared the winner.

In knights Isolation, tokens can move to any open cell that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board.  On a blank board, this means that tokens have at most eight liberties surrounding their current location.  Token movement is blocked at the edges of the board (the board does not wrap around the edges), however, tokens can "jump" blocked or occupied spaces (just like a knight in chess).

Finally, agents have a fixed time limit (150 milliseconds by default) to search for the best move and respond.  The search will be automatically cut off after the time limit expires, and the active agent will forfeit the game if it has not chosen a move.
## Structure
First, I implemented a basic agent combining minimax search with alpha-beta pruning and iterative deepening.
Then I experimented various techniques to improve the efficiency of the alpha-beta pruning technique.<br/>
1- I added a Transposition Table <br>
2- Updated the Transposition table with PV-Nodes and Beta-Cut-Off Nodes <br>
3- Implemented Killer heuristic Technique <br>
4- Performed Move ordering.
## Agent
The agent is implemented in the `my_custom_player.py` file, within the `get_action` function using alpha-beta pruning with iterative deepening, 
this function is called once per turn for each player. The calling function handles the time limit
## Evaluation
The evaluation function is implemented in the `my_custom_player.py` file, within the `my_moves` function.
## Move Ordering    <br>    
The function responsible for the scoring the moves is `score_moves`, it gives each move its own sort score,
the sorting is done as follows : a) The transposition table moves come first, which are the following :-
<br> 
1- PV-Nodes : if the current move is a PV-Node in the transposition table.

2- Beta-Cut-Off Nodes :  if the current move is a Beta-Cut-Off Node in the transposition table.
<br>

b) After that, the two killer moves.

The move ordering is process is done using Selection-Sort in the `min_value`  `max_values` functions.
## Running the code to test the agent
You can run matches to test the performance of the efficient implemented agent against sample opponents.
Example Usage:
--------------
            - Run 40 games (10 rounds = 20 games x2 for fair matches = 40 games) against
              the greedy agent with 4 parallel processes: 

                $python run_match.py -f -r 10 -o GREEDY -p 4

            - Run 100 rounds (100 rounds = 200 games) against the minimax agent with 1 process:

                $python run_match.py -r 100



