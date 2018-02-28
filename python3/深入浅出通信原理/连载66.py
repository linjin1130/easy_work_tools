import numpy as np
import matplotlib.pyplot as plt

def unit(num, duty):
    x1 = np.zeros(int(np.ceil(num/2 - duty*num/200)))
    x2 = np.ones(int(np.ceil(duty*num/100)))
    y = np.concatenate([x1,x2])
    z = np.concatenate([y,x1])
    return z

def square(in_array, T, duty):
    space = in_array[-1]-in_array[0]
    num = len(in_array)/(space/T)
    unit_arr = unit(num, duty)
    repeat = int(np.ceil(space/T))
    return  np.tile(unit_arr, repeat)

def square1(x, duty):
    y = []
    for i in x:
        if np.sin(i) > np.sin(np.pi/2 - np.pi/100*duty):
            y.append(1)
        else:
            y.append(0)
    return  np.array(y)

x = np.arange(-8, 8, 0.01)
a = square1(0.125*np.pi*x+np.pi/2, 12.5/4)

plt.figure()
plt.subplot(2,1,1)
plt.plot(x,a)
a = square1(1*np.pi*x+np.pi/2, 25)

x = np.arange(-128,128,1)
plt.subplot(2,1,2)
plt.stem(x, 0.125/4*np.sinc(0.125/4*x), '-')
plt.show()


