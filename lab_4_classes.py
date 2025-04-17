import math
from infos import *
class Integrator:
    def __init__(self, x0, T):
        self.x0 = 0
        self.x1 = 0
        self.integral = x0
        self.T = T

    def update(self, val: float) -> float:
        self.x1 = val
        area = (self.x0 + self.x1) * 0.5 * self.T 
        self.integral += area
        self.x0 = self.x1
        return self.integral

class Odometry:
    def __init__(self, r, B, T):
        self.x_integrator = Integrator(0, T)
        self.y_integrator = Integrator(0, T)
        self.theta_integrator = Integrator(0, T)
        self.B = B
        self.r = r

    def get_speed(self, wl:float, wr:float) -> tuple:
        v = (wr + wl)*self.r/2
        w = (wr - wl)*self.r/self.B
        dth = w
        self.theta = self.theta_integrator.update(dth)
        dx = v * math.cos(self.theta)
        dy = v * math.sin(self.theta)
        return (dx, dy, dth)
    
    def update(self, wl: float, wr: float) -> tuple:
        # Here we integrate the theta derivative
        dx, dy, _ = self.get_speed(wl, wr)
        x = self.x_integrator.update(dx)
        y = self.y_integrator.update(dy)
        return (x, y, self.theta)
    
if __name__ == '__main__':
    wheel_radius = 0.02
    base = 0.17
    # wl = int(input())
    # wr = int(input())
    o = Odometry(wheel_radius, base, 1)
    # print(o.update(wl, wr))
    # print(o.get_speed(-3, 3, 0))

    for i in range(40):
        print(o.update(1, 2))