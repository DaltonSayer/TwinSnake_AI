import numpy as np
import random
from Models.Finite.QLearning import EpsilonGreedy

def greedyPolicy(x, W):
    action_value = W @ x
    action = np.argmax(action_value)
    return action 



def QLearningFA(env, W=None, gamma=0.99, step_size=0.005, epsilon=0.5, max_episodes=4000):
    view_size = 10
    try:
        (W == None)
    except:
        pass
    else:
        W = np.random.rand(4, view_size*view_size)    
    
    for i in range(1, max_episodes + 1):
        _ = env.reset()
        state = env.featurize(view_size=view_size)
        terminated = False
        while not terminated:
            if(random.uniform(0,1) > epsilon):
                action = greedyPolicy(state, W)
            else:
                action = random.randint(0, 3)
            reward, _, terminated = env.step(action)

            new_state = env.featurize(view_size=view_size)
            error_term = reward + (gamma * np.max(W @ new_state)) - (W @ state)[action]
            W[action] = W[action] + step_size * error_term * state
            state = new_state
    print(W)

#using simpler q_learning to train
def QLearningFA_traning(env, q=None, gamma=0.99, step_size=0.005, epsilon=0.1, max_episodes=400):
    try:
        (q == None)
    except:    
        pass
    else:
        q = np.random.rand(env.n_states, env.n_actions)
    
    view_size = 20
    W = np.random.rand(4, view_size*view_size)
    for i in range(1, max_episodes + 1):
        q_state = env.reset()
        state = env.featurize(view_size=view_size)
        terminated = False
        while not terminated:
            action = np.argmax(q[q_state])
            reward, q_state, terminated = env.step(action)

            new_state = env.featurize(view_size=view_size)
            error_term = reward + (gamma * np.max(W @ new_state)) - (W @ state)[action]
            W[action] = W[action] + step_size * error_term * state
            state = new_state
        if(i%20 == 0):
            print(i)
    return(W)
