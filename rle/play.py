#!/usr/bin/env python
# play.py
# Author: Fabrício Olivetti de França
#
# play the Q-learning agent
# using RLE

import sys
from rle_python_interface.rle_python_interface import RLEInterface
import numpy as np
from numpy.random import uniform, choice, random
import pickle
import os
import time
from rominfo import *
from utils import *

# Todas as possíveis ações
actions_map = {'noop':0, 'down':32, 'up':16, 'jump':1, 'spin':3,
               'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67,
               'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131,
               'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
               }


# parâmetros do Q-Learning
radius = 6

def printState(state):
    state_n = np.reshape(state.split(','), (2*radius + 1, 2*radius + 1))
    _=os.system("clear")
    mm = {'0':'  ', '1':'$$', '-1':'@@'}
    for i,l in enumerate(state_n):
      line = list(map(lambda x: mm[x], l))
      if i == radius + 1:
        line[radius] = 'X'
      print(line)

def play():
  rle = loadInterface(True)
  #time.sleep(30)
  fname = 'Q.pkl'
  if len(sys.argv) > 1:
    fname = sys.argv[1]

  Q, ep, maxActions = getStoredQ(fname)

  total_reward = 0

  while not rle.game_over():
    state, x, y = getState(rle.getRAM(), radius)
    printState(state)

    a = actions_list[getBestActionDet(Q, state)]
    qv, t = Q.get(f'{state},{a}', (0.0,0))
    qvs = [(ai,Q.get(f'{state},{ai}', (0.0, 0))) for ai in actions_list]
    print(f'{a} {qv} {qvs}')

    total_reward += performAction(a, rle)

  print('score:', total_reward, 'distance: ', x)

def main():
  play()

if __name__ == "__main__":
  main()

