#Treat The game of snake as a maze solving problem from the head of the snake to the apple, with the border walls, and snake body as obsticals 
#doesn't deal with the snake shrinking
import numpy as np
import copy
import random
import time
DEBUG_PRINTING=True


class State_Graph:
    def __init__(self, snake_list, shape: tuple[int,int]):
        self.snake_list = copy.deepcopy(snake_list)
        self.shape = shape
        #self.graph = graph
    def copy(self):
        return State_Graph(self.snake_list, self.shape)
    #update snake_list
    def update_snake(self, index):
        self.snake_list.pop(0)
        self.snake_list.append(index)

class State_Node:
    def __init__(self, index, weight, heuristic, graph:State_Graph, parent=None):
        self.index = index
        self.weight = weight
        self.heuristic = heuristic
        self.parent = parent
        self.graph = graph
    def __eq__(self, value:object) -> bool:
        if(value.index == self.index):
            return True
        return False

def getWeight(n: State_Node):
    return n.weight + n.heuristic

def create_node(index : tuple[int, int], goal_index: tuple[int,int], graph, weight=0, parent=None) -> State_Node:
    heuristic = abs(goal_index[0]-index[0]) + abs(goal_index[1] - index[1])
    g = graph.copy()
    g.update_snake(index) #need to update the snake
    return State_Node(index=index, weight=weight, heuristic=heuristic, graph=g, parent=parent)



def neighbourhood(node : State_Node, goal_index : tuple[int,int]) -> list[State_Node]:
    cols, rows = node.graph.shape
    y, x = node.index
    ret = []
    for (i,j) in [(y+1, x),(y-1,x), (y,x-1), (y,x+1)]:
        if(i >= 0 and j >= 0 and i < cols and j < rows): #bounds checking    
            if([i,j] not in node.graph.snake_list):
                weight = node.weight + 1
                ret.append(create_node((i,j), goal_index, node.graph, weight, node))
    return ret

def get_path(node : State_Node):
    cursor = node
    arr = []
    while True:
        if (type(cursor) != State_Node):
            break
        else:
            arr.append(cursor.index)
            cursor = cursor.parent
    arr2 = []
    for _ in range(len(arr)):
        arr2.append(arr.pop())
    ret = []
    for i in range(1, len(arr2)):
        ret.append(get_action(arr2[i-1], arr2[i]))
    return ret

def get_action(state1, state2):
    if(state1[0] - 1 == state2[0]): return 0
    if(state1[0] + 1 == state2[0]): return 1
    if(state1[1] - 1 == state2[1]): return 2
    if(state1[1] + 1 == state2[1]): return 3
    print("BAD")
    return 1
            

#return the next set of actions to get to the next apple
#protect tail will reject any paths that do not let the tail reach a % of tiles at the end of the path
def search_for_actions(graph, start_index, goal_index):
    frontier = [create_node(start_index, goal_index, graph)]
    explored = []
    while True:
        if frontier == []:
            if DEBUG_PRINTING:print("PATH NOT FOUND")
#            time.sleep(1000)
            #There's no way out, the snake is doomed
            return [random.randint(0, 3)]
        frontier.sort(reverse=True, key=getWeight)
        leaf = frontier.pop()
        if (leaf.index[0] == goal_index[0] and leaf.index[1] == goal_index[1]): #if the leaf is the apple
            if DEBUG_PRINTING: print("PATH FOUND")
            
            path = get_path(leaf)
            return path
        explored.append(leaf)
        for node in neighbourhood(leaf, goal_index):
            if(node in frontier):
                if(frontier[frontier.index(node)].weight > node.weight):
                    frontier.remove(node)
                    frontier.append(node)
            elif(node not in explored):
                frontier.append(node)


# def get_action(node: State_Node):
#     child = node
#     parent = node.parent
#     while True:
#         if(type(parent.parent) != State_Node):
#             break
#         else:
#             child = parent
#             parent = parent.parent
#     if(parent.index[0] - 1 == child.index[0]): return 0
#     if(parent.index[0] + 1 == child.index[0]): return 1
#     if(parent.index[1] - 1 == child.index[1]): return 2
#     if(parent.index[1] + 1 == child.index [1]): return 3
#     return np.random.randint(0,3)



def pathfinding(env, max_episode:int, sleep=0):
    terminated = False
    env.reset()
    for x in range(max_episode):
        actions = []
        while not terminated:
            if(sleep > 0):
                time.sleep(sleep)
            head_index = env.game.snake_list[-1]
            fruit_index = env.game.apple_pos
            graph = State_Graph(env.game.snake_list, [env.game.game_width, env.game.game_height])
            if (actions == []):
                actions = search_for_actions(graph, head_index, fruit_index)
            action = actions.pop(0)

            # path = get_path(G_node)
            # action = get_action(path)
            reward, new_state, terminated = env.step(action)
    