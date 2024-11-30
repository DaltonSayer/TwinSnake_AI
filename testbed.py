from Models.Finite.QLearning import DynaQ, Qlearning, OnPolicy
from Models.pathBuilding.Astar_snake import pathfinding
from Models.pathBuilding.Hamiltonian_Cycle import cycleSnake
from Models.pathBuilding.ShortCut_Cycle import shortCycleSnake
import time
import numpy as np
from Environment import Environment

def main():
    env = Environment(rendering=True, height=10, width=20)
    #print(pathfinding(env, 1, return_score=True))
    #cycleSnake(env)
    shortCycleSnake(env, render_shortcuts=False, sleep=0)
   # q = np.loadtxt("foo.csv")
    #q = DynaQ(env, 0.2, 0.1, 0.1, 200, 1)
    # #np.savetxt("foo.csv", q)
    #q = Qlearning(env, 0.9, 0.1, 0.9, 400)
    #OnPolicy(env, q, 100)
       


def runExperiments(agent):
    grid_sizes = [[10,10], [10,20], [20,20], [20,40], [40, 50], [100, 100], [4, 20]]
    n_runs = 1
    averages = []
    for x,y in grid_sizes:
        env = Environment(rendering=False, height=x, width=y)
        scores = []
        for _ in range(n_runs):
            score = agent(env, 1, sleep=0, return_score=True)
            scores.append(score)
        averages.append([str(x)+" , "+str(y),np.average(scores)])
    return averages

#main()

print(runExperiments(shortCycleSnake))