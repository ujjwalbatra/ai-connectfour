from connectfour.agents.computer_player import RandomAgent
import random


class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 6

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append(move)
            vals.append(self.dfMiniMax(next_state, float("-inf"), float("+inf"), 1))

        bestMove = moves[vals.index(max(vals))]

        return bestMove

    def dfMiniMax(self, board, alpha, beta, depth):
        # Goal return column with maximized scores of all possible next states

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        moves = []

        if depth % 2 == 1:
            bestVal = float("inf")
            valid_moves = board.valid_moves()
            for move in valid_moves:
                next_state = board.next_state(self.id % 2 + 1, move[1])
                moves.append(move)
                bestVal = min(bestVal, self.dfMiniMax(next_state, alpha, beta, depth + 1))
                beta = min(beta, bestVal)
                if beta <= alpha:
                    break
            return bestVal

        else:
            bestVal = float("-inf")
            valid_moves = board.valid_moves()
            for move in valid_moves:
                next_state = board.next_state(self.id, move[1])
                moves.append(move)
                bestVal = max(bestVal, self.dfMiniMax(next_state, alpha, beta, depth + 1))
                alpha = max(alpha, bestVal)
                if beta <= alpha:
                    break

            return bestVal

    def evaluateBoardState(self, board):
        """
        Your evaluation function should look at the current state and return a score for it.
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """

        if board.winner() == 1:
            return -1000
        elif board.winner() == 2:
            return 1000

        map_ = [[3, 4, 5, 7, 5, 4, 3],
                [4, 6, 8, 10, 8, 6, 4],
                [5, 8, 11, 13, 11, 8, 5],
                [5, 8, 11, 13, 11, 8, 5],
                [4, 6, 8, 10, 8, 6, 4],
                [3, 4, 5, 7, 5, 4, 3]
                ]

        student_agent_utility = 0
        nemesis_utility = 0

        for i in range(6):
            for col in range(7):
                row = 5 - i
                if board.get_cell_value(row, col) == 2:
                    student_agent_utility += map_[row][col]
                elif board.get_cell_value(row, col) == 1:
                    nemesis_utility -= map_[row][col]

        return student_agent_utility - nemesis_utility
