#!/usr/bin/env python
# utils.py
# Author: Fabrício Olivetti de França
#
# utility functions for the Q-Learning agent

import sys
import pickle
import os
from rle_python_interface.rle_python_interface import RLEInterface
import numpy as np
from numpy.random import uniform, choice, random

# Todas as possíveis ações
actions_map = {'noop':0, 'down':32, 'up':16, 'jump':1, 'spin':3, 
               'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67, 
               'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131, 
               'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
               }

# Vamos usar apenas um subconjunto
actions_list = [66,130,128,131,386]

# faz as ações até mudar de estado
def performAction(a, rle):
  reward = 0
  if a == 64 or a == 128:
    for it in range(8):
      reward += rle.act(a)
  elif a == 66 or a == 130:
    for it in range(4):
      reward += rle.act(a)
  elif a == 131 or a == 67:
    for it in range(8):
      reward += rle.act(a)
  elif a == 386 or 322:
    for it in range(4):
      reward += rle.act(a)
  else:
    reward += rle.act(a)
  return reward

# Retorna a melhor ação do estado atual pela matriz Q  
def getBestActionDet(Q, state):
  # recupera o valor de Q para todas as ações
  qvals = np.array([Q.get(f'{state},{ai}',(0.0,0)) [0]
                     for ai in actions_list])

  # Se empatar, sorteia entre eles                     
  maxval = np.max(qvals)
  if (qvals == maxval).sum() > 1:
    idx = choice(np.nonzero(qvals==maxval)[0])
  else:
    idx = np.argmax(qvals)
  return idx

def getNewActionDet(Q, state):
  # recupera o valor de Q para todas as ações
  qvals = np.array([Q.get(f'{state},{ai}',(0.0,0))[1] 
                     for ai in actions_list])

  # Se empatar, sorteia entre eles       
  if (np.abs(qvals)<=20).sum() > 0:
    idx = choice(np.nonzero(np.abs(qvals)<=20)[0])
  else:
    idx = choice(np.nonzero(qvals)[0])
  return idx
  
def loadInterface(display=False):
  rle = RLEInterface()
  rle.setInt(b'random_seed', 12)
  rle.setBool(b'sound', False)
  
  if sys.platform == 'darwin':
    import pygame
    pygame.init()
  rle.setBool(b'display_screen', display)

  rle.loadROM('super_mario_world.smc', 'snes')
  return rle

  
def getStoredQ(fname='Q.pkl'):
  Q, ep, maxActions = {}, 0, 0
  if os.path.exists(fname):
    Q, ep, maxActions = pickle.load(open(fname, 'rb'))
  return Q, ep, maxActions 
