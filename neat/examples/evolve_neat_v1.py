# -*- coding: utf-8 -*-
"""
Created on Mon May  7 09:10:21 2018

@author: ufabc
"""

import neat

actions_map = {'noop':0
             , 'down':32, 'up':16, 'jump':1, 'spin':3
             , 'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67
             , 'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131
             , 'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
              }

def control(self, state_input,net):

    # retorna o resultado de saida da rede neural em forma de uma lista para a variavel output
    output = net.activate(state_input)

    # toma as decisoes de acao para o sprite do jogador
    if output[0] > 0.5:
        left = 1
    else:
        left = 0

    if output[1] > 0.5:
        right = 1
    else:
        right = 0

    if output[2] > 0.5:
        jump = 1
    else:
        jump = 0
        
    if output[3] > 0.5:
        down = 1
    else:
        down = 0    

    # dado como retorno uma lista de boleanos indicando as acoes para o sprite do jogador
    return [left, right, jump, down]
            

def getTime():
  return (time.perf_counter() - time_start)

def printStats(run, reward, time):
  return None

def getRadar(rle,radius=6):
  a = getInputs(rle.getRAM(), radius)
  return np.reshape(a[0], (-1, (radius*2+1))), a[1], a[2]
              


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                     config_file)


actions_list = [66,130,128,131,386]
actions_list = [130,131]

time_start = time.perf_counter()

def runMarioRun(genome):      
  # recebe o objeto do tipo net para ser avaliado
  net = neat.nn.FeedForwardNetwork.create(genome, config)
    
  rle = loadInterface(True)
  total_reward = 0
  total_run = 0
  while not rle.game_over():
    
    actions = control(state_input, net)
    #a = actions_list[randrange(len(actions_list))]
    
    reward = performAction(actions, rle)
    total_run = getRadar(rle,2)[1] * 100
    total_reward += reward
  
  return total_run, total_reward, getTime()
  

def play():
    
  genomeFile = '/home/roshan/Documents/mario_neat/bestGenomes/2_732.p'
  genome = pickle.load(open(genomeFile,'rb'))
    
  print(runMarioRun(genome))


