import numpy as np
import time


def EpsilonGreedy(state_action, n_actions, epsilon):
    if(np.random.random() > epsilon):
        return np.argmax(state_action)
    else:
        return np.random.randint(0, n_actions)

def Qlearning(env, gamma:float, step_size:float, epsilon:float, max_episode:int, q = None):
    #Initialize Q(s,a) ∀s∈S, ∀a∈A arbitrarily
    #env.n_states = 2^8
    #env.n_actions = 4
    try:
        (q == None)
    except:
        #q is a nparray
        pass
    else:
        q = np.random.rand(env.n_states, env.n_actions)

    for x in range(max_episode):    
        #Initialize S
        S = env.reset()
        #Loop for each step of episode
        terminated = False
        while(not terminated):
            time.sleep(0.01)
            #Choose A from S using a policy derived from Q (e-greedy)
            action = EpsilonGreedy(q[S], env.n_actions, epsilon)
            #Take action A, observe R, S'
            reward, new_state, terminated = env.step(action)
            q[S][action] = q[S][action] + step_size*(reward + gamma * np.max(q[new_state]) - q[S][action])
            #S <- S'
            S = new_state
    return q

def DynaQ(env, gamma:float, step_size:float, epsilon:float, max_episode:int, max_model_step:int, q= None):
    def PlanningUpdate(q, Model, max_model_step:int, step_size, gamma):
        #Loop repeat n times:
        for _ in range(max_model_step):
            #S <- random previously observed state
            previously_observed_states = np.unique(np.nonzero(Model)[0])
            S = previously_observed_states[np.random.randint(0,len(previously_observed_states))]
            #A <- random action previously taken in S
            previously_observed_actions = np.nonzero(Model[S])[0]
            action = previously_observed_actions[np.random.randint(0,len(previously_observed_actions))]
            #R, S' <- Model(S,A)
            R, new_state = Model[S, action]
            new_state = int(new_state)
            #Q(S, A) <- Q(S,A) + step_size[R + gamma max_a Q(S', a) - Q(S,A)]
            q[S][action] = q[S][action] + step_size*(R + gamma* np.max(q[new_state]) - q[S][action])

    Model = np.zeros((env.n_states,env.n_actions,2))
    try:
        (q == None)
    except:
        pass
    else:
        q = np.random.rand(env.n_states, env.n_actions)
    #Loop for each episode:
    for _ in range(max_episode):
        #initialize S
        S = env.reset()
        #Loop for each step of episode:
        terminated = False
        while(not terminated):
            #Chose A from S using a policy derived from Q (e.g., ∈-greedy)
            action = EpsilonGreedy(q[S], env.n_actions, epsilon)
            
            #Take action A, observe R, S'
            reward, new_state, terminated = env.step(action)
            #Q(S,A) <- Q(S,A) + step_size*[R + gamma*max_a*Q(S',a) - Q(S,A)]
            q[S][action] = q[S][action] + step_size*(reward + gamma* np.max(q[new_state]) - q[S][action])
            #Model(S,A) <- R, S' (assuming deterministic)
            Model[S][action] = [reward, new_state]
            PlanningUpdate(q, Model, max_model_step, step_size, gamma)
            S = new_state
            print(np.max(q[S]))
    return q



def OnPolicy(env, q, max_episode=1):
     for _ in range(max_episode):
          S = env.reset()
          terminated = False
          while(not terminated):
               time.sleep(0.05)
               action = np.argmax(q[S])
               reward, new_state, terminated = env.step(action)
               S = new_state


