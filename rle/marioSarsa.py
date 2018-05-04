#!/usr/bin/env python
# marioQLearning.py
# Author: Fabrício Olivetti de França
#
# A simple Q-Learning Agent for Super Mario World
# using RLE

import sys
from rle_python_interface.rle_python_interface import RLEInterface
import numpy as np
from numpy.random import uniform, choice, random

import time
from rominfo import *
from utils import *

# parâmetros do Q-Learning
l_rate = 0.8
gamma  = 0.6
thr    = 0.7
radius = 6
  
def getReward(reward, gameOver, action, dx):
  R = 0 
  
  # +0.5 for stomping enemies or getting itens/coins
  if reward > 0 and not gameOver:
    R += 0.8*np.log(reward)
 
  # incentiva andar pra direita
  if action == 128 and dx > 0:
    R += 0.5
  # e pular correndo
  elif action == 130 and dx > 0:
    R += 0.5

  if gameOver:
    R  -= 2.0
  else:
    R  += 0.1 
    
  return R
   
def getAction(state, Q, randomOrnew):
  if random() > thr:
    if randomOrnew > 0.5:
      a = actions_list[choice(len(actions_list))]
    else:
      # pega uma ação nunca escolhida para diversificar
      a = actions_list[getNewActionDet(Q, state)]
  # deterministica (1-thr)% de chances ou a cada dez episodios
  else:
    a = actions_list[getBestActionDet(Q, state)]     
  return a
  
# Sarsa     
def train():
  rle = loadInterface(False)
    
  Q, ep, maxActions = getStoredQ('Qsarsa.pkl')

  total_reward, total_my_reward = 0, 0
  stateOld = ''
  state, x, y = getState(rle.getRAM(), radius)
  randomOrnew = random()
  it = 0
  
  a = getAction(state, Q, randomOrnew)
  
  while not rle.game_over():
 
    # aplica a acao e monta a chave da tabela e pega o proximo estado
    reward = performAction(a, rle)          
    current_key = f'{stateOld},{state},{a}'
    
    stateOld = state
    state, xn, yn = getState(rle.getRAM(), radius)
        
    # contabiliza os ganhos
    R = getReward(reward, rle.game_over(), a, xn-x)
    x = xn
    total_reward += reward
    total_my_reward += R
    
    # verifica a melhor previsao de valor
    next  = getAction(state, Q, randomOrnew)
    key   = f'{stateOld},{state},{next}'
    #R2 = getReward(reward, rle.game_over(), best, xn-x)
    futureQ, t1 = Q.get(key, (0.0, 0))
    if rle.game_over():
      futureQ = 0.0

    # atualiza o valor de Q para esse estado
    Qval, t = Q.get(current_key, (0.0, 0))
    
    newQval = (1-l_rate)*Qval + (l_rate/(t+1))*(R + gamma*futureQ)
    Q[current_key] = (newQval, t+1)
    a = next
    
    it += 1
    if it > maxActions:
      maxActions = it
    
  ep += 1
  fw = open('Qsarsa.pkl', 'wb')
  pickle.dump((Q, ep, maxActions), fw)
  print(f'{ep} ({thr}, {it}): REWARD: {total_reward}, {total_my_reward} {xn}!!!!!!!!!!!!!!!!!!')
  fw.close()
  
  return total_reward


def main():
  r = train()
  time.sleep(2)
    
if __name__ == "__main__":
  main()

  
