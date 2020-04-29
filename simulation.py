import numpy as np
from scipy.ndimage import gaussian_filter
from random import randint
import matplotlib.pyplot as plt
from battery import battery

# parameters =========
shape_env = (50, 50)
n_batteries = 1
n_danger_points = 2000
n_food_points = 500
sigma = 1
steps = 150
# ====================

def print_plot(env, movements=None, labels=False):
    if movements == None:
        plt.imshow(env, cmap="gray")
        plt.colorbar()
        plt.show()
    else:
        plt.imshow(env, cmap="gray")
        plt.colorbar()
        # draw path
        xs = []
        ys = []
        for m in movements:
            xs.append(m[0])
            ys.append(m[1])
        plt.plot(ys, xs, marker="o")
        
        if labels == True:
            for i, coords in enumerate(zip(xs, ys)):
                plt.text(coords[1], coords[0], str(i), color="blue", fontsize=15)
            
        plt.show()


def get_random_position():
    return (randint(0, shape_env[0]-1), randint(0, shape_env[1]-1))

env = np.zeros(shape_env)

# place danger points in the environment
for _ in range(n_danger_points):
    loc = get_random_position()
    env[loc[0]][loc[1]] = -1

# place food points in the environment
for _ in range(n_food_points):
    loc = get_random_position()
    while env[loc[0]][loc[1]] != 0:
        loc = get_random_position()
    env[loc[0]][loc[1]] = 1

print("Plot of the binary environment")
print_plot(env)

print("Plot of the smoothed environment")
gaussian_env = gaussian_filter(env, sigma=sigma)
print_plot(gaussian_env)

# display the batteries
batteries = []
for _ in range(n_batteries):
    starting_point = get_random_position()
    batteries.append(battery(starting_point, shape_env, gaussian_env))
    print("Starting point: {}".format(starting_point))

for i in range(steps):
    for b in batteries:
        b.movement()
        print("{}) Move in {} | direction {}".format(i+1, b.coord_battery, b.direction))
        # if the battery ate the food, remove from the env and update the gaussian_env
        if env[b.coord_battery[0]][b.coord_battery[1]] == 1:
            b.food += 1
            print("The battery ate the food!")
            env[b.coord_battery[0]][b.coord_battery[1]] = 0
            b.gaussian_env = gaussian_filter(env, sigma=sigma)
            print_plot(b.gaussian_env)

print_plot(env, batteries[0].movements)
print(batteries[0].food)
