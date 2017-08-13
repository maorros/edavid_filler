import numpy as np
import random
import matplotlib.pyplot as plt

class Strokes:
    def __init__(self):
        self.board_height = 33
        self.board_width = 26
        self.board = np.zeros((self.board_height, self.board_width))
        self.goal = np.ones((self.board_height, self.board_width))
        self.initial_pos = (0,0)
        self.current_pos = (0,0)

    def set_board_size(self, height, width):
        self.board_height = height
        self.board_width = width
        self.board = np.zeros((self.board_height, self.board_width))
        self.goal = np.ones((self.board_height, self.board_width))

    def set_current_pos(self, i, j):
        self.current_pos = (i,j)

    def set_n_fill_current_pos(self, i, j):
        self.current_pos = (i,j)
        self.board[i,j] = 1

    def get_current_pos(self):
        return self.current_pos[0], self.current_pos[1]

    def get_possible_strokes(self):
        end_point_list = []
        directions = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
        for vec in directions:
            point = self.current_pos
            while point[0] >= 0 and point[0] <= self.board_height-1 and \
            point[1] >= 0 and point[1] <= self.board_width-1:
                point = (point[0]+vec[0], point[1]+vec[1])
                if point[0] >= 0 and point[0] <= self.board_height-1 and \
                point[1] >= 0 and point[1] <= self.board_width-1:
                    if self.board[point] == 1:
                        break
            point = (point[0] - vec[0], point[1] - vec[1])
            if point != self.current_pos:
                end_point_list.append(point)
        return end_point_list

    def get_possible_straight_strokes(self):
        end_point_list = []
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        for vec in directions:
            point = self.current_pos
            while point[0] >= 0 and point[0] <= self.board_height-1 and \
            point[1] >= 0 and point[1] <= self.board_width-1:
                point = (point[0]+vec[0], point[1]+vec[1])
                if point[0] >= 0 and point[0] <= self.board_height-1 and \
                point[1] >= 0 and point[1] <= self.board_width-1:
                    if self.board[point] == 1:
                        break
            point = (point[0] - vec[0], point[1] - vec[1])
            if point != self.current_pos:
                end_point_list.append(point)
        return end_point_list

    def get_best_stroke(self):
        possible = self.get_possible_strokes()
        if not possible:
            return None
        lengths = [np.sqrt((p[0] - self.current_pos[0]) ** 2 + (p[1] - self.current_pos[1]) ** 2) for p in possible]
        ind = lengths.index(max(lengths))
        return possible[ind]

    def get_best_straight_stroke(self):
        possible = self.get_possible_straight_strokes()
        if not possible:
            return None
        lengths = [np.sqrt((p[0] - self.current_pos[0]) ** 2 + (p[1] - self.current_pos[1]) ** 2) for p in possible]
        ind = lengths.index(max(lengths))
        return possible[ind]

    def get_random_stroke(self):
        possible = self.get_possible_strokes()
        if not possible:
            return None
        ind = np.random.choice(range(len(possible)))
        end_p =  possible[ind]
        direction = (np.sign(end_p[0]-self.current_pos[0]), np.sign(end_p[1]-self.current_pos[1]))
        sub_length = random.randint(1, max(np.abs(end_p[0] - self.current_pos[0]), np.abs(end_p[1] - self.current_pos[1])))
        short_end_p = (self.current_pos[0]+sub_length*direction[0], self.current_pos[1]+sub_length*direction[1])
        return short_end_p


    def draw_stroke(self,end_point_i, end_point_j):
        direction = (np.sign(end_point_i - self.current_pos[0]), np.sign(end_point_j - self.current_pos[1]))
        point = self.current_pos
        self.board[point] = 1
        while point != (end_point_i, end_point_j):
            point = (point[0]+direction[0], point[1]+direction[1])
            self.board[point] = 1

    def set_random_pos(self):
        white_board = np.where(self.board == 0)  # indexes of white board
        if len(white_board[0]) != 0:
            rnd_index = random.choice(range(len(white_board[0])))
            i = white_board[0][rnd_index]
            j = white_board[1][rnd_index]
            self.current_pos = (i, j)
            self.board[i, j] = 1  # paint the current position

    def set_best_pos(self):
        white_board = np.where(self.board == 0)  # indexes of white board
        if len(white_board[0]) == 0:
            return
        max_list = []
        current_max = 0
        best_pos = (white_board[0][0], white_board[1][0])
        for n in range(len(white_board[0])):
            self.set_current_pos(white_board[0][n], white_board[1][n])
            list = self.get_possible_strokes()
            if not list:
                max_list.append(0)
            else:
                max_length = max([np.sqrt((p[0]-self.current_pos[0])**2+(p[1]-self.current_pos[1])**2) for p in list])
                max_list.append(max_length)
                if max_length > current_max:
                    current_max = max_length
                    best_pos = (white_board[0][n], white_board[1][n])
        self.set_n_fill_current_pos(best_pos[0], best_pos[1])
        #print best_pos
        return best_pos, max_list

    def set_best_straight_pos(self):
        white_board = np.where(self.board == 0)  # indexes of white board
        if len(white_board[0]) == 0:
            return
        max_list = []
        current_max = 0
        best_pos = (white_board[0][0], white_board[1][0])
        for n in range(len(white_board[0])):
            self.set_current_pos(white_board[0][n], white_board[1][n])
            list = self.get_possible_straight_strokes()
            if not list:
                max_list.append(0)
            else:
                max_length = max([np.sqrt((p[0]-self.current_pos[0])**2+(p[1]-self.current_pos[1])**2) for p in list])
                max_list.append(max_length)
                if max_length > current_max:
                    current_max = max_length
                    best_pos = (white_board[0][n], white_board[1][n])
        self.set_n_fill_current_pos(best_pos[0], best_pos[1])
        #print best_pos
        return best_pos, max_list

    def is_board_full(self):
        if np.array_equal(self.board, self.goal):
            return True
        else:
            return False

    def display(self, title=''):
        current = np.zeros((self.board_height, self.board_width))
        current[self.current_pos]=3
        plt.imshow(self.board+current, interpolation='none')
        plt.title(title)
        plt.pause(0.5)

