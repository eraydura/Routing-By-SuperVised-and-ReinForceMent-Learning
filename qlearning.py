import numpy as np

gamma = 0.75
alpha = 0.9

#Defining states
states = { '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8}

#Defining reward array
reward = np.array([
              [0,1,0,0,0,0,0,1,0],
              [1,0,1,0,0,0,0,1,0],
              [0,1,0,1,0,1,0,0,1],
              [0,0,1,0,1,1,0,0,0],
              [0,0,0,1,0,1,0,0,0],
              [0,0,1,1,1,0,1,0,0],
              [0,0,0,0,0,1,0,1,1],
              [1,1,0,0,0,0,1,0,1],
              [0,0,1,0,0,0,1,1,0]
              ])


def optimal_paths(start, end):
    state = {state: location for location, state in states.items()}
    reward_new = np.copy(reward)
    endstate = states[end]
    #define the maximum reward state
    reward_new[endstate, endstate] = 9999
    #initialize Q -Value as a Numpy
    Q = np.array(np.zeros([9,9]))

    for i in range(9999):
        #random state set from our possible states
        current = np.random.randint(0,9)
        actions = []
        for j in range(9):
            if reward_new[current, j] > 0:
                actions.append(j)
        #arbitrary action at that can lead to the next possible state
        next = np.random.choice(actions)
        #We compute the temporal difference (T.D):
        Qt = Q[next, np.argmax(Q[next,])] - Q[current, next]
        TD = reward_new[current, next] + gamma * Qt
        #We update the Q-value applying the Bellman equation:
        Q[current, next] = Q[current, next] + alpha * TD

    route = [start]
    nextstate = start

    while (nextstate != end):
        #Q value for the maximum argument in the array
        nextstate = state[np.argmax(Q[states[start],])]
        #appended to the route list
        route.append(nextstate)
        start = nextstate

    return route


#Print all optimal paths
route_start = 0
def alloptimalroute():
    global route_start
    for i in range(route_start,9):
        if i!=route_start:
           print("Optimal route between "+ str(route_start) + " and " +str(i)+" "+ str(optimal_paths(str(route_start), str(i))))
    if route_start<8:
        route_start += 1
        alloptimalroute()

alloptimalroute()