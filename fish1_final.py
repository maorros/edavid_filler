from Filler import *
from Strokes import *
from RobotPainter import *
from Curves import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import csv

with_robot = True
with_camera = False

if with_robot:
    robot = RobotPainter()
    vis = Camera()

    # simulation
    # robot.init('134.34.231.221:33333')
    # vis.init('134.34.231.221:55555')

    # e-david
    robot.init('192.168.1.6:33333')
    vis.init('192.168.1.6:55555')
    #
    robot.start()
    [width, height] = robot.get_canvas_size()
    print (width, height)

    res = vis.get_resolution()

x_f = []
y_f = []
x_list = []
y_list = []

n=0
scale = 2500.0
scale = 1625.0
with open('default.combine1.csv', 'rb') as csvfile:
    # spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print row['x'], row['y']
        x_f.append(float(row['x']))
        y_f.append(float(row['y']))
        x_list.append(np.max([10.0,float(row['y'])*scale+170+100+250]))
        y_list.append(np.max([10.0,float(row['x'])*scale+100+100+150]))
        n += 1
        if n>200000:
            break

print ('length:', len(x_list))
print (np.min(x_list), np.max(x_list), np.min(y_list), np.max(y_list), np.mean(x_list), np.mean(y_list))
print (np.min(x_f), np.max(x_f), np.min(y_f), np.max(y_f), np.mean(x_f), np.mean(y_f))

temp_x_list = x_list[0:20661]
temp_y_list = y_list[0:20661]
print (np.min(temp_x_list), np.max(temp_x_list), np.min(temp_y_list), np.max(temp_y_list), np.mean(temp_x_list), np.mean(temp_y_list))
print (np.min(x_f), np.max(x_f), np.min(y_f), np.max(y_f), np.mean(x_f), np.mean(y_f))

# plt.plot(x_list[1:10000], y_list[1:10000])
# plt.pause(1)

length = 0
st=0
x_r = []
y_r = []

if with_robot:
    color = random.randint(0, 1)
    robot.dip_slot_paint(color)

for k in range(int(0*len(x_list)),int(0.35*len(x_list)-1)):
    x_r.append(int(x_list[k]))
    y_r.append(int(y_list[k]))
    length += np.sqrt((x_list[k+1] - x_list[k])**2 + (y_list[k+1] - y_list[k])**2)
    # print length
    if length > 3000:
        # remove duplicates
        mask = np.where(((np.diff(x_r) == 0) & (np.diff(y_r) == 0)))
        if len(mask[0]) > 0:
            x_r = np.delete(x_r, mask[0])
            y_r = np.delete(y_r, mask[0])
            print ('deleted duplicates:', len(mask[0]))

        plt.plot(x_r, y_r)
        plt.axis('equal')
        plt.axis([170, 170+700, 100, 100+500])
        # axes = plt.gca()
        # axes.set_xlim([0, 800])
        # axes.set_ylim([0, 800])

        print len(x_r)
        plt.title('length:'+str(length)+' k:'+str(k))
        plt.pause(1)
        if with_robot:
            color = random.randint(0, 1)
            robot.dip_slot_paint(color)
            robot.move_pose_safe(x_r, y_r)
        x_r = []
        y_r = []
        length = 0
        st += 1
        if with_camera:
            robot.hide_pose()
            png = vis.get_png('fish_'+ str(st) + '.png')
            robot.home_pose()
            # img = vis.get_image()


plt.pause(10)





