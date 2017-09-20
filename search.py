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


def dfsPath(problem, fringeList, exploredSet):
    """
    Recursive dfs call to find path
    :param problem: problem state
    :param fringeList: open list
    :param exploredSet: closed list
    :return:
    """

    if fringeList.isEmpty():
        return None

    """
    state is ((x,y), action, cost, path)
    Get the next state from fringe list and add it to the explored set and explore its successors.
    """
    currentState = fringeList.pop()
    currentPath = currentState[3][:]
    currentPath.append(currentState[1])
    exploredSet.add(currentState[0])

    if problem.isGoalState(currentState[0]):
        return currentPath

    counter = 0
    for successor in problem.getSuccessors(currentState[0]):
        """
        If the successor is not explored, append the path and put it in the fringe list
        """
        if successor[0] not in exploredSet:
            counter += 1
            successor = list(successor)
            successor.append(currentPath)
            successor = tuple(successor)
            fringeList.push(successor)

    return dfsPath(problem, fringeList, exploredSet)


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    :param problem: problem state
    :return: path
    """
    if problem.isGoalState(problem.getStartState()):
        return None

    exploredSet = set() # Maintains a list of explored nodes
    """
    Add the start state to the explored set and explore its successors
    """
    exploredSet.add(problem.getStartState())
    fringeList = util.Stack()
    for successor in problem.getSuccessors(problem.getStartState()):
        successor = list(successor)
        successor.append(list())
        successor = tuple(successor)
        fringeList.push(successor)

    path = dfsPath(problem, fringeList, exploredSet)
    if len(path) > 0:
        return path
    else:
        print 'Path not found'


def bfsPath(problem, fringeList, exploredSet, fringeSet):
    """
    Recursive bfs call to find the path
    :param problem: problem state
    :param fringeList: open list
    :param exploredSet: closed list
    :param fringeSet: set of nodes in the fringe list
    :return:
    """

    if fringeList.isEmpty():
        return None

    """
    state is ((x,y), action, cost, path)
    Get the next state from fringe list and add it to the explored set and explore its successors.
    """
    currentState = fringeList.pop()
    currentPath = currentState[-1][:]
    currentPath.append(currentState[1])
    exploredSet.add(currentState[0])

    if problem.isGoalState(currentState[0]):
        return currentPath

    for successor in problem.getSuccessors(currentState[0]):
        """
        If the successor is not explored, and not in the open list, append the path and put it in the fringe list
        """
        if successor[0] not in exploredSet and successor[0] not in fringeSet:
            successor = list(successor)
            successor.append(currentPath)
            successor[2] += currentState[2]
            successor = tuple(successor)
            fringeList.push(successor)
            fringeSet.add(successor[0])

    return bfsPath(problem, fringeList, exploredSet, fringeSet)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    """
    Original start state of the problem is stored in the originalStartState variable.
    If there are no more goals left to be explored, the start state is reverted back to this state.
    This is used as a stop condition in this implementation.
    Path is calculated until start state is equal to the original start state.
    """
    if problem.isGoalState(problem.getStartState()):
        return None

    originalStartState = problem.getStartState()
    exploredSet = set()
    """
    Add the start state to the explored set(closed list) and fringe set(open list) and explore its successors
    """
    exploredSet.add(problem.getStartState())
    fringeList = util.Queue()
    fringeSet = set()
    fringeSet.add(problem.getStartState())
    for successor in problem.getSuccessors(problem.getStartState()):
        if successor[0] not in fringeSet:
            successor = list(successor)
            successor.append(list())
            successor = tuple(successor)
            fringeList.push(successor)
            fringeSet.add(successor[0])

    path = bfsPath(problem, fringeList, exploredSet, fringeSet)

    """
    Continues finding path until original start state is not equal to the problem's start state.
    """
    while originalStartState != problem.getStartState():
        if problem.isGoalState(problem.getStartState()):
            return None

        exploredSet = set()
        """
        Add the start state to the explored set(closed list) and fringe set(open list) and explore its successors
        """
        exploredSet.add(problem.getStartState())
        fringeList = util.Queue()
        fringeSet = set()
        fringeSet.add(problem.getStartState())
        for successor in problem.getSuccessors(problem.getStartState()):
            if successor[0] not in fringeSet:
                successor = list(successor)
                successor.append(list())
                successor = tuple(successor)
                fringeList.push(successor)
                fringeSet.add(successor[0])
        tempPath = bfsPath(problem, fringeList, exploredSet, fringeSet)
        if tempPath is not None and len(tempPath) > 0:
            path += tempPath

    if path is not None and len(path) > 0:
        return path
    else:
        print 'Path not found'


def getUCSFringeList(successor, fringeList):
    """
    Refreshes the priority queue's elements based on the new cost of the element
    :param successor: element with new cost
    :param fringeList: priority queue
    :return: queue with the element with lower cost in it
    """
    queue = util.PriorityQueue()
    while not fringeList.isEmpty():
        nextElement = fringeList.pop()
        if nextElement[0] == successor[0] and nextElement[2] > successor[2]:
            queue.push(successor, successor[2])
        else:
            queue.push(nextElement, nextElement[2])
    return queue


def ucsPath(problem, fringeList, exploredSet, fringeSet):
    """
    Recursively finds the path using f(n) = g(n)
    :param problem: original problem
    :param fringeList: list of items to be explored
    :param exploredSet: list of explored items
    :param fringeSet: open list
    :return: path
    """
    if fringeList.isEmpty():
        return None

    currentState = fringeList.pop()
    currentPath = currentState[3][:]
    currentPath.append(currentState[1])
    exploredSet.add(currentState[0])

    if problem.isGoalState(currentState[0]):
        return currentPath

    for successor in problem.getSuccessors(currentState[0]):
        """
        If the successor is not explored, append current path to its path
        """
        if successor[0] not in exploredSet:
            successor = list(successor)
            successor.append(currentPath)
            successor[2] += currentState[2]
            successor = tuple(successor)

            """
            If successor is not in the open list, add it to the open list else replace it with the lower cost element
            """
            if successor[0] not in fringeSet:
                fringeList.push(successor, successor[2])
                fringeSet.add(successor[0])
            else:
                fringeList = getUCSFringeList(successor, fringeList)


    return ucsPath(problem, fringeList, exploredSet, fringeSet)


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    :param problem: problem state
    :return: path
    """
    if problem.isGoalState(problem.getStartState()):
        return None

    exploredSet = set()
    """
    Add the start state to the explored set(closed list) and fringe set(open list) and explore its successors
    """
    exploredSet.add(problem.getStartState())
    fringeList = util.PriorityQueue()
    fringeSet = set()
    fringeSet.add(problem.getStartState())
    for successor in problem.getSuccessors(problem.getStartState()):
        successor = list(successor)
        successor.append(list())
        successor = tuple(successor)
        if successor[0] not in fringeSet:
            fringeList.push(successor, successor[2])
            fringeSet.add(successor[0])
        else:
            fringeList = getUCSFringeList(successor, fringeList)

    path = ucsPath(problem, fringeList, exploredSet, fringeSet)
    if len(path) > 0:
        return path
    else:
        print 'Path not found'

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def getAStarFringeList(successor, fringeList):
    """
    Refreshes the priority queue's elements based on the new cost of the element
    :param successor: element with new cost
    :param fringeList: priority queue
    :return: queue with the element with lower cost in it
    """
    queue = util.PriorityQueue()
    while not fringeList.isEmpty():
        nextElement = fringeList.pop()
        if nextElement[0] == successor[0] and nextElement[2] > successor[2]:
            queue.push(successor, successor[4])
        else:
            queue.push(nextElement, nextElement[4])
    return queue


def aStarPath(problem, heuristic=nullHeuristic):
    """
    Non recursive approach of the A-Star
    :param problem: problem state
    :param heuristic: default is set to nullHeuristic
    :return: path
    """
    if problem.isGoalState(problem.getStartState()):
        return None

    exploredSet = set()
    """
    Add the start state to the explored set(closed list) and fringe set(open list) and explore its successors
    """
    exploredSet.add(problem.getStartState())
    fringeList = util.PriorityQueue()
    fringeSet = set()
    fringeSet.add(problem.getStartState())

    for successor in problem.getSuccessors(problem.getStartState()):
        successor = list(successor)
        successor.append(list())
        successor.append(successor[2] + heuristic(successor[0], problem))
        successor = tuple(successor)
        """
        If successor is not in the open list, add it to the open list else replace it with the lower cost element
        """
        if successor[0] not in fringeSet:
            fringeList.push(successor, successor[4])
            fringeSet.add(successor[0])
        else:
            fringeList = getAStarFringeList(successor, fringeList)


    while not fringeList.isEmpty():
        currentState = fringeList.pop()
        currentPath = currentState[3][:]
        currentPath.append(currentState[1])
        exploredSet.add(currentState[0])

        if problem.isGoalState(currentState[0]):
            return currentPath

        for successor in problem.getSuccessors(currentState[0]):
            """
            If the successor is not explored, append current path to its path
            """
            if successor[0] not in exploredSet:
                successor = list(successor)
                successor.append(currentPath)
                successor[2] += currentState[2]
                successor.append(successor[2] + heuristic(successor[0], problem))
                successor = tuple(successor)
                """
                If successor is not in the open list, add it to the open list else replace it with the lower cost element
                """
                if successor[0] not in fringeSet:
                    fringeList.push(successor, successor[4])
                    fringeSet.add(successor[0])
                else:
                    fringeList = getAStarFringeList(successor, fringeList)


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    Finds path until originalStartState is not equal to the problem's start state
    :param problem: problem state
    :param heuristic: nullHeuristic by default
    :return: path
    """
    originalStartState = problem.getStartState()
    path = aStarPath(problem, heuristic)
    while originalStartState != problem.getStartState():
        path += aStarPath(problem, heuristic)
    if len(path) > 0:
        return path
    else:
        print 'Path not found'
        return ""


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
