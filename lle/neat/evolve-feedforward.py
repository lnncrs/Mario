from __future__ import print_function

import sys
import time
import random, string

import os
import neat
import visualize

from random import randrange
from rle_python_interface.rle_python_interface import RLEInterface
from time import sleep

from rominfo import *
from utils import *

runs_per_net = 5

actions_map = {'noop':0
              ,'down':32, 'up':16, 'jump':1, 'spin':3
              ,'left':64, 'jumpleft':65, 'runleft':66, 'runjumpleft':67
              ,'right':128, 'jumpright':129, 'runright':130, 'runjumpright':131
              ,'spin':256, 'spinright':384, 'runspinright':386, 'spinleft':320, 'spinrunleft':322
              }

#actions_list = [66,130,128,131,386]
actions_list = [130,131]
#actions_list = [1,1,386,1,1,1,1,386,386,386,386,386,386,131,386,386,386,1,1,386,131,1,1,386,386]



def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)



# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    rle = loadInterface(True)

    apperture = 3
    distance = 0
    bonus = 0
    fitness = 0

    while not rle.game_over():

      radar = getRadar(rle,apperture)
      inputs = radar[0],radar[1]
      action = net.activate(inputs)
      reward = performAction(action, rle)
      radar = getRadar(rle,apperture)
      total_run = radar[1] * 100 + reward
      fitness += fitness

    if rle.game_over:
        fitness = -1000

    '''
    for runs in range(runs_per_net):

        rle = loadInterface(True)
        apperture = 3
        distance = 0
        bonus = 0

        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        while sim.t < simulation_seconds:
            inputs = sim.get_scaled_state()
            action = net.activate(inputs)

            # Apply action to the simulated cart-pole
            force = cart_pole.discrete_actuator_force(action)
            sim.step(force)

            # Stop if the network fails to keep the cart within the position or angle limits.
            # The per-run fitness is the number of time steps the network can balance the pole
            # without exceeding these limits.
            if abs(sim.x) >= sim.position_limit or abs(sim.theta) >= sim.angle_limit_radians:
                break

            fitness = sim.t

        fitnesses.append(fitness)
    '''

    # The genome's fitness is its worst performance across all runs.
    return fitness



def getRadar(rle,radius=6):
  a = getInputs(rle.getRAM(), radius)
  return np.reshape(a[0], (-1, (radius*2+1))), a[1], a[2]



def runMarioRun():
  rle = loadInterface(True)

  apperture = 3
  distance = 0
  bonus = 0

  start = getRadar(rle,apperture)[1]
  a = actions_list[randrange(len(actions_list))]
  bonus = performAction(a, rle)
  radar = getRadar(rle,apperture)

  fitness = ((radar[1] - start)*100)+bonus

  if rle.game_over():
      fitness = -1000

  return fitness



def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    '''
    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)
    '''

def play():
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)

def main():
  play()

if __name__ == "__main__":
  main()
