import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

class CurvesFish:
    def __init__(self):
        self.x_list = []
        self.y_list = []
        self.x_pre = [] # increasing points density and removing edge points
        self.y_pre = []
        self.x_smooth = []
        self.y_smooth = []

    def set_point_list(self, x_list, y_list):
        self.x_list = x_list
        self.y_list = y_list

    def points_to_pre(self, step_size, num_edge_points_remove = 0):
        new_x_list = []
        new_y_list = []
        new_x_list.append(self.x_list[0])
        new_y_list.append(self.y_list[0])
        for n in range(len(self.x_list)-1):
            dir_x = np.sign(self.x_list[n+1] - self.x_list[n])
            dir_y = np.sign(self.y_list[n+1] - self.y_list[n])
            if dir_x != 0 and dir_y == 0:
                step_x = np.arange(self.x_list[n], self.x_list[n + 1] + dir_x * step_size, dir_x * step_size)
                step_y = self.y_list[n] * np.ones(len(step_x))
            elif dir_y != 0 and dir_x == 0:
                step_y = np.arange(self.y_list[n], self.y_list[n + 1] + dir_y * step_size, dir_y * step_size)
                step_x = self.x_list[n] * np.ones(len(step_y))
            elif dir_x != 0 and dir_y != 0:
                step_x = np.arange(self.x_list[n], self.x_list[n + 1] + dir_x * step_size, dir_x * step_size)
                dx = np.abs(self.x_list[n+1] - self.x_list[n])
                dy = np.abs(self.y_list[n+1] - self.y_list[n])
                step_size_y = 1.0*step_size * dy / dx # calculate the y step size according to x step size
                step_y = np.arange(self.y_list[n], self.y_list[n + 1] + dir_y * step_size_y, dir_y * step_size_y)
                step_y = step_y[0:len(step_x)] # make sure x and y are at the same length
            elif dir_x == 0 and dir_y == 0:
                step_x = np.zeros(0) # empty array
                step_y = np.zeros(0)
                pass
            if len(step_x) > num_edge_points_remove*2 and num_edge_points_remove > 0:
                new_x_list = np.concatenate((new_x_list, step_x[num_edge_points_remove:-num_edge_points_remove]))
                new_y_list = np.concatenate((new_y_list, step_y[num_edge_points_remove:-num_edge_points_remove]))
                # print ('removed edge points')
            else:
                new_x_list = np.concatenate((new_x_list, step_x))
                new_y_list = np.concatenate((new_y_list, step_y))
                # print ('didnt removed edge points')

        new_x_list = np.concatenate((new_x_list, [self.x_list[-1]]))
        new_y_list = np.concatenate((new_y_list, [self.y_list[-1]]))
        self.x_pre = new_x_list
        self.y_pre = new_y_list
        return new_x_list, new_y_list

    def points_to_smooth(self, resolution):
        if len(self.x_pre)>10:
            mask = np.where(((np.diff(self.x_pre) == 0) & (np.diff(self.y_pre) == 0)))
            if len(mask[0]) > 0 :
                self.x_pre = np.delete(self.x_pre, mask[0])
                self.y_pre = np.delete(self.y_pre, mask[0])
                print ('deleted duplicates:', len(mask[0]))
            tck, u = interpolate.splprep([self.x_pre, self.y_pre], s=0)
            unew = np.arange(0, 1.0 + resolution, resolution)
            out = interpolate.splev(unew, tck)
            self.x_smooth = out[0]
            self.y_smooth = out[1]
        else:
            self.x_smooth = self.x_pre
            self.y_smooth = self.y_pre

        # remove duplicates in smooth
        mask = np.where(((np.diff(self.x_smooth) == 0) & (np.diff(self.y_smooth) == 0)))
        if len(mask[0]) > 0:
            self.x_smooth = np.delete(self.x_smooth, mask[0])
            self.y_smooth = np.delete(self.y_smooth, mask[0])
            print ('deleted smooth duplicates:', len(mask[0]))
        return self.x_smooth, self.y_smooth

    def display(self, title=''):
        plt.plot(self.x_list, self.y_list, 'x', self.x_pre, self.y_pre,'x', self.x_smooth, self.y_smooth, self.x_list, self.y_list, 'b')
        plt.title(title)
        plt.pause(0.5)