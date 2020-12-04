#The minimax algorithm and the corresponding functions such as evaluate, empty_cells and game over were referred from the below link.
# It was modified and adapted for the first capture game that is implemented in this project
#https://github.com/Cledersonbc/tic-tac-toe-minimax/blob/master/py_version/minimax.py

from math import inf as infinity
import random
human = -1
bot = 1
class FirstCaptureGo:
    def __init__(self,side_len, is_black):
        self.board = []
        self.visited = []
        self.prior_states = []
        for i in range(side_len):
            self.board.append([])
            self.visited.append([])
            for j in range(side_len):
                self.board[i].append(-1)
                self.visited[i].append(0)
        print(self.board)
        self.human = is_black
        self.bot = not is_black

def find_adjacent_cells(x, y, side_len):
    neighbours = []
    for x_neighbour in range(x-1,x+2):
        for y_neighbour in range(y-1,y+2):
            if (-1 < x < side_len and -1 < y < side_len and (x != x_neighbour or y != y_neighbour)
                    and (0 <= x_neighbour < side_len) and (0 <= y_neighbour < side_len)) and (abs(x_neighbour-x) != abs(y_neighbour-y)):
                neighbours.append((x_neighbour,y_neighbour))
    return neighbours

def get_groups(board,is_black):
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



def flat_board(board: list):
    flat_board = ""
    for x in board:
        for y in x:
            flat_board += str(y)
    return flat_board

# def play_fcg(player: list):

    # while True:
    #     x = random.randint(0,len(player.board)-1)
    #     y = random.randint(0,len(player.board)-1)
    #     if player.visited[x][y] == 0:
    #         player.visited[x][y] = 1
    #         if player.is_black:
    #             player.board[x][y] = 1
    #             player.prior_states.append(flat_board(player.board))
    #             win = winning_move(player.board, player.is_black)
    #             if win:
    #                 print("Black Player Won")
    #                 exit()
    #             # print(player.prior_states)
    #             # print(player.board)
    #             # print(player.visited)
    #             break
    #         else:
    #             player.board[x][y] = 0
    #             player.prior_states.append(flat_board(player.board))
    #             win = winning_move(player.board, player.is_black)
    #             if win:
    #                 print("White Player Won")
    #                 exit()
    #             # print(player.prior_states)
    #             # print(player.board)
    #             # print(player.visited)
    #             break

def print_board(board):
    for row in board:
        row = ["_" if x == -1 else x for x in row]
        row = ["B" if x == 1 else x for x in row]
        row = ["W" if x == 0 else x for x in row]
        print(row)


def evaluate(game_object):
    if winning_move(game_object.board, game_object.bot):
        score = 1
    elif winning_move(game_object.board, game_object.human):
        score = -1
    else:
        score = 0
    return score


def game_over(board):
    return winning_move(board, True) or winning_move(board, False)

def empty_cells(board):
    empty_cells = []
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == -1:
                empty_cells.append([x, y])
    return empty_cells

def minimax(game_object, depth, player, alpha, beta):
    if player == bot:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(game_object.board):
        score = evaluate(game_object)
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
        current_score = minimax(game_object, depth - 1, -player, alpha, beta)
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

# def minimax(game_object, depth, player, alpha, beta):
#     # if player == bot:
#     #     best = [-1, -1, -infinity]
#     # else:
#     #     best = [-1, -1, +infinity]
#
#     if depth == 0 or game_over(game_object.board):
#         score = evaluate(game_object)
#         return [-1, -1, score]
#
#     if player == bot:
#         best_val = -infinity
#         for cell in empty_cells(game_object.board):
#             x, y = cell[0],cell[1]
#             if game_object.bot:
#                 game_object.board[x][y] = 1
#             else:
#                 game_object.board[x][y] = 0
#             current_score = minimax(game_object,depth-1, -player, alpha, beta)
#             game_object.board[x][y] = -1
#             current_score[0] = x
#             current_score[1] = y
#             if current_score[2] > best_val[2]:
#                 best_val[2] = current_score[2]
#             alpha = max(alpha, best_val[2])
#             if beta <= alpha:
#                 break
#         return  best_val
#     else:
#         best_val = infinity
#         for cell in empty_cells(game_object.board):
#             x, y = cell[0], cell[1]
#             if game_object.human:
#                 game_object.board[x][y] = 1
#             else:
#                 game_object.board[x][y] = 0
#             current_score = minimax(game_object, depth - 1, -player, alpha, beta)
#             game_object.board[x][y] = -1
#             current_score[0] = x
#             current_score[1] = y
#             if current_score[2] < best_val[2]:
#                 best_val[2] = current_score[2]
#             beta = min(beta, best_val[2])
#             if beta <= alpha:
#                 break
#         return best_val



def get_move_input(game_object):
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
                if count < 1:
                    while True:
                        x = random.randint(0, len(game_object.board) - 1)
                        y = random.randint(0, len(game_object.board) - 1)
                        count += 1
                        if game_object.visited[x][y] == 1:
                            continue
                        else:
                            break
                else:
                    # best_move = minimax(game_object,len(empty_cells(game_object.board)),bot)
                    best_move = minimax(game_object, len(empty_cells(game_object.board)), bot, -infinity, infinity)
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
                best_move = minimax(game_object, len(empty_cells(game_object.board)) , bot, -infinity, infinity)
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

    #side_len  = input("Enter grid length")
    side_len = 5
    #player = FirstCaptureGo(side_len)
    while True:
        print("Play against the bot")
        print("Computer vs Human")
        #game_type = int(input())
        play_fcg_cvh(side_len)
