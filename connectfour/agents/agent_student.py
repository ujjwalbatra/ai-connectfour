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

        if depth == self.MaxDepth or board.winner() != 0:
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

        winner = board.winner()

        if winner != 0:
            if winner != self.id:
                return -500
            elif winner == self.id:
                return 500

        student_agent_utility = 0
        nemesis_utility = 0
        nemesis_id = 1 if (self.id == 2) else 2

        for i in range(6):
            for col in range(7):
                row = 5 - i
                if board.get_cell_value(row, col) == self.id:
                    student_agent_utility += self.__get_horizontal_utility(board, row, col, self.id) \
                                             + self.__get_vertical_utility(board, row, col, self.id) \
                                             + self.__get_diagonal_utility(board, row, col, self.id)
                elif board.get_cell_value(row, col) == nemesis_id:
                    nemesis_utility += self.__get_horizontal_utility(board, row, col, nemesis_id) \
                                       + self.__get_vertical_utility(board, row, col, nemesis_id) \
                                       + self.__get_diagonal_utility(board, row, col, nemesis_id)

        return student_agent_utility - nemesis_utility

    def __get_horizontal_utility(self, board, row, col, id):
        """
        Calculates horizontal utility(east and west both directions and all permutations) 
        of a given coordinate on the board.
              
        Args:
            board: An instance of `Board` that is the current state of the board.
            row: row (y coordinate) of the point in board to check utility for
            col: col (x coordinate) of the point in board to check utility for
            id: id of the player to calculate utility for

        Returns:
            int: utility of the coordinate 

        """
        start = col
        end = col

        # move start towards left
        while start > 0 and start > col - 4:
            previous_horizontal_dot = board.get_cell_value(row, start - 1)
            if previous_horizontal_dot == 0 or previous_horizontal_dot == id:
                start -= 1
            else:
                break

        # move end towards right
        while end < board.DEFAULT_WIDTH - 1 and end < col + 4:
            next_horizontal_dot = board.get_cell_value(row, end + 1)
            if next_horizontal_dot == 0 or next_horizontal_dot == id:
                end += 1
            else:
                break

        if (end - start) < 3:
            return 0
        else:
            return (end - start) - 2

    def __get_vertical_utility(self, board, row, col, id):
        """
        Calculates vertical utility(north and south both directions and all permutations) 
        of a given coordinate on the board.
        
        Args:
            board: An instance of `Board` that is the current state of the board.
            row: row (y coordinate) of the point in board to check utility for
            col: col (x coordinate) of the point in board to check utility for
            id: id of the player to calculate utility for

        Returns:
            int: utility of the coordinate

        """
        start = row
        end = row

        # move start towards bottom
        while start < board.DEFAULT_HEIGHT - 1 and start < row + 4:
            next_vertical_dot = board.get_cell_value(start + 1, col)
            if next_vertical_dot == 0 or next_vertical_dot == id:
                start += 1
            else:
                break

        # move end towards top
        while end > 0 and end > row - 4:
            previous_vertical_dot = board.get_cell_value(end - 1, col)
            if previous_vertical_dot == 0 or previous_vertical_dot == id:
                end -= 1
            else:
                break

        if (start - end) < 3:
            return 0
        else:
            return (start - end) - 2

    def __get_diagonal_utility(self, board, row, col, id):
        """
        Gets utility of each diagonal and returns returns the sum of utilities.

        Args:
            board: An instance of `Board` that is the current state of the board.
            row: row (y coordinate) of the point in board to check utility for
            col: col (x coordinate) of the point in board to check utility for
            id: id of the player to calculate utility for

        Returns:
            int: utility of the coordinate for both diagonals
        """
        return self.__get_primary_diagonal_utility(board, row, col, id) + \
            self.__get_non_primary_diagonal_utility(board, row, col, id)

    def __get_primary_diagonal_utility(self, board, row, col, id):
        """
        Calculates primary diagonal(top left to bottom right on board)
        utility(north-west and south-east both directions and all permutations)
        of a given coordinate on the board.

        Args:
            board: An instance of `Board` that is the current state of the board.
            row: row (y coordinate) of the point in board to check utility for
            col: col (x coordinate) of the point in board to check utility for
            id: id of the player to calculate utility for

        Returns:
            int: utility of the coordinate
        """
        start = [row, col]
        end = [row, col]

        # move start towards top left corner
        while start[0] > 0 and start[1] > 0 \
                and start[0] > row - 4 and start[1] > col - 4:
            previous_diagonal_dot = board.get_cell_value(start[0] - 1, start[1] - 1)
            if previous_diagonal_dot == 0 or previous_diagonal_dot == id:
                start[0] -= 1
                start[1] -= 1
            else:
                break

        # move end towards bottom right corner
        while (end[0] < board.DEFAULT_HEIGHT - 1) and (end[1] < board.DEFAULT_WIDTH - 1) \
                and (end[0] < row + 4) and (end[1] < col + 4):
            next_diagonal_dot = board.get_cell_value(end[0] + 1, end[1] + 1)
            if next_diagonal_dot == 0 or next_diagonal_dot == id:
                end[0] += 1
                end[1] += 1
            else:
                break

        if (end[0] - start[0]) < 3:
            return 0
        else:
            return (end[0] - start[0]) - 2

    def __get_non_primary_diagonal_utility(self, board, row, col, id):
        """
        Calculates non primary diagonal(bottom left to top right on board)
        utility(south-west and north-east directions and all permutations)
        of a given coordinate on the board.

        Args:
            board: An instance of `Board` that is the current state of the board.
            row: row (y coordinate) of the point in board to check utility for
            col: col (x coordinate) of the point in board to check utility for
            id: id of the player to calculate utility for

        Returns:
            int: utility of the coordinate
        """
        start = [row, col]
        end = [row, col]

        # move start towards bottom left corner
        while (start[0] < board.DEFAULT_HEIGHT - 1) and (start[1] > 0) \
                and (start[0] < row + 4) and (start[1] > col - 4):
            previous_diagonal_dot = board.get_cell_value(start[0] + 1, start[1] - 1)
            if previous_diagonal_dot == 0 or previous_diagonal_dot == id:
                start[0] += 1
                start[1] -= 1
            else:
                break

        # move end towards top right corner
        while (end[0] > 0) and (end[1] < board.DEFAULT_WIDTH - 1) \
                and (end[0] > row - 4) and (end[1] < col + 4):
            next_diagonal_dot = board.get_cell_value(end[0] - 1, end[1] + 1)
            if next_diagonal_dot == 0 or next_diagonal_dot == id:
                end[0] -= 1
                end[1] += 1
            else:
                break

        if (end[1] - start[1]) < 3:
            return 0
        else:
            return (end[1] - start[1]) - 2
