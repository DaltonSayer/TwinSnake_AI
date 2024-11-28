from Models.Finite.QLearning import DynaQ, Qlearning, OnPolicy
from Models.Continuous.QLearningFA import QLearningFA, QLearningFA_traning
from Models.Astar_snake import pathfinding
from Models.Hamiltonian_Cycle import cycle_snake
import time
import numpy as np
from Environment import Environment

def main():
    env = Environment(rendering=True, height=40, width=40)
    #pathfinding(env, 1)
    cycle_snake(env)
    #q = np.loadtxt("foo.csv")
    #q = DynaQ(env, 0.2, 0.1, 0.5, 400, 20)
    # #np.savetxt("foo.csv", q)
    # #q = Qlearning(env, 0.9, 0.1, 0.9, 200)
    # OnPolicy(env, q, 100)
       

main()