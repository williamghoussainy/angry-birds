def trajectory(x, dx, dy, dist):
    return x * dy/dx + (9.81 * x ** 2)/(2 * dist**2 * (dx/dist)**2)