from Filler import *
from Strokes import *
from RobotPainter import *
from Curves import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

random.seed(3)

robot = RobotPainter()
vis = Camera()

# simulation
robot.init('134.34.231.221:33333')
vis.init('134.34.231.221:55555')

# e-david
# robot.init('192.168.1.6:33333')
# vis.init('192.168.1.6:55555')

robot.start()
[width, height] = robot.get_canvas_size()
print (width, height)

res = vis.get_resolution()

fill = Filler(robot=robot, vis=vis, canvas_ratio=10, board_height=50, board_width=30, \
              alpha= 0.8, alpha_2 = 0.3, n_switch = 50, \
              x_translation=170 + 100, y_translation=100 + 100, max_line_length=3000, \
              sp_step_size=50, sp_num_edge_points_remove=2, sp_resolution=0.005, \
              get_images=False)


fill.draw()
