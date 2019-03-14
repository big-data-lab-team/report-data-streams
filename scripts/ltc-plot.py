#!/usr/bin/env python

from matplotlib import pyplot as plt
from numpy import array


def plot_point(x, y, epsilon, j, k, transmitted):
    xshift = 0.05
    yshift = 0
    size = 'x-small'
    label = "$(u^{}_{}, y^{}_{})$".format(k, j, k, j)
    if transmitted:
        color = 'red'
    else:
        color = 'blue'
    plt.plot(x, y, '.', color=color)
    plt.annotate(label,
                 xy=(x+xshift, y+yshift),
                 fontsize=size)
    if not transmitted:
        plt.plot(x, y+epsilon, '.', color=color)
        plt.plot(x, y-epsilon, '.', color=color)
        plt.plot([x, x], [y-epsilon, y+epsilon], '-', color='blue')

def y_line(x, point_x, point_y, trans_x, trans_y):
    '''
    Return the value of y such that (x,y) is on the line
    defined by (trans_x, trans_y), (point_x, point_y)
    point may be the high or the low point
    '''
    return trans_y + (point_y-trans_y)/(point_x-trans_x)*(x-trans_x)

# Constants
epsilon = 0.5
x = [0, 1, 2, 3, 4, 5, 6]
y = [0, 1, 2.1, 4, 4.15, 5.6, 7.3]
assert(len(x) == len(y))
n = len(x)

# Initialization
lowpoint = y[1] - epsilon
highpoint = y[1] + epsilon
trans_x, trans_y = x[0], y[0]
k = 0 # Number of transmitted points
j = 1 # Current number of non-transmitted points
plot_point(x[0], y[0], epsilon, 0, k, True)
plot_point(x[1], y[1], epsilon, 1, k, False)
#triangle = plt.Polygon(array([[trans_x, trans_y], [x[1], lowpoint], [x[1], highpoint]]), color=(0.8, 0.8, 0.8, 0.5))
#plt.gca().add_patch(triangle)

xis = [x[0]]
taus = [0] 
xis = []
for i in range(2, n):
    j += 1


    # Update high and low lines
    new_low = max(y[i]-epsilon, y_line(x[i], trans_x, trans_y, x[i-1], lowpoint))
    new_high = min(y[i]+epsilon, y_line(x[i], trans_x, trans_y, x[i-1], highpoint))
    if new_low < new_high:
        # Plot non-transmitted point
        plot_point(x[i], y[i], epsilon, j, k, False)
        lowpoint = new_low
        highpoint = new_high
        # triangle = plt.Polygon(array([[trans_x, trans_y], [x[i], lowpoint], [x[i], highpoint]]), color=(0.8, 0.8, 0.8, 0.5))
        # plt.gca().add_patch(triangle)
        continue

    # Plot non-transmitted point
    plot_point(x[i], y[i], epsilon, 1, k+1, False)

    # Low line is above high line: transmit point
    # Plot triangle from previously transmitted point
    triangle = plt.Polygon(array([[trans_x, trans_y], [x[i-1], lowpoint], [x[i-1], highpoint]]), color=(0.8, 0.8, 0.8, 0.5))
    plt.gca().add_patch(triangle)
    
    # Update initial variables
    plt.plot([trans_x, x[i-1]], [trans_y, lowpoint], '--', color=(0.1, 0.1, 0.1, 0.5))
    plt.plot([trans_x, x[i-1]], [trans_y, highpoint], '--', color=(0.1, 0.1, 0.1, 0.5))
    trans_x = x[i-1]
    trans_y = (lowpoint+highpoint)/2
    j = 1
    k = k + 1
    plot_point(trans_x, trans_y, epsilon, 0, k, True)
    taus.append(trans_x)
    xis.append(trans_y)

    # Update variables
    lowpoint = y[i] - epsilon
    highpoint = y[i] + epsilon
 
xticks = []
j = 0
for i in range(0, n):
    if i in taus:
        xticks.append('$t_{}=\\tau_{}$'.format(i,j))
        j += 1
    else:
        xticks.append('$t_{}$'.format(i))
plt.xticks(range(0, n), xticks, fontsize='x-small')

yticks = []
values = sorted(y + xis)
i = 0
k = 1
for v in values:
    if v == 0:
        yticks.append('$\\xi_0 = x_{}$'.format(i))
        i += 1
        continue
    if v in y:
        yticks.append('$x_{}$'.format(i))
        i += 1
    else:
        yticks.append('$\\xi_{}$'.format(k))
        k += 1
plt.yticks(values, yticks, fontsize='x-small')
plt.savefig('./figures/ltc.pdf', dpi=3000)
