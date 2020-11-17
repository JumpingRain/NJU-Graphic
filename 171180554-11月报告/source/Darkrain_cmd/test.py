def do_clip_cohen(self, x1, y1, x2, y2):
    self.point_vec = []
    x_max_real = max(self.x2, self.x1)
    x_min_real = min(self.x2, self.x1)
    y_min_real = min(self.y1, self.y2)
    y_max_real = max(self.y1, self.y2)
    x_max = max(x1, x2)
    x_min = min(x1, x2)
    y_max = max(y1, y2)
    y_min = min(y1, y2)
    print(x_min, x_max, y_min, y_max)
    bit1 = self.y1 > y_max
    bit2 = self.y1 < y_min
    bit3 = self.x1 > x_max
    bit4 = self.x1 < x_min

    bit5 = self.y2 > y_max
    bit6 = self.y2 < y_min
    bit7 = self.x2 > x_max
    bit8 = self.x2 < x_min

    print(bit1, bit2, bit3, bit4, bit5, bit6, bit7, bit8)

    if (not bit1 and not bit2 and not bit3 and not bit4 and not bit5 and not bit6 and not bit7 and not bit8):
        return True
        # no need inside the rectangular
    elif ((bit1 and bit5) or (bit2 and bit6) or (bit3 and bit7) or (bit4 and bit8)):
        return False
    else:
        if (self.x1 == self.x2):
            self.y1 = max(y_min_real, y_min)
            self.y2 = min(y_max_real, y_max)
            self.draw_line(self.x1, self.y1, self.x2, self.y2, self.algorithm)
            return True
        elif (self.y1 == self.y2):
            self.x1 = max(x_min_real, x_min)
            self.x2 = min(x_max_real, x_max)
            self.draw_line(self.x1, self.y1, self.x2, self.y2, self.algorithm)
            return True
        else:
            print('reach here cal')
            rate = ((float)(self.y1 - self.y2)) / ((float)(self.x1 - self.x2))
            print('rate is ', rate)
            y0 = float(self.y1) - rate * self.x1
            y1 = x_min * rate + y0
            y2 = x_max * rate + y0
            x1 = (y_min - y0) / rate
            x2 = (y_max - y0) / rate
            print(y1, y2, x1, x2)
            print('xy_min is', x_min_real, y_min_real, x_max_real, y_max_real)
            new_x1 = 0
            new_x2 = 0
            new_y1 = 0
            new_y2 = 0
            point_index = 0
            if (y1 < y_max and y1 > y_min and y1 >= y_min_real and y1 <= y_max_real):
                point_index = 1
                new_x1 = x_min
                new_y1 = y1
            if (y2 < y_max and y2 > y_min and y2 >= y_min_real and y2 <= y_max_real):
                if (point_index == 0):
                    point_index = 1
                    new_x1 = x_max
                    new_y1 = y2
                elif (point_index == 1):
                    point_index = 2
                    new_x2 = x_max
                    new_y2 = y2
            if (x1 <= x_max and x1 >= x_min and x1 <= x_max_real and x1 >= x_min_real):
                if (point_index == 0):
                    point_index = 1
                    new_x1 = x1
                    new_y1 = y_min
                elif (point_index == 1):
                    point_index = 2
                    new_x2 = x1
                    new_y2 = y_min
            if (x2 <= x_max and x2 >= x_min and x2 <= x_max_real and x2 >= x_min_real):
                if (point_index == 0):
                    point_index = 1
                    new_x1 = x2
                    new_y1 = y_max
                elif (point_index == 1):
                    point_index = 2
                    new_x2 = x2
                    new_y2 = y_max
            if (point_index == 0):
                print("index is 0")
                return False
            if (point_index == 1):
                if (not bit1 and not bit2 and not bit3 and not bit4):
                    self.x2 = new_x1
                    self.y2 = new_y1
                    self.draw_line(self.x1, self.y1, self.x2, self.y2, self.algorithm)
                    return True
                elif (not bit5 and not bit6 and not bit7 and not bit8):
                    self.x2 = new_x1
                    self.y2 = new_y1
                    self.draw_line(self.x1, self.y1, self.x2, self.y2, self.algorithm)
                    return True

            elif (point_index == 2):
                self.x1 = new_x1
                self.y1 = new_y1
                self.x2 = new_x2
                self.y2 = new_y2
                self.draw_line(self.x1, self.y1, self.x2, self.y2, self.algorithm)
                return True