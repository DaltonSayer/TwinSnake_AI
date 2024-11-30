from Models.Finite.QLearning import DynaQ, Qlearning, OnPolicy
from Models.Continuous.QLearningFA import QLearningFA, QLearningFA_traning
from Models.pathBuilding.Astar_snake import pathfinding
from Models.pathBuilding.Hamiltonian_Cycle import cycleSnake
from Models.pathBuilding.ShortCut_Cycle import shortCycleSnake
import time
import numpy as np
from Environment import Environment

def main():
    env = Environment(rendering=True, height=20, width=20)
    #pathfinding(env, 1)
    #cycleSnake(env)
    #shortCycleSnake(env, render_shortcuts=True, sleep=0.01)
   # q = np.loadtxt("foo.csv")
    q = DynaQ(env, 0.2, 0.1, 0.1, 200, 1)
    # #np.savetxt("foo.csv", q)
     #q = Qlearning(env, 0.9, 0.1, 0.9, 200)
    OnPolicy(env, q, 100)
       

main()