
import sys
import time

from random import randrange
from rle_python_interface.rle_python_interface import RLEInterface
from time import sleep

from rominfo import *
from utils import *



actions_map = {'noop':0
             , 'down':32, 'up':16, 'jump':1, 'spin':3
             , 'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67
             , 'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131
             , 'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
              }

actions_list = [66,130,128,131,386]

actions_list = [130,131]

time_start = time.perf_counter()



def getTime():
  return (time.perf_counter() - time_start)

def printStats(run, reward, time):
  return None

def getRadar(rle,radius=6):
  a = getInputs(rle.getRAM(), radius)
  return np.reshape(a[0], (-1, (radius*2+1))), a[1], a[2]

def runMarioRun():
  rle = loadInterface(True)
  total_reward = 0
  total_run = 0
  while not rle.game_over():
    a = actions_list[randrange(len(actions_list))]
    reward = performAction(a, rle)
    radar = getRadar(rle,2)
    total_run = radar[1] * 100
    print(radar,a)
    total_reward += reward
  return total_run, total_reward, getTime()

def play():

  print(runMarioRun())


def main():
  play()

if __name__ == "__main__":
  main()
