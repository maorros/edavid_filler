from Strokes import *
from RobotPainter import *
from Curves import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

# c = Curves()
# c.set_point_list([20, 40, 30, 30], [10, 40, 40, 50])
# c.points_to_pre(0.5,3)
# s_x, s_y = c.points_to_smooth(0.001)
# c.display()

canvas_ratio = 20
x_translation = 170
y_translation = 100
alpha = 0.3
# width 650
# height 500
dip_ratio = 5
dip_count = 0

random.seed(1)

robot = RobotPainter()
vis = Camera()
# simulation
robot.init('134.34.231.221:33333')
vis.init('134.34.231.221:55555')

# big robot
# robot.init('192.168.1.6:33333')
# vis.init('192.168.1.6:55555')
robot.start()
[width, height] = robot.get_canvas_size()
print (width, height)

res = vis.get_resolution()
# img = vis.get_image()
# png = vis.get_png()

x_list = []
y_list = []

st = Strokes()
st.set_board_size(33,26)
st.set_best_straight_pos()
x, y = st.get_current_pos()
x_list.append(canvas_ratio*x+x_translation)
y_list.append(canvas_ratio*y+y_translation)

for n in range(1000):
    if st.is_board_full():  # TODO: check why doesn't stop
        break
    stroke = st.get_best_straight_stroke()
    if stroke:
        p = random.random()
        if p < alpha:
            stroke = st.get_random_stroke()
        st.draw_stroke(stroke[0], stroke[1])
        st.set_current_pos(stroke[0], stroke[1])
        st.display(str(n))
        x, y = st.get_current_pos()
        x_list.append(canvas_ratio * x + x_translation)
        y_list.append(canvas_ratio * y + y_translation)
    else:
        for p in range(len(x_list) - 1):
            if dip_count % dip_ratio == 0:
                color = random.randint(0,1)
                robot.dip_slot_paint(color)
            dip_count += 1
            res = robot.move_pose_safe([x_list[p], x_list[p + 1]], [y_list[p], y_list[p + 1]])
            img = vis.get_image()
        st.set_best_straight_pos()
        x_list = []
        y_list = []
        x, y = st.get_current_pos()
        x_list.append(canvas_ratio * x + x_translation)
        y_list.append(canvas_ratio * y + y_translation)

for p in range(len(x_list) - 1):
    if dip_count % dip_ratio == 0:
        color = random.randint(0, 1)
        robot.dip_slot_paint(color)
    dip_count += 1
    res = robot.move_pose_safe([x_list[p], x_list[p + 1]], [y_list[p], y_list[p + 1]])
    img = vis.get_image()






# for p in range(len(x_list)-2):
#     robot.dip_slot_paint(0)
#     res = robot.move_pose_safe([x_list[p], x_list[p+1]], [y_list[p], y_list[p+1]])
#     img = vis.get_image()

    # strokes_list = st.get_possible_strokes()
    # stroke = st.get_best_stroke()
    # if strokes_list: # if list is not empty
    #     st.draw_stroke(strokes_list[0][0], strokes_list[0][1])
    #     st.set_current_pos(strokes_list[0][0], strokes_list[0][1])
    #     st.display(str(n))
    # else:
    #     st.set_best_pos()
#
# l = st.get_possible_strokes()
# for t in l:
#     st.draw_stroke(t[0], t[1])
# st.display()
# st.set_current_pos(5,3)
# l = st.get_possible_strokes()
# for t in l:
#     st.draw_stroke(t[0], t[1])
# st.display()
# plt.pause(4)
