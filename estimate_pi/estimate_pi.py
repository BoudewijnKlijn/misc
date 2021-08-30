#!/usr/bin/env python
# coding: utf-8

# # Estimate pi
# 
# By choosing random points and checking whether they are inside a circle in a square.
# 
# - Area circle: pi * r^2
# - Area square:  (2 * r)^2
#    - where r is half the diameter and half a side
# 
# Ratio: pi / 4 = circle / square, so pi = 4 * circle / square
# 
# 1. Draw two random numbers from random uniform(0, 1)
# 1. Square and sum them
# 1. If < 1, it means they are within the circle
# 
# We observe only a quarter of the circle but also only a quarter of the square so ratio is the same.

# In[1]:


import numpy as np
import matplotlib.pyplot as plt


# In[2]:


np.random.seed(0)
n = int(1e7)
r = np.random.random((n, 2))
r2 = ((r**2).sum(axis=1) < 1)
r3 = r2.cumsum()
inside_square = np.arange(1, n+1)
r4 = 4 * r3 / inside_square


# In[3]:


plt.semilogx(r4)
plt.hlines(np.pi, 0, n, color='orange', linestyle='--')
# plt.ylim([2, 4])
plt.ylabel('estimate of pi')
plt.xlabel('# random numbers')
plt.savefig('figure1.png')
plt.show()

