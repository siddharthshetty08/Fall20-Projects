#The minimax algorithm and the corresponding functions such as evaluate, empty_cells and game over were referred from the below link.
#It was modified and adapted for the first capture game that is implemented in this project
# https://github.com/Cledersonbc/tic-tac-toe-minimax/blob/master/py_version/minimax.py

from math import inf as infinity
import random
import copy

human = -1
bot = 1

class FirstCaptureGo:
    """
    Object of this class represents an instance of the game
    """
    def __init__(self,side_len, is_black):
        """
        Initializes the board, and the colours for both players
        :param side_len int: length of each side of the baord
        :param is_black boolean: True if the Human player is black, False otherwise
        """
        self.board = []
        self.visited = []
        self.prior_states = []
        for i in range(side_len):
            self.board.append([])
            self.visited.append([])
            for j in range(side_len):
                self.board[i].append(-1)
                self.visited[i].append(0)
        print_board(self.board)
        self.human = is_black
        self.bot = not is_black

def find_adjacent_cells(x, y, side_len):
    """
    Finds the legal adjacent cells for a given co-ordinate (x,y)
    :param x int: Row index
    :param y int : Column index
    :param side_len int: Length of each side of the baord
    :return:
    """
    neighbours = []
    for x_neighbour in range(x-1,x+2):
        for y_neighbour in range(y-1,y+2):
            if (-1 < x < side_len and -1 < y < side_len and (x != x_neighbour or y != y_neighbour)
                    and (0 <= x_neighbour < side_len) and (0 <= y_neighbour < side_len)) and (abs(x_neighbour-x) != abs(y_neighbour-y)):
                neighbours.append((x_neighbour,y_neighbour))
    return neighbours

def get_groups(board,is_black):
    """
    Returns a list of lists containing groups of the opponent's pieces on the board
    :param board: Current game state
    :param is_black: Colour of the player
    :return: List  consisting of groups
    """
    groups = []
    group = []
    non_visited_group_elements = set()
    # completed = []
    visited = []
    current_point = (-1,-1)
    all_occurances = []
    if is_black:
        for i in range(len(board)):
            all_occurances += [(i, j) for j, x in enumerate(board[i]) if x == 0]
    else:
        for i in range(len(board)):
            all_occurances += [(i, j) for j, x in enumerate(board[i]) if x == 1]

    while all_occurances:
        if not non_visited_group_elements:
            groups.append(group)
            group = []
            non_visited_group_elements = set()
        current_point = all_occurances.pop(0)
        if (current_point not in group) and (current_point not in visited):
            if non_visited_group_elements and current_point in non_visited_group_elements:
                group.append(current_point)
                visited.append(current_point)
                non_visited_group_elements.add(current_point)
            elif not non_visited_group_elements:
                group.append(current_point)
                visited.append(current_point)
                non_visited_group_elements.add(current_point)
            else:
                all_occurances.insert(len(all_occurances),current_point)
                continue
        neighbours = find_adjacent_cells(current_point[0],current_point[1],len(board))
        if any(neighbour in neighbours for neighbour in all_occurances):
            for neighbour in neighbours:
                if (neighbour in all_occurances) and (neighbour not in group):
                    group.append(neighbour)
                    non_visited_group_elements.add(neighbour)
                    visited.append(neighbour)
            if current_point in non_visited_group_elements:
                non_visited_group_elements.remove(current_point)
        elif any(neighbour in neighbours for neighbour in non_visited_group_elements):
            for neighbour in neighbours:
                if (neighbour in all_occurances) and (neighbour not in group):
                    group.append(neighbour)
                    non_visited_group_elements.add(neighbour)
                    visited.append(neighbour)
            if current_point in non_visited_group_elements:
                non_visited_group_elements.remove(current_point)
        else:
            if current_point in non_visited_group_elements:
                non_visited_group_elements.remove(current_point)
    groups.append(group)
    return groups[1:]


def winning_move(board: list,is_black):
    """
    Checks player wins in the current board state
    :param board list of lists: Current board state
    :param is_black Boolean:  True if the colour of the player is black, False otherwise
    :return Boolean: True if the player wins, False otherwise (Loss, draw or no result)
    """
    groups = get_groups(board,is_black)
    for group in groups:
        empty_intersection = False
        for co_ord in group:
            neighbours = find_adjacent_cells(co_ord[0],co_ord[1],len(board))
            for neighbour in neighbours:
                if board[neighbour[0]][neighbour[1]] == -1:
                    empty_intersection = True
                    break
        if not empty_intersection:
            return True
    if groups:
        if empty_intersection:
            return False
        return True
    else:
        return False


# Written to evaluate the rule of KO. Isn't required in First Capture go as the gamestates cannot be repeated in this case
# def flat_board(board: list):
#     flat_board = ""
#     for x in board:
#         for y in x:
#             flat_board += str(y)
#     return flat_board


def print_board(board):
    """
    Prints the baord
    :param board List of lists: Current board state
    :return:
    """
    for row in board:
        row = ["_" if x == -1 else x for x in row]
        row = ["B" if x == 1 else x for x in row]
        row = ["W" if x == 0 else x for x in row]
        print(row)

def smart_play(board, is_black):
    """
    Returns a list of attacking positions for the player. Not Used in this code due to performance issues, needs some tuning.
    :param board List of lists: Current board states
    :param is_black Boolean: True if the colour of the player is black, False otherwise
    :return:
    """
    groups = get_groups(board, not is_black)
    possible_attack = []
    for group in groups:
        for co_ord in group:
            neighbours = find_adjacent_cells(co_ord[0], co_ord[1], len(board))
            for neighbour in neighbours:
                if board[neighbour[0]][neighbour[1]] == -1:
                    if is_black:
                        board[neighbour[0]][neighbour[1]] = 1
                    else:
                        board[neighbour[0]][neighbour[1]] = 0
                    if not winning_move(board, not is_black):
                        possible_attack.append([neighbour[0],neighbour[1]])
                    board[neighbour[0]][neighbour[1]] = -1

    #print("smart_play")
    return possible_attack

def randomized_moves(board , count, game_object):
    """
    Generates "count" number of random moves for both players alternately to compensate for lower depth used while calling the minimax function.
    :param board List of lists: current board state
    :param count int: Number of random moves required
    :param game_object: Current game instance
    :return List of lists: Board after the random moves are played
    """
    possible_moves = empty_cells(board)
    turn = 1
    while count > 0 and possible_moves:
        # i = random.randint(0, len(possible_moves) - 1)
        # x, y = possible_moves.pop(i)
        if turn == 1:
            # possible_attack = smart_play(board, game_object.bot)
            # if possible_attack:
            #     i = random.randint(0, len(possible_attack) - 1)
            #     x,y = possible_attack[i]
            #     possible_moves.remove(possible_attack[i])
            # else:
            i = random.randint(0, len(possible_moves) - 1)
            x, y = possible_moves.pop(i)

            if game_object.bot:
                board[x][y] = 1
            else:
                board[x][y] = 0
            turn = 2
            count -= 1
            continue
        else:
            #possible_attack = smart_play(board, game_object.human)
            # if possible_attack:
            #     i = random.randint(0, len(possible_attack) - 1)
            #     x, y = possible_attack[i]
            #     possible_moves.remove(possible_attack[i])
            # else:
            i = random.randint(0, len(possible_moves) - 1)
            x, y = possible_moves.pop(i)

            if game_object.human:
                board[x][y] = 1
            else:
                board[x][y] = 0
            turn = 1
            count -= 1
            continue
    return board

def evaluate(game_object):
    """
    Evaluates the scores for the current game instance
    :param game_object Class instance: Current game instance
    :return score int: Score based on whether its a win, loss or draw for the bot
    """
    board = copy.deepcopy(game_object.board)
    board = randomized_moves(board, len(empty_cells(board)) ,game_object)
    if winning_move(game_object.board, game_object.bot):
        score = 3
    elif winning_move(game_object.board, game_object.human):
        score = -2
    else:
        score = -1
    return score


def game_over(board):
    """
    Checks if the game is over
    :param board List of lists: Current board state
    :return Boolean: True if the game is over, False otherwise
    """
    return winning_move(board, True) or winning_move(board, False)

def empty_cells(board):
    """
    Returns the empty cells in the baord
    :param board List of lists: Current baord state
    :return List of lists: Empty cells in the board
    """

    empty_cells = []
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == -1:
                empty_cells.append([x, y])
    return empty_cells

def minimax(game_object, depth, player, alpha, beta, score):
    """
    Evaluates the best move based on the minimax algorithm. Alpha beta pruning is implemented to improve the performance of the code
    :param game_object Class instance: Current game instance
    :param depth int: Depth until which the algorithm needs to be executed
    :param player int: Represents the player (-1 for human and 1 for bot)
    :param alpha int: Initially -infinity, replaced by the max score during the evaluation
    :param beta int:  Initially +infinity, replaced by the min score during the evaluation
    :return List: Contains the co-ordinates of the best move and the score.
    """
    if player == bot:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(game_object.board):
        score += evaluate(game_object)
        return [-1, -1, score]

    for cell in empty_cells(game_object.board):
        x, y = cell[0],cell[1]
        if player == bot:
            if game_object.bot:
                game_object.board[x][y] = 1
            else:
                game_object.board[x][y] = 0
        else:
            if game_object.human:
                game_object.board[x][y] = 1
            else:
                game_object.board[x][y] = 0
        current_score = minimax(game_object, depth - 1, -player, alpha, beta, score)
        #print("current ", current_score)
        #print("Co-ord ",x,y)
        game_object.board[x][y] = -1
        current_score[0], current_score[1] = x, y
        if player == bot:
            if current_score[2] > best[2]:
                best = current_score  # max value
            alpha = max(alpha, best[2])
            if beta <= alpha:
                break
        else:
            if current_score[2] < best[2]:
                best = current_score  # min value
            beta = min(best[2], beta)
            if beta <= alpha:
                break
            if current_score[2] < best[2]:
                best = current_score  # min value
    return best

def get_move_input(game_object):
    """
    Gets input from the human
    :param game_object: Current game instance
    :return int: x and y co-ordinates of the human move
    """
    while True:
        try:
            print("Enter your move in the same format as this example:")
            print(" 0,0 ")
            move = input()
            (x, y) = tuple(map(int, move.split(',')))
            if game_object.visited[x][y] == 1:
                print("Choose an empty intersection")
                continue
            break
        except ValueError:
            print("Invalid input, Try again")
    return x,y

def play_fcg_cvh(side_len):
    """
    Creates and executes the First capture game between a Computer and a Human
    :param side_len int: Length of each side of the baord
    :return None:
    """
    turn = 1
    #Human player gets to select the colour
    first_move = True
    count = 0
    while True:
        print("Which colour do you choose?")
        player_colour = int(input("Enter 1 for Black or 2 for White: "))
        if player_colour == 1:
            game_object = FirstCaptureGo(side_len,True)
            break
        elif player_colour == 2:
            game_object = FirstCaptureGo(side_len, False)
            break
        else:
            print("Invalid input, try again")

    while True:
        if turn == 1:
            if player_colour == 1:
                print("Your turn")
                x,y = get_move_input(game_object)
                game_object.board[x][y] = 1
                game_object.visited[x][y] = 1
                #game_object.prior_states.append(flat_board(game_object.board))
                win = winning_move(game_object.board, game_object.human)
                if first_move:
                    first_move = False
                    count += 1
                elif win:
                    print("You Won!")
                    print_board(game_object.board)
                    exit()
                print_board(game_object.board)
                turn = 2
            else:
                print("Bot's Turn")
                # best_move = minimax(game_object,len(empty_cells(game_object.board)),bot)
                score = 0
                best_move = minimax(game_object, 5, bot, -infinity, infinity, score)
                x, y = best_move[0], best_move[1]
                game_object.board[x][y] = 1
                game_object.visited[x][y] = 1
                # game_object.prior_states.append(flat_board(game_object.board))
                win = winning_move(game_object.board, game_object.bot)
                if first_move:
                    first_move = False
                elif win:
                    print("Bot Won!")
                    print_board(game_object.board)
                    exit()
                print_board(game_object.board)
                turn = 2
        else:
            if player_colour == 2:
                print("Your turn")
                x,y = get_move_input(game_object)
                game_object.board[x][y] = 0
                game_object.visited[x][y] = 1
                #game_object.prior_states.append(flat_board(game_object.board))
                win = winning_move(game_object.board, game_object.human)
                if win:
                    print("You Won!")
                    print_board(game_object.board)
                    exit()
                print_board(game_object.board)
                turn = 1
            else:
                print("Bot's Turn")
                score = 0
                best_move = minimax(game_object, 5 , bot, -infinity, infinity, score)
                x, y = best_move[0], best_move[1]
                game_object.board[x][y] = 0
                game_object.visited[x][y] = 1
                # game_object.prior_states.append(flat_board(game_object.board))
                win = winning_move(game_object.board, game_object.bot)
                if win:
                    print("Bot Won!")
                    print_board(game_object.board)
                    exit()
                print_board(game_object.board)
                turn = 1


if __name__ == '__main__':
    side_len = 5
    print("Welcome to First Capture go (5x5)")
    print("You are playing against the bot")
    #game_type = int(input())
    play_fcg_cvh(side_len)
