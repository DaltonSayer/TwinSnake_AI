from snake_game import snake_game
#Give the game environment a gym-like interface
class Environment:
        def __init__(self, rendering=True, width=20, height=20):
             self.game = snake_game(width, height, rendering=rendering)
             self.n_actions = 4
             self.n_states = 2**len(self.get_state_version_1())
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
             print(state)
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