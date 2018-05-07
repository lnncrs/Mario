# -*- coding: utf-8 -*-
"""
Created on Mon May  7 07:23:47 2018

@author: ufabc
"""

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.RecurrentNetwork.create(genome, config)
####################### Interface com o jogo #################################
        #genome.fitness = simula(env, net)
        genome.fitness = runMarioRun(genome)

def eval_genomes(genomes, config):
	i = 0
	global SCORE
	global GENERATION, MAX_FITNESS, BEST_GENOME

	GENERATION += 1
	for genome_id, genome in genomes:

           #genome.fitness = game(genome, config)
		genome.fitness = runMarioRun(genome)
		print("Gen : %d Genome # : %d  Fitness : %f Max Fitness : %f"%(GENERATION,i,genome.fitness, MAX_FITNESS))
		if genome.fitness >= MAX_FITNESS:
			MAX_FITNESS = genome.fitness
			BEST_GENOME = genome
		SCORE = 0
i+=1

def treinamento():
    # carrega o arquivo de configuracao realizando os "parsers" necessarios para coletar as configuracoes.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                         config_file)

    # Cria uma populacao de genomas baseadas nas configuracoes setadas no arquivo
    p = neat.Population(config)

    # Executa N vezes o metodo de avaliação/seleção de fitness para toda a populacao 
    # parametro 1 passa-se o metodo o segundo a quantidade de geracoes em que sera executada. 
    winner = p.run(eval_genomes, 100)
    # Mostra qual o genoma obteve o maior fitness dentre as N execucoes de avaliacao 
    #e ou o melhor genoma que atingiu o valor igual ou superior ou desejado e determinado no arquivo de configuracao.
    print('\nBest genome:\n{!s}'.format(winner))

    outputDir = '/home/roshan/Documents/FlappyBird/bestGenomes'
    os.chdir(outputDir)
    serialNo = len(os.listdir(outputDir))+1
    outputFile = open(str(serialNo)+'_'+str(int(MAX_FITNESS))+'.p','wb' )

    pickle.dump(winner, outputFile)
    
    
    
