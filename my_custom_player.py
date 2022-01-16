
from sample_players import DataPlayer


class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    from collections import defaultdict, Counter
    transpose_table = defaultdict(list)
    killer_moves = defaultdict(list)
    move_ordering = defaultdict(Counter)
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE:
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """

        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        #import random
        #self.queue.put(random.choice(state.actions()))
        current_depth = 1
        best_move = None
        while current_depth <= 3:
            best_move = self.minimax_decision(state, current_depth, self.transpose_table, self.killer_moves)
            print(best_move)
            current_depth += 1
        self.queue.put(best_move)

    #Evaluation Function
    def my_moves(self, gameState):
        loc = gameState.locs[self.player_id]
        return len(gameState.liberties(loc))
    # prepare for move ordering
    # the transposition table score for moves first
    # the two killer moves per ply
    def minimax_decision(self,gameState,current_depth, transpose_table, killer_moves):
        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        # FROM left to right
        for a in gameState.actions():
            v = self.min_value(gameState.result(a), alpha, beta, current_depth-1, transpose_table, killer_moves)
            alpha = max(v, alpha)
            if v > best_score:
                best_score = v
                best_move = a
        return best_move

    # def min_value(self, gameState, alpha, beta, depth, transpose_table, killer_moves):
    #     """ Return the value for a win (+1) if the game is over,
    #     otherwise return the minimum value over all legal child
    #     nodes.
    #     """
    #     if gameState.terminal_test():
    #         return gameState.utility(0)
    #     if depth <= 0:
    #         return self.my_moves(gameState)
    #
    #     v = float("inf")
    #     for a in gameState.actions():
    #         v = min(v, self.max_value(gameState.result(a), alpha, beta, depth-1, transpose_table, killer_moves))
    #         if v <= alpha:
    #             return v
    #         beta = min(beta, v)
    #     return v
    # def min_value22(self, gameState, alpha, beta, depth, transpose_table, killer_moves, ply):
    #     """"""
    #     if gameState.terminal_test():
    #         return gameState.utility(0)
    #     if depth <= 0:
    #         return self.my_moves(gameState)
    #
    #     v = float("inf")
    #
    #     if len(transpose_table[gameState]) == 0:
    #         transpose_table[gameState] = [0]*5
    #         legal_moves = gameState.actions()
    #         for a in gameState.actions():
    #             v = min(v, self.max_value(gameState.result(a), alpha, beta, depth - 1, transpose_table, killer_moves, ply + 1))
    #             if alpha >= v:
    #                 transpose_table[gameState][3] = "cut_node"
    #                 if len(killer_moves[depth]) < 2:
    #                     killer_moves[depth].append(a)
    #                 break
    #             elif v > alpha and v < beta:
    #                 #print("PV")
    #                 transpose_table[gameState][3] = "pv_node"
    #             else:
    #                 transpose_table[gameState][3] = "fail_node"
    #
    #             beta = min(v, beta)
    #
    #         transpose_table[gameState][0] = depth
    #         transpose_table[gameState][1] = v
    #         transpose_table[gameState][2] = a
    #
    #     else:
    #         largest_depth_so_far = transpose_table[gameState][0]
    #         if depth > largest_depth_so_far:
    #
    #             legal_moves = gameState.actions()
    #             for a in gameState.actions():
    #                 v = min(v, self.max_value(gameState.result(a), alpha, beta, depth - 1, transpose_table, killer_moves, ply + 1))
    #                 if alpha >= v:
    #                     transpose_table[gameState][3] = "cut_node"
    #                     if len(killer_moves[depth]) < 2:
    #                         killer_moves[depth].append(a)
    #                     break
    #                 elif v > alpha and v < beta:
    #                     transpose_table[gameState][3] = "pv_node"
    #                 else:
    #                     transpose_table[gameState][3] = "fail_node"
    #                 beta = min(v, beta)
    #
    #
    #             transpose_table[gameState][0] = depth
    #             transpose_table[gameState][1] = v
    #             transpose_table[gameState][2] = a
    #         else:
    #
    #             v = transpose_table[gameState][1]
    #     return v

    def min_value(self, gameState, alpha, beta, depth, transpose_table, killer_moves):
            """"""
            if gameState.terminal_test():
                return gameState.utility(0)
            if depth <= 0:
                return self.my_moves(gameState)

            v = float("inf")

            if len(transpose_table[gameState]) == 0:
                score_moves = self.score_moves(gameState.actions(), transpose_table, killer_moves, depth, gameState)
                transpose_table[gameState] = [0] * 5
                legal_moves = gameState.actions()
                for i in range(0, len(legal_moves)):
                    best_idX = i
                    for j in range(i + 1, len(legal_moves)):
                        if score_moves[legal_moves[best_idX]] <= score_moves[legal_moves[j]]:
                            best_idX = j
                    temp = legal_moves[i]
                    legal_moves[i] = legal_moves[best_idX]
                    legal_moves[best_idX] = temp
                    #legal_moves[i], legal_moves[best_idX] = legal_moves[best_idX], legal_moves[i]
                    v = min(v, self.max_value(gameState.result(legal_moves[i]), alpha, beta, depth - 1, transpose_table,
                                              killer_moves))
                    if alpha >= v:
                        transpose_table[gameState][0] = depth
                        transpose_table[gameState][1] = v
                        transpose_table[gameState][2] = legal_moves[i]
                        transpose_table[gameState][3] = "alpha_cut"
                        return v
                    elif v > alpha and v < beta:
                        transpose_table[gameState][3] = "pv_node"
                    else:
                        transpose_table[gameState][3] = "fail_node"
                    beta = min(v, beta)
                transpose_table[gameState][0] = depth
                transpose_table[gameState][1] = v
                transpose_table[gameState][2] = legal_moves[i]

            else:
                #Assigned scores to our legal moves
                score_moves = self.score_moves(gameState.actions(), transpose_table, killer_moves, depth, gameState)

                largest_depth_so_far = transpose_table[gameState][0]

                if depth >= largest_depth_so_far:
                    legal_moves = gameState.actions()
                    for i in range(0, len(legal_moves)):
                        best_idX = i
                        for j in range(i+1, len(legal_moves)):
                            if score_moves[legal_moves[best_idX]] < score_moves[legal_moves[j]]:
                                best_idX = j
                        temp = legal_moves[i]
                        legal_moves[i] = legal_moves[best_idX]
                        legal_moves[best_idX] = temp
                        v = min(v, self.max_value(gameState.result(legal_moves[i]), alpha, beta, depth - 1, transpose_table, killer_moves
                                                ))
                        if alpha >= v:
                            transpose_table[gameState][0] = depth
                            transpose_table[gameState][1] = v
                            transpose_table[gameState][2] = legal_moves[i]
                            transpose_table[gameState][3] = "alpha_cut"
                            return v
                        elif v > alpha and v < beta:
                            transpose_table[gameState][3] = "pv_node"
                        else:
                            transpose_table[gameState][3] = "fail_node"
                        beta = min(v, beta)
                    transpose_table[gameState][0] = depth
                    transpose_table[gameState][1] = v
                    transpose_table[gameState][2] = legal_moves[i]

                else:
                    v = transpose_table[gameState][1]
            return v
    # scoring legal moves
    def score_moves(self, legal_moves, transpose_table, killer_moves, current_depth, gameState):
        moves_with_scores = {}
        if len(transpose_table[gameState]) > 0:
            if transpose_table[gameState][3] == "pv_node" or transpose_table[gameState][3] == "beta_cut":
                if transpose_table[gameState][2] in legal_moves:
                    print("best movesssssssss")
                    moves_with_scores[transpose_table[gameState][2]] = 2
            else:
                #print("Worst movesssssssss")
                moves_with_scores[transpose_table[gameState][2]] = 0
        if len(killer_moves[current_depth]) != 0:
            for move in killer_moves[current_depth]:
                if move in legal_moves:
                    #print("Killer Moves")
                    moves_with_scores[move] = 1
        for a in legal_moves:
            if a not in moves_with_scores.keys():
                moves_with_scores[a] = 0
        return moves_with_scores



    # def max_value(self,gameState, alpha, beta,depth, transpose_table, killer_moves):
    #     if gameState.terminal_test():
    #         return gameState.utility(0)
    #     if depth <= 0:
    #         return self.my_moves(gameState)
    #
    #     v = float("-inf")
    #
    #     for a in gameState.actions():
    #         v = max(v, self.min_value(gameState.result(a), alpha, beta, depth - 1, transpose_table, killer_moves))
    #         if v >= beta:
    #             return v
    #         alpha = max(v, alpha)
    #         # save the value of the best move in the transposition table
    #     return v







    def max_value(self, gameState, alpha, beta, depth, transpose_table, killer_moves):
        """"""
        if gameState.terminal_test():
            #print(gameState.utility(0))
            return gameState.utility(0)
        if depth <= 0:
            return self.my_moves(gameState)

        v = float("-inf")

        if len(transpose_table[gameState]) == 0:
            score_moves = self.score_moves(gameState.actions(), transpose_table, killer_moves, depth, gameState)

            transpose_table[gameState] = [0] * 5
            legal_moves = gameState.actions()
            for i in range(0, len(legal_moves)):
                best_idX = i

                for j in range(i + 1, len(legal_moves)):
                    if score_moves[legal_moves[best_idX]] < score_moves[legal_moves[j]]:
                        best_idX = j
                temp = legal_moves[i]
                legal_moves[i] = legal_moves[best_idX]
                legal_moves[best_idX] = temp
                #legal_moves[i], legal_moves[best_idX] = legal_moves[best_idX], legal_moves[i]

                v = max(v, self.min_value(gameState.result(legal_moves[i]), alpha, beta, depth - 1, transpose_table,
                                          killer_moves
                                          ))
                #beta cut-offs
                if v >= beta:
                    transpose_table[gameState][3] = "beta_cut"
                    transpose_table[gameState][0] = depth
                    transpose_table[gameState][1] = v
                    transpose_table[gameState][2] = legal_moves[i]
                    if len(killer_moves[depth]) < 2:
                        killer_moves[depth].append(legal_moves[i])
                    return v
                elif v > alpha and v < beta:
                    transpose_table[gameState][3] = "pv_node"
                else:
                    transpose_table[gameState][3] = "fail_node"
                alpha = max(v, alpha)
            transpose_table[gameState][0] = depth
            transpose_table[gameState][1] = v
            transpose_table[gameState][2] = legal_moves[i]

        else:

            score_moves = self.score_moves(gameState.actions(), transpose_table, killer_moves, depth, gameState)

            largest_depth_so_far = transpose_table[gameState][0]

            if depth >= largest_depth_so_far:
                legal_moves = gameState.actions()
                for i in range(0, len(legal_moves)):
                    best_idX = i
                    for j in range(i+1, len(legal_moves)):
                        if score_moves[legal_moves[best_idX]] < score_moves[legal_moves[j]]:
                            best_idX = j

                    temp = legal_moves[i]
                    legal_moves[i] = legal_moves[best_idX]
                    legal_moves[best_idX] = temp
                    #legal_moves[i], legal_moves[best_idX] = legal_moves[best_idX], legal_moves[i]
                    v = max(v, self.min_value(gameState.result(legal_moves[i]), alpha, beta, depth - 1, transpose_table, killer_moves
                                          ))
                    if v >= beta:
                        transpose_table[gameState][3] = "beta_cut"
                        transpose_table[gameState][0] = depth
                        transpose_table[gameState][1] = v
                        transpose_table[gameState][2] = legal_moves[i]
                        if len(killer_moves[depth]) < 2:
                            killer_moves[depth].append(legal_moves[i])
                        return v
                    elif v > alpha and v < beta:
                        transpose_table[gameState][3] = "pv_node"
                    else:
                        transpose_table[gameState][3] = "fail_node"
                    alpha = max(v, alpha)

                transpose_table[gameState][0] = depth
                transpose_table[gameState][1] = v
                transpose_table[gameState][2] = legal_moves[i]

            else:
                v = transpose_table[gameState][1]
        return v
