# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))    
    """
    "*** YOUR CODE HERE ***"
    # For all of my implementations for this searh problems, I am going to be making use of the
    # generic search problem provided in class
    # Node state stack
    NSS = util.Stack()
    start = problem.getStartState()

    # Take the node located in the start variable and push onto the 
    # the stack as a tuple of (state, path) where path is the list of actions taken to reach that state
    # Node State Stack
    NSS.push((start, []))

    # A set makes the search much faster by allowing us to check if a state has been visited in O(1) time, instead of O(n) time if we were to use a list
    visited = set()

    while not NSS.isEmpty():
        # we begin by popping the top node from the stack, which gives us the current state and the path taken to reach that state
        current_state, path = NSS.pop()
       
        #check if we have the goal state at current state, then we return path
        if problem.isGoalState(current_state):
            return path
        # o/W if current state is in visited, meaning that we have already explore all the nodes in here
        # then we skip the current state and continue to pop the next node in the stack
        if current_state in visited:
            continue
        # we need to get the succesor from the current state that has being currently counted as visited
        # for each successor, we check if the successor is not in visited, meaning that we have not explore the successor yet, then we push the successor onto the stack as a tuple of (successor, path + [action]) where path + [action] is the list of actions taken to reach the successor
        successors = problem.getSuccessors(current_state)
        # we have to look for each succesor in the list
        for s in successors:
            # s[0] contains the succesor and s[1] contains the action
            if s[0] not in visited:
                NSS.push((s[0], path + [s[1]]))

        # We need to make sure we add the current state to the visited 
        visited.add(current_state)

    # No solution found
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # the implementation is similar to DFS, however we are going to be using queue since the BFS implementation is last in first out
    # meaning that the first node that we push onto the queue will be the first node that we pop from the queue, and we are going to 
    # be exploring the shallowest nodes in the search tree first, meaning that we are going to be exploring all the nodes at the current 
    # depth before we move on to the next depth level  
    #Node State Queue
    """      
             A
            / \  
           B   C    
          / \  |    
         D   E F    
    """
    #Load the queue with the start state, and an empty path
    # in this queue for the example is A
    # Contents at the top of the queue: (A, [])
    NSQ = util.Queue()
    start = problem.getStartState()
    NSQ.push((start, []))

    # Need to keep tracj of visited states to avoid cycles and redundant paths, 
    # we can use a set for this purpose since it allows us to check if a state has been visited in O(1) time
    visited = set()

    while not NSQ.isEmpty():
        # example visual run
        # Contents at the top of the queue: (A, [])
        # we pop the top node from the queue, which gives us the current state and the
        # path taken to reach that state
        current_state, path = NSQ.pop()

        # the current state is not the goal
        if problem.isGoalState(current_state):
            return path
        # item is not in visited since is the first time we see it and we have not explore any of its successors yet, so we add the current state to the visited set, and we get all the successors of the current state by calling problem.getSuccessors(current_state)
        if current_state in visited:
            continue
        # or also call children of the current state, and for each successor
        # we check if the successor is not in visited, meaning that we have not explore the successor yet
        # then we push the successor onto the queue as a tuple of (successor, path + [action]) where path + [action] 
        # is the list of actions taken to reach the successor
        successors = problem.getSuccessors(current_state)
        for s in successors:
                # s[0] contains the successor and s[1] contains the action
                NSQ.push((s[0], path + [s[1]]))

        #Add items to visited set and get the successors of the current state
        visited.add(current_state)

    return []



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #Node State Queue Priority
    # This implementation similar to 
    NSQP = util.PriorityQueue()

    start = problem.getStartState()
    # push tuple (state, path, cost) with priority = cost
    NSQP.push((start, [], 0), 0)
    # best cost seen so far for each state 
    best_cost = {}

    while not NSQP.isEmpty():
        # cost is the current one since we started from the start state and we have to keep track of the cost for each successor 
        current_state, current_path, current_cost = NSQP.pop()

        # added this since I was loosing points due to repetition of states, and I was not able to get the correct cost for each state, 
        # since I was not keeping track of the best cost for each state, and I was not able to update the cost for each state when I found a better cost, 
        # so I added this check to skip the current state if we have already seen a better cost for it
        if current_state in best_cost:
            continue
        
        if problem.isGoalState(current_state):
            return current_path
        
        successors = problem.getSuccessors(current_state)
        
        for s in successors:
            new_cost = current_cost + s[2] # s[2] is the step cost to reach the successor
            # s[1] is the action to reach the successor and s[0] is the successor state
            # need to make use of infinity expression since we every unvisted node at this time is supposed
            # to be greater than every other node 
            if new_cost < best_cost.get(s[0], float("inf")):
                NSQP.push((s[0], current_path + [s[1]], new_cost), new_cost)

        best_cost[current_state] = current_cost
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # f(n) = g(n) + h(n)
    # Node stack Queue priority
    NSQP = util.PriorityQueue()
    startingState = problem.getStartState()

    # we need to have variables for state, path and cost
    gn = 0
    fn = gn + heuristic(startingState, problem)
    NSQP.push((startingState, [], gn), fn)


    # this at some point behaves just like a uniform cost search
    # since we can have the heuristic function return 0 for all states, then we will have f(n) = g(n) + 0 = g(n)
    best_cost = {}
    while not NSQP.isEmpty():
        current_state, current_path, updatedGN = NSQP.pop()

        if problem.isGoalState(current_state):
            return current_path
        
        successors = problem.getSuccessors(current_state)

        for s in successors:
            # Current cost from start state to successor s
            new_gn = updatedGN + s[2] # s[2] is the step cost to reach the successor
            # Estimated total cost from start to goal through successor s
            if new_gn < best_cost.get(s[0], 1000000):
                # Update best cost for successor s
                best_cost[s[0]] = new_gn
                new_fn = new_gn + heuristic(s[0], problem)
                NSQP.push((s[0], current_path + [s[1]], new_gn), new_fn)

        best_cost[current_state] = updatedGN
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
