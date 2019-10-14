'''
AIM: SOLVE N-QUEENS PROBLEM USING GENETIC ALGORITHM

IMPLEMENTATION: 
A list is such that, value in list is row number in which queen is placed and its index is its column number
For example, for 4-queens
list [2,4,1,3] suggests that queens are placed as follows:
Column 1, Row 2
Column 2, Row 4
Column 3, Row 1
Column 4, Row 3



AUTHOR: DIVYA AGARWAL

Python version: 3.6.2
'''

import random
from random import randint

POPULATION_SIZE = 100
max_fitness = 0


def generate_individual(n):
        individual = []
        for i in range(n):
                #random.shuffle(individual)
            #individual.append(randint(1,n))
            individual.append(i+1)
        random.shuffle(individual)
        return individual



def determine_fitness(n, individual):
        total_clashes = 0

        #row clashes from left
        for i in range(n):
                for j in range(i):
                        #print(i,j)
                        if individual[j] == individual[i]:
                                total_clashes += 1


        #diagonal clashes from left
        for i in range(n):
                for j in range(i):
                        if (i-j) == abs(individual[i] - individual[j]):
                                total_clashes += 1

        
        global max_fitness
        #max_fitness = (n * ((n-1)/2))

        fitness = max_fitness - total_clashes

        return fitness



def generate_population(n):
        population = {}
        for i in range(POPULATION_SIZE):
                ind = generate_individual(n)
                population[tuple(ind)] = determine_fitness(n, ind)
       
        return population



def sort_population(population):
        #sort on based of value of fitness function in descending order
        population = dict(sorted(population.items(), key = lambda x : x[1], reverse = True))
        return population



def crossover(n, individual1, individual2):

        individual1 = list(individual1)
        individual2 = list(individual2)

        crossover_point = randint(2,n-2)
        #print("crossover pt: ", crossover_point,"\n")
        for i in range(crossover_point, n):
                individual1[i], individual2[i] = individual2[i], individual1[i]

        return individual1, individual2



def mutate(n, individual):

        #random index on left half
        random_index1 = randint(0, int(n/2))
        #random index on right half
        random_index2 = randint(int(n/2)+1, n-1)
        
        individual[random_index1], individual[random_index2] = individual[random_index2], individual[random_index1]

        random_index = randint(0, n-1)
        while True:
                random_number = randint(1,n)
                if individual[random_index] != random_number:
                        individual[random_index] = random_number
                        break
        
        return individual



def genetic_algorithm():
        #taking input n
        while 1:
                n = int(input("Enter value of n >= 4 : "))
                if n >= 4:
                        break
                else:
                        print("Not valid value! Enter again! \n")
        
        global max_fitness
        max_fitness = (n * ((n-1)/2))

        p = generate_population(n)

        global POPULATION_SIZE
        
        if len(p) < POPULATION_SIZE:
                POPULATION_SIZE = len(p)
                
        #p = sort_population(p)

        #ORIGINAL POPULATION
        #print("ORIGINAL POPULATION: \n",p)
        
        itr = 0
        solution_found = False
        while True:
                itr += 1
                print("Iteration: ",itr,"\n")

                #stores new generation
                new_population = {}

                p = sort_population(p)

                #one round of generating new generation
                i = 0
                while i < POPULATION_SIZE/2:
                        parent1 = list(p.keys())[i]
                        if p[parent1] == max_fitness:
                                solution = parent1
                                solution_found = True
                                break

                        parent2 = list(p.keys())[i+1]

                                
                        #print(p)

                        child1, child2 = crossover(n, parent1, parent2)

                        
                        while tuple(child1) in p:
                                child1 = mutate(n, child1)
                        while tuple(child2) in p:
                                child2 = mutate(n, child2)


                        #maintaing population size constant

                        
                        #adding 2 children to population
                        new_population[tuple(child1)] = determine_fitness(n, child1)
                        new_population[tuple(child2)] = determine_fitness(n, child2)

                        
                        #print("np: ",new_population,"\n")

                        i += 1


                new_population_len = len(new_population)
                new_population = sort_population(new_population)
                #print("len newpop: ",new_population_len,"np/2: :",new_population_len/2)

                
                i = 0
                while i < int(new_population_len/2):
                        
                        k = list(new_population.keys())
                        del new_population[k[len(k)-1]]
                       
                        i += 1
                       

                p_keys = list(p.keys())

                i = len(new_population)
                #print("i",i," p",len(p_keys))
                j = 0
                while i < POPULATION_SIZE:
                        new_population[tuple(p_keys[j])] = p[tuple(p_keys[j])]
                        j += 1
                        i += 1
                        
                #new_population.update(p)
                p = new_population
                p = sort_population(p)
                        

                if solution_found:
                        break

                
                if itr%200 == 0:
                        parent1 = p_keys[0]
                        parent2 = p_keys[1]
                        #print(p,"\n")
                        del p[tuple(parent1)]
                        parent1 = mutate(n, list(parent1))
                        
                        while tuple(parent1) in p:
                                parent1 = mutate(n, list(parent1))
                                
                        #adding mutated value
                        p[tuple(parent1)] = determine_fitness(n, parent1)


                        del p[tuple(parent2)]
                        parent2 = mutate(n, list(parent2))
                        
                        while tuple(parent2) in p:
                                parent2 = mutate(n, list(parent2))
                                
                        #adding mutated value
                        p[tuple(parent2)] = determine_fitness(n, parent2)
                        

                        
                #POPULATION IN EACH ITERATION
                #print("population size: ",len(p),"\n")                
                #print(p,"\n")
                

        print("Solution: ",solution) # ," ",p)
        



genetic_algorithm()
