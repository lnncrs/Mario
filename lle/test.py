
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

def time_elapsed():
  return (time.perf_counter() - time_start)

def test_actions(rle):
  for akey, avalue in actions_map.items():
    print('{0}/{1}'.format(akey,avalue))
    reward = rle.act(avalue)
    print(reward)

def getStats(run, reward, time):
  print('total {}, run {}, reward {}, time {}'.format(run+reward, run, reward, time))

def getRadar(rle,radius=6):
  a = getInputs(rle.getRAM(), radius)
  return np.reshape(a[0], (-1, (radius*2+1))), a[1], a[2]

def play():
  rle = loadInterface(True)

  total_reward = 0
  total_run = 0

  #limit = 10000
  #tick = 0
  #tack = 10
  #idx = 0

  #act = { 160:1, 500:130, 520:130, 540:130, 550:130 }

  #performAction(0, rle)

  while not rle.game_over():

    #test_getradar(rle,6)
    #test_actions(rle)
    #break
    a = actions_list[randrange(len(actions_list))]
    # Apply an action and get the resulting reward
    #reward = rle.act(a)
    reward = performAction(a, rle)
    total_run = getRadar(rle,2)[1] * 100
    print(getRadar(rle,2))
    #print(reward)
    total_reward += reward

  getStats(total_run, total_reward, time_elapsed())
  #rle.reset_game()

  '''
  while tick <= limit:

    #rle.act(0)

    if tick % tack == 0:
      #print(time.process_time())
      #print(time_elapsed())
      print(tick)
      #sleep(0.0001)
      rle.act(0)

    if rle.game_over():
      break

    #if tick % tack == 0:
    #if act.get(tick,-1) != -1:
      #reward = rle.act(act[tick])
      #print(tick)
    #else:
      #if act.get(tick,-1) != -1:
        #reward = rle.act(act[tick])
        #print(tick)

    if tick % tack == 0:
      if act.get(tick,-1) != -1:
        reward = rle.act(act[tick])
        #print(idx)
        idx+=1
      else:
        rle.act(0)

    #reward = rle.act(0)
    tick+=1
  '''



def main():
  play()

if __name__ == "__main__":
  main()
