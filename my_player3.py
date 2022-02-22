import copy
import time


def read_input():
    with open('input.txt') as f:
        lines = f.readlines()
    f.close()
    i = 0
    prev_board = []
    curr_board = []
    your_color = '1'
    for line in lines:
        line = line.replace("\n", "", -1)
        i = i + 1
        if i == 1:
            your_color = line
            continue
        elif (i > 1) and (i < 7):
            list_ = []
            for char in line:
                list_.append(char)
            prev_board.append(list_)
        else:
            list_ = []
            for char in line:
                list_.append(char)
            curr_board.append(list_)
    try:
        with open('counter.txt') as f:
            count = int(f.readline())
    except:
        count = 0

    return count, your_color, prev_board, curr_board

def compare_board(prev_board, curr_board):
    for i in range(0, 5):
        for j in range(0, 5):
            if prev_board[i][j] != curr_board[i][j]:
                return False
    return True

def write_output(x, y):
    f = open("output.txt", "w")
    f.write(str(x) + "," + str(y))
    f.close()


def write_pass():
    f = open("output.txt", "w")
    f.write("PASS")
    f.close()


def find_neighbours(x, y):
    neighbours = []
    if x > 0:
        neighbours.append((x - 1, y))
    if y > 0:
        neighbours.append((x, y - 1))
    if x < 4:
        neighbours.append((x + 1, y))
    if y < 4:
        neighbours.append((x, y + 1))
    return neighbours


class Game:
    def __init__(self, your_color, prev_board, curr_board):
        self.your_game_score = -2.5
        if your_color == '2':
            self.your_game_score = 2.5
        self.your_color = your_color
        self.prev_board = copy.deepcopy(prev_board)
        self.curr_board = copy.deepcopy(curr_board)

    def differ_board(self):
        for i in range(0, 5):
            for j in range(0, 5):
                if self.curr_board[i][j] != self.prev_board[i][j]:
                    return True
        return False

    def find_connecting_point_neighbours(self, x, y):
        connecting_point_neighbours = []
        neighbours = find_neighbours(x, y)
        for neighbour in neighbours:
            if self.curr_board[neighbour[0]][neighbour[1]] == self.curr_board[x][y]:
                connecting_point_neighbours.append(neighbour)
        return connecting_point_neighbours

    def dfs(self, x, y):
        connecting_points = []
        point_list = [(x, y)]
        while point_list:
            curr_point = point_list.pop()
            connecting_points.append(curr_point)
            connecting_point_neighbours = self.find_connecting_point_neighbours(curr_point[0], curr_point[1])
            for connecting_point_neighbour in connecting_point_neighbours:
                if connecting_point_neighbour not in point_list and connecting_point_neighbour not in connecting_points:
                    point_list.append(connecting_point_neighbour)
        return connecting_points

    def check_liberty(self, x, y):
        connecting_points = self.dfs(x, y)
        for point in connecting_points:
            neighbours = find_neighbours(point[0], point[1])
            for neighbour in neighbours:
                if self.curr_board[neighbour[0]][neighbour[1]] == '0':
                    return True
        return False

    def find_attacked_points(self, color):
        attacked_points = []
        for i in range(0, 5):
            for j in range(0, 5):
                if self.curr_board[i][j] == color:
                    if not self.check_liberty(i, j):
                        attacked_points.append((i, j))
        return attacked_points

    def check_remove_attacked_points(self, color):
        attacked_points = self.find_attacked_points(color)
        if len(attacked_points) == 0:
            return False, 0
        for point in attacked_points:
            self.curr_board[point[0]][point[1]] = '0'
        return True, len(attacked_points)

    def get_all_valid_moves(self):
        valid_moves = []
        for i in range(0, 5):
            for j in range(0, 5):
                if self.curr_board[i][j] == '0':
                    copy_curr_game = copy.deepcopy(self)
                    copy_curr_game.curr_board[i][j] = copy_curr_game.your_color
                    if copy_curr_game.check_liberty(i, j):
                        valid_moves.append((i, j))
                    else:
                        is_point_removed, _ = copy_curr_game.check_remove_attacked_points(str(3-int(copy_curr_game.your_color)))
                        # KO Case
                        if not(is_point_removed and compare_board(self.prev_board, copy_curr_game.curr_board)):
                            valid_moves.append((i,j))

        return valid_moves

    def max_min_format(self, each_move, original_color):
        temp_game = copy.deepcopy(self)
        temp_game.prev_board = temp_game.curr_board
        if temp_game.your_color == '2':
            temp_game.your_color = '1'
        else:
            temp_game.your_color = '2'
        temp_game.curr_board[each_move[0]][each_move[1]] = self.your_color
        remove_attack_points, add_score = temp_game.check_remove_attacked_points(temp_game.your_color)
        if remove_attack_points:
            if temp_game.your_color == original_color:
                temp_game.your_game_score = temp_game.your_game_score - add_score
            else:
                temp_game.your_game_score = temp_game.your_game_score + add_score

        return temp_game

    def last_time_filled_coord(self):
        for i in range(0, 5):
            for j in range(0, 5):
                if self.curr_board[i][j] != '0' and self.prev_board[i][j] == '0':
                    return i, j
        return -1, -1

    def get_euler_value(self, color):
        padded_board = []
        first_padding_row = ['0', '0', '0', '0', '0', '0', '0']
        padded_board.append(first_padding_row)
        for i in range(0, 5):
            padded_row = ['0']
            for j in range(0, 5):
                padded_row.append(self.curr_board[i][j])
            padded_row.append('0')
            padded_board.append(padded_row)
        padded_board.append(first_padding_row)

        q4 = 0
        q1 = 0
        q3 = 0
        for i in range(0, 6):
            for j in range(0, 6):
                count_color = 0
                if padded_board[i][j] == color:
                    count_color = count_color + 1
                if padded_board[i][j + 1] == color:
                    count_color = count_color + 1
                if padded_board[i + 1][j + 1] == color:
                    count_color = count_color + 1
                if padded_board[i + 1][j] == color:
                    count_color = count_color + 1

                if count_color == 1:
                    q1 = q1 + 1
                if count_color == 3:
                    q3 = q3 + 1
                if count_color == 2:
                    if (padded_board[i][j] == color and padded_board[i + 1][j + 1] == color) or \
                            (padded_board[i][j + 1] == color and padded_board[i + 1][j] == color):
                        q4 = q4 + 1

        return (q1 - q3 + 2 * q4) / 4.0

    def evaluate(self, color):
        num_pieces = 0
        edges = 0
        opp_color = str(3 - int(color))
        liberties = 0
        counted_neighbour = dict()
        for i in range(0, 5):
            for j in range(0, 5):
                if self.curr_board[i][j] == color:
                    num_pieces = num_pieces + 1
                    if (i == 0) or (j == 0):
                        edges = edges - 1
                    neighbours = find_neighbours(i, j)
                    for neighbour in neighbours:
                        if self.curr_board[neighbour[0]][neighbour[1]] == '0' and counted_neighbour.get(neighbour, False):
                            liberties = liberties + 1
                            counted_neighbour[neighbour] = True
                elif self.curr_board[i][j] == opp_color:
                    num_pieces = num_pieces - 1
                    if (i == 0) or (j == 0):
                        edges = edges + 1
                    neighbours = find_neighbours(i, j)
                    for neighbour in neighbours:
                        if self.curr_board[neighbour[0]][neighbour[1]] == '0' and counted_neighbour.get(neighbour, False):
                            liberties = liberties - 1
                            counted_neighbour[neighbour] = True
        euler_value_col = self.get_euler_value(color)
        euler_value_opp_col = self.get_euler_value(opp_color)

        return min(max(liberties, -4), 4) - 4 * (euler_value_col - euler_value_opp_col) + 5 * num_pieces + edges + self.your_game_score

    def find_move(self, depth, isMax, alpha, beta, original_color):
        if depth == 0 :
            return self.evaluate(original_color), -1, -1
        valid_moves = self.get_all_valid_moves()
        if len(valid_moves) == 0:
            return self.evaluate(original_color), -1, -1
        best_coordinate = ()
        if isMax:
            best_score = float("-inf")
            for each_move in valid_moves:
                temp_game = self.max_min_format(each_move, original_color)
                score, _, _ = temp_game.find_move(depth - 1, not isMax, alpha, beta, original_color)
                if score > best_score:
                    best_score = score
                    best_coordinate = (each_move[0], each_move[1])
                alpha = max(best_score, alpha)
                if alpha >= beta:
                    break
            return best_score, best_coordinate[0], best_coordinate[1]
        else:
            best_score = float("inf")
            for each_move in valid_moves:
                temp_game = self.max_min_format(each_move, original_color)
                score, _, _ = temp_game.find_move(depth - 1, not isMax, alpha, beta, original_color)
                if score < best_score:
                    best_score = score
                    best_coordinate = (each_move[0], each_move[1])
                beta = min(best_score, beta)
                if alpha >= beta:
                    break
            return best_score, best_coordinate[0], best_coordinate[1]


if __name__ == "__main__":
    count, your_color, prev_board, curr_board = read_input()
    game = Game(your_color, prev_board, curr_board)
    score, x, y = game.find_move(4, True, float("-inf"), float("inf"), your_color)
    if x == -1:
        write_pass()
    else:
        write_output(x, y)
