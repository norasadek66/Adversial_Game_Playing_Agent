 Build an Adversarial Game Playing Agent

![Example game of isolation on a square board](viz.gif)
## Synopsis

In this project, I used adversarial search techniques to build an agent to play knights Isolation.
## Structure
First, I implemented a basic agent combining minimax search with alpha-beta pruning and iterative deepening.
Then I experimented various techniques to improve the efficiency of the alpha-beta pruning technique.<br/>
1- I added a Transposition Table <br>
2- Updated the Transposition table with PV-Nodes and Cut-Off Nodes <br>
3- Implemented Killer heuristic Technique <br>
4- Performed Move ordering.