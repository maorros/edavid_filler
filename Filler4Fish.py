from Strokes import *
from RobotPainter import *
from Curves import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

class Filler4Fish:
    def __init__(self, canvas_ratio=20, x_translation=170, y_translation = 100, \
                 alpha = 0.3, alpha_2 = 0.1, n_switch = 15, \
                 robot=None, vis= None, board_height = 33, board_width=26, max_line_length = 1000, \
                 sp_step_size = 1, sp_num_edge_points_remove = 3, sp_resolution = 0.1, \
                 get_images = False):
        self.canvas_ratio = canvas_ratio
        self.x_translation = x_translation
        self.y_translation = y_translation
        self.alpha = alpha
        self.alpha_2 = alpha_2
        self.n_switch = n_switch

        # width 650
        # height 500

        self.robot = robot
        self.vis = vis # visual feedback
        self.board_height = board_height
        self.board_width = board_width
        self.max_line_length = max_line_length
        self.sp_step_size = sp_step_size
        self.sp_num_edge_points_remove = sp_num_edge_points_remove
        self.sp_resolution = sp_resolution
        self.get_images = get_images

    def draw(self):
        random.seed(1)
        x_list = []
        y_list = []
        x_fish = []
        y_fish = []

        line_length = 0
        #color = random.randint(0, 1)
        #self.robot.dip_slot_paint(color)
        st = Strokes()

        st.set_board_size(self.board_height, self.board_width)

        st.set_best_straight_pos()
        x, y = st.get_current_pos()
        x_list.append(self.canvas_ratio * x + self.x_translation)
        y_list.append(self.canvas_ratio * y + self.y_translation)

        for n in range(100000):
            if n == self.n_switch:
                self.alpha = self.alpha_2
            if st.is_board_full():
                break
            stroke = st.get_best_straight_stroke()
            if stroke:
                p = random.random()
                if p < self.alpha:
                    stroke = st.get_random_stroke()
                st.draw_stroke(stroke[0], stroke[1])
                st.set_current_pos(stroke[0], stroke[1])
                #st.display(str(n)+' '+str(line_length))
                x, y = st.get_current_pos()
                x_list.append(self.canvas_ratio * x + self.x_translation)
                y_list.append(self.canvas_ratio * y + self.y_translation)
                line_length += np.sqrt((x_list[-1]-x_list[-2])**2 + (y_list[-1]-y_list[-2])**2)
            else:
                st.set_best_straight_pos()
                x, y = st.get_current_pos()
                x_list.append(self.canvas_ratio * x + self.x_translation)
                y_list.append(self.canvas_ratio * y + self.y_translation)
        return x_list, y_list


    def draw_to_fish(self, x_list, y_list):
        cur = Curves()
        cur.set_point_list(x_list, y_list)
        cur.points_to_pre(1, 0)



