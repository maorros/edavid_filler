from Filler import *
from Filler4Fish import *
from Strokes import *
from RobotPainter import *
from CurvesFish import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import csv



fill = Filler4Fish(canvas_ratio=4, board_height=50, board_width=30, \
              alpha= 0.8, alpha_2 = 0.3, n_switch = 50, \
              x_translation=0, y_translation=0, max_line_length=3000, \
              sp_step_size=50, sp_num_edge_points_remove=2, sp_resolution=0.005, \
              get_images=False)


x,y = fill.draw()
cur = CurvesFish()
cur.set_point_list(x,y)
cur.points_to_pre(1, 0)
x_f = 1.0*cur.x_pre/1000-0.1
y_f = 1.0*cur.y_pre/1000-0.06


plt.plot(x_f, y_f)

with open('fishdraw.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for n in range(len(x_f)):
        wr.writerow([x_f[n], y_f[n]])




plt.pause(40)
