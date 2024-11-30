from Models.pathBuilding import Hamiltonian_Cycle as hc
import time
#The cycle is certain to win but steps can be shaved off to ensure success
#can skip part of the hamilton path as long as you do not overtake the tail
#i.e., if tail is in index [4] and head is in index [7] then it is known that the body is in indexs [4,5,6] so it is safe to jump to index [8,9,...,0,1,2,3]



def between_on_path(path, index1, index2, point, dir) ->bool:
    #returns true if the point is between the path from index1 to index2 on the path moving in dir
    if(dir == 1): #moving forwards
        if(index2 > index1): #[...index1.between..index2...]
            return (point > index1 and point < index2)
        elif(index1 > index2): #[.between..index2...index1..between.]
            return (point < index2 or point > index1)
        else:#index2==index1
            return (point == index1)
    else:
        return between_on_path(path, index2, index1, point, 1)
    # else: #return between_on_path(path, index2, index1, point, 1)
    #     if(index2 > index1): #[.between..index1 ... index2 ..between.] <-
    #         return (point < index1 or point > index2)
    #     elif(index2 < index1): #[ index2 .between. index1] <-
    #         return (point > index2 and point < index1)
    #     return (point == index2)

def check_safe(path, head, tail, new, dir):
    head_index = path.index(head)
    tail_index = path.index(tail)
    new_index = path.index(new)
    return not between_on_path(path, tail_index, head_index, new_index, dir)
def path_dist(path, point1, point2, dir):
    #distance in path from point1 to point2
    
    if(dir == 1 and point2 > point1):#[point1 -> point2]
        return point2-point1
    if(dir == 1 and point1 > point2):#[-> point2 -> point1]
        return len(path) - point1 + point2
    if(point2 == point1):
        return len(path)
    return path_dist(path, point2, point1, 1)

#greedy, check if theres a move that brings you closer to the fruit
def find_shortcut(env, path:list[list[int,int]], snakelist:list[list[int,int]], fruit:list[int,int], dir):
    #find what directions to check
    head = snakelist[-1]
    if(len(snakelist) > 1):
        tail = snakelist[1]
    else:
        tail = snakelist[0]
    [fx, fy] = fruit
    [hx, hy] = head
    
    tail_index = path.index(tail)
    head_index = path.index(head)
    fruit_index = path.index(fruit)
    #want to move in the path towards the fruit
    #cannot overtake the tail 
    #all spots in the path between the head and the tail will be assumed to part of the snake
    #cannot take a shortcut that passes the apple
    #maximum shortcut length shouldn't be anything more than the distance from the head to the tail
    max_shortcut_len = path_dist(path, head_index, tail_index, dir) -(path_dist(path, head_index, fruit_index, dir)) - 2#2#((env.game.game_width * env.game.game_height) - len(snakelist))//4
    best_shortcut_len = 1
    cur = path.index(head)
    cur = (cur+dir)%len(path)
    for [i,j] in [[hx-1, hy], [hx+1, hy], [hx, hy-1], [hx, hy+1]]: #for each direction 
        if(i >= 0 and i < env.game.game_width and j >= 0 and j < env.game.game_height):
            new_index = path.index([i,j])
            if(dir == 1 and head_index < new_index): #[ head... new] ->
                shortcut_len = new_index - head_index
            elif(dir == 1 and head_index > new_index): #[ new ... head ...] ->
                shortcut_len = new_index + len(snakelist)-head_index
            elif(dir == -1 and head_index < new_index): #[ head ... new ...] <-
                shortcut_len = head_index + len(snakelist) - new_index
            else: #dir == -1 and new_index < head_index  #[new ... head ...]  <-
                shortcut_len = head_index - new_index
            #shortcut isn't too long 
            if(shortcut_len <= max_shortcut_len):
                #check if the shortcut is safe, i.e., does not end up inside the snake
                if((check_safe(path, head, tail, [i,j], dir))
                    #check if the shortcut bypasses the apple
                    and (not between_on_path(path, head_index, new_index, fruit_index, dir))
                    #shortcut is an improvement
                    and (shortcut_len > best_shortcut_len)):
                    cur = path.index([i,j])
                    best_shortcut_len = shortcut_len
    return cur
            
    
    
    # #try to skip as much of the cycle as possible and move towards the fruit
    # #try to move towards the fruit
    # if(fx < hx and hx-1 >= 0): 
    #     if(check_safe(path, head, tail, [hx-1, hy], dir)): return path.index([hx-1, hy])
    # if(fx > hx and hx+1 < env.game.game_width):
    #     if(check_safe(path, head, tail, [hx+1, hy], dir)): return path.index([hx+1, hy])
    # if(fy < hy and hy-1 >=0):
    #     if(check_safe(path, head, tail, [hx, hy-1], dir)): return path.index([hx, hy-1])
    # if(hy < fy and hy+1 < env.game.game_height):
    #     if(check_safe(path, head, tail, [hx, hy+1], dir)): return path.index([hx,hy+1])
    #no shortcuts return normal path move
    # cur = path.index(head)
    # return (cur+dir)%len(path)

def shortCycleSnake(env, max_episodes:int=10, render_shortcuts=False, sleep=0, return_score=False):
    terminated = False
    dir = 1

    for _ in range(max_episodes):
        env.reset()
        path = hc.Maze(env.game.game_width, env.game.game_height).make_path()
        fruit = env.game.apple_pos
        while not terminated:
            if(sleep > 0):
                time.sleep(sleep)
            head =env.game.snake_list[-1]
            tail =env.game.snake_list[0]
            cur = path.index(head)
            next = find_shortcut(env, path, env.game.snake_list, fruit, dir)
            if render_shortcuts:
                imaginary_snake = []
                if(len(env.game.snake_list) > 1):
                    i = path.index(env.game.snake_list[1])
                else:
                    i = path.index(tail)
                done = False
                while not done:
                    imaginary_snake.append(path[i])
                    if(i == next):
                        done = True
                    i = (i+dir)%len(path)
                env.game.GUI.imaginary_snake = imaginary_snake
            action = hc.get_action(path[cur], path[next])
            reward, new_state, terminated = env.step(action)
            if(reward):
                dir = -1*dir
                fruit = env.game.apple_pos
        if(return_score):
            return (len(env.game.snake_list)-1)