from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np


def normal_data_plotting(data):
    print 'NORMAL_DATA_PLOTTING'
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter([H for UPC, H, S, V in data], [S for UPC, H, S, V in data], [UPC for UPC, H, S, V in data],
               zdir='z', label='CARACTERIZACION PROTOTIPO VERTICAL', cmap='Blues')
    # ax.plot([H for UPC, H, S, V in data], [S for UPC, H, S, V in data], [UPC for UPC, H, S, V in data],
    # 'red')
    ax.set_xlabel('HUE')
    ax.set_ylabel('SATURATION')
    ax.set_zlabel('UPC')
    ax.legend()

    plt.show()


def cylindrical_data_plotting(data):
    print 'CYLINDRICAL_DATA_PLOTTING'
    # prepare some coordinates, and attach rgb values to each
    r = [(float(S) / 100.0) for UPC, H, S, V in data]
    theta = [((float(H) * np.pi) / 180.0) for UPC, H, S, V in data]
    z = [(float(UPC)) for UPC, H, S, V in data]
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(x, y, z, zdir='z', label='CARACTERIZACION PROTOTIPO VERTICAL', cmap='Blues')
    # ax.plot(x, y, z,'red')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('UPC')
    ax.legend()

    plt.show()

