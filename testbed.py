from Models import DynaQ, Qlearning, OnPolicy
import time
import numpy as np
from Environment import Environment

def main():
    env = Environment(rendering=True, height=20, width=20)
    q = np.loadtxt("foo.csv")
    #q = DynaQ(env, 0.2, 0.1, 0.5, 200, 10)
    #np.savetxt("foo.csv", q)
    #q = Qlearning(env, 0.9, 0.1, 0.9, 200)
    OnPolicy(env, q, 100)


main()