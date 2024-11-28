import numpy as np

def runExperiments(env, model):
    def repeatExperiments(gamma=gamma,
                            step_size=step_size,
                            epsilon=epsilon,
                            max_episode=max_episode):
        #train agent with model
        q = model(env, gamma, step_size, epsilon, max_episode)
        #run agent n_run times
        scores = []
        for _ in range(n_runs):
            score = OnPolicy(env, q)
            scores.append(score)
        #return average score
        return np.average(scores)
    
    n_runs = 10
    
     