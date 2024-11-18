import snake_game as sg
import numpy as np
import time

#Give the game environment a gym-like interface
class Environment:
        def __init__(self, rendering=True):
             self.game = sg.snake_game(20, 20, rendering=rendering)
             self.n_actions = 4
             self.n_states = 2**8
        def step(self, _action):
             #convert numerical actions to game movements
             match _action:
                  case 0: action = [-1,0] 
                  case 1: action = [1,0]
                  case 2: action = [0,-1]
                  case 3: action = [0,1]
                  case _: action =[0,0]
            
             reward, new_state, terminated = self.game.step(action)
             #convert state into a numerical value
             ns = self.get_state_version_1()
             state = 0
             for i in range(len(ns)):
                  state += ns[i] * (2**i)
             return reward, state, terminated 
        
        def reset(self):
             self.game.reset()
             ns = self.get_state_version_1()
             state = 0
             for i in range(len(ns)):
                  state += ns[i] * (2**i)
             return state 


        def get_state_version_1(self):
            """
            each field in the state is a boolean
            State:[
            apple left:
            apple right:
            apple up:
            apple down:
            danger left:
            danger right:
            danger up:
            danger down
            ]
            """
            snake_list = self.game.snake_list
            left_check = [snake_list[-1][0] -1, snake_list[-1][1]]
            right_check = [snake_list[-1][0] + 1, snake_list[-1][1]]
            up_check = [snake_list[-1][0], snake_list[-1][1]-1]
            down_check = [snake_list[-1][0], snake_list[-1][1]+1]

            apple_left = 1 if(snake_list[-1][0] > self.game.apple_pos[0]) else 0
            apple_right = 1 if(snake_list[-1][0] < self.game.apple_pos[0]) else 0
            apple_up = 1 if(snake_list[-1][1] < self.game.apple_pos[1]) else 0
            apple_down = 1 if(snake_list[-1][1] > self.game.apple_pos[1]) else 0

            danger_left = 1 if(self.game._out_of_bounds(left_check) or left_check in snake_list) else 0
            danger_right = 1 if(self.game._out_of_bounds(right_check) or right_check in snake_list) else 0
            danger_up = 1 if(self.game._out_of_bounds(up_check) or up_check in snake_list) else 0
            danger_down = 1 if(self.game._out_of_bounds(down_check) or down_check in snake_list) else 0

            ret = [apple_left, apple_right, apple_up, apple_down, danger_left, danger_right, danger_up, danger_down]
            return ret



def EpsilonGreedy(state_action, n_actions, epsilon):
    if(np.random.random() > epsilon):
        return np.argmax(state_action)
    else:
        return np.random.randint(0, n_actions)

def Qlearning(env, gamma:float, step_size:float, epsilon:float, max_episode:int):
    #Initialize Q(s,a) ∀s∈S, ∀a∈A arbitrarily
    #env.n_states = 2^8
    #env.n_actions = 4
    q = np.random.rand(2**8, 4)

    for x in range(max_episode):    
        print(x)
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

def DynaQ(env:Environment, gamma:float, step_size:float, epsilon:float, max_episode:int, max_model_step:int):
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
            R, S_prime = Model[S, action]
            S_prime = int(S_prime)
            #Q(S, A) <- Q(S,A) + step_size[R + gamma max_a Q(S', a) - Q(S,A)]
            q[S][action] = q[S][action] + step_size*(R + gamma* np.max(q[S_prime]) - q[S][action])

    Model = np.zeros((env.n_states,env.n_actions,2))
    #Initialize: Q(s,a) ∀s∈S, ∀a∈A arbitrarily execpt that Q(terminal, *) = 0
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


env = Environment(rendering=True)
#q = DynaQ(env, 0.9, 0.1, 0.5, 100, 10)
#np.savetxt("foo.csv", q)
q = np.loadtxt("foo.csv")
OnPolicy(env, q, 2000)