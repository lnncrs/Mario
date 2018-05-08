#!/usr/bin/env python
# marioRule.py
# Author: Fabrício Olivetti de França
#
# Agente baseado em regras para o SMW

import sys
from rle_python_interface.rle_python_interface import RLEInterface
import numpy as np
from numpy.random import uniform, choice, random
import pickle
import os
import time
from rominfo import *
from utils import *

def rule():
  rle = loadInterface(True)
  
  total_reward = 0
  long_jump = False
  
  while not rle.game_over():
    state, x, y = getInputs(rle.getRAM())
    printState(state)
    
    if long_jump==True:
      total_reward += rle.act(131)
      total_reward += rle.act(131)
      long_jump = False
    else:
      if state_mtx[7,9]==-1 or state_mtx[7,8]==-1:
        total_reward += rle.act(384)
      elif state_mtx[5,11] == -1:
        total_reward += rle.act(130)
      elif state_mtx[5,9]==-1 or state_mtx[5,8]==-1:
        if state_mtx[4,9]==-1 or state_mtx[4,8]==-1:
          total_reward += rle.act(128)
        else:
          total_reward += rle.act(131)
          long_jump = True
      else:
        total_reward += rle.act(128)
  return total_reward

def main():
  r = rule()
    
if __name__ == "__main__":
  main()  
