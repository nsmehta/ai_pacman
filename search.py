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
import game
import sys

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


def oppositeDirection(direction):
    # from game import Directions
    s = game.Directions.SOUTH
    w = game.Directions.WEST
    n = game.Directions.NORTH
    e = game.Directions.EAST

    if direction == s:
        return n
    elif direction == w:
        return e
    elif direction == n:
        return s
    elif direction == e:
        return w
    else:
        raise Exception('Invalid direction!')


def dfsPath(problem, fringeList, exploredSet):
    if fringeList.isEmpty():
        return None

    currentState = fringeList.pop()
    currentPath = currentState[3][:]
    currentPath.append(currentState[1])
    exploredSet.add(currentState[0])

    if problem.isGoalState(currentState[0]):
        return currentPath

    counter = 0
    for successor in problem.getSuccessors(currentState[0]):
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
    """
    if problem.isGoalState(problem.getStartState()):
        return None

    exploredSet = set()
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
    if fringeList.isEmpty():
        return None

    currentState = fringeList.pop()
    currentPath = currentState[3][:]
    currentPath.append(currentState[1])
    exploredSet.add(currentState[0])

    if problem.isGoalState(currentState[0]):
        # print 'goal state reached'
        return currentPath

    for successor in problem.getSuccessors(currentState[0]):
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
    if problem.isGoalState(problem.getStartState()):
        return None

    exploredSet = set()
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
    if path is not None and len(path) > 0:
        return path
    else:
        print 'Path not found'
        util.raiseNotDefined()


def getUCSFringeList(successor, fringeList):
    queue = util.PriorityQueue()
    while not fringeList.isEmpty():
        nextElement = fringeList.pop()
        if nextElement[0] == successor[0] and nextElement[2] > successor[2]:
            queue.push(successor, successor[2])
        else:
            queue.push(nextElement, nextElement[2])
    return queue


def ucsPath(problem, fringeList, exploredSet, fringeSet):
    if fringeList.isEmpty():
        return None

    currentState = fringeList.pop()
    currentPath = currentState[3][:]
    currentPath.append(currentState[1])
    exploredSet.add(currentState[0])

    if problem.isGoalState(currentState[0]):
        return currentPath

    for successor in problem.getSuccessors(currentState[0]):
        if successor[0] not in exploredSet:
            successor = list(successor)
            successor.append(currentPath)
            successor[2] += currentState[2]
            successor = tuple(successor)
            if successor[0] not in fringeSet:
                fringeList.push(successor, successor[2])
                fringeSet.add(successor[0])
            else:
                fringeList = getUCSFringeList(successor, fringeList)


    return ucsPath(problem, fringeList, exploredSet, fringeSet)



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    if problem.isGoalState(problem.getStartState()):
        return None

    exploredSet = set()
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
    queue = util.PriorityQueue()
    while not fringeList.isEmpty():
        nextElement = fringeList.pop()
        if nextElement[0] == successor[0] and nextElement[2] > successor[2]:
            queue.push(successor, successor[4])
        else:
            queue.push(nextElement, nextElement[4])
    return queue


def astarPath(problem, heuristic, fringeList, exploredSet, fringeSet):
    if fringeList.isEmpty():
        return None

    currentState = fringeList.pop()
    currentPath = currentState[3][:]
    currentPath.append(currentState[1])
    exploredSet.add(currentState[0])

    if problem.isGoalState(currentState[0]):
        return currentPath

    for successor in problem.getSuccessors(currentState[0]):
        if successor[0] not in exploredSet:
            successor = list(successor)
            successor.append(currentPath)
            successor[2] += currentState[2]
            successor.append(successor[2] + heuristic(successor[0], problem))
            successor = tuple(successor)
            if successor[0] not in fringeSet:
                fringeList.push(successor, successor[4])
                fringeSet.add(successor[0])
            else:
                fringeList = getAStarFringeList(successor, fringeList)

    return astarPath(problem, heuristic, fringeList, exploredSet, fringeSet)


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    if problem.isGoalState(problem.getStartState()):
        return None

    exploredSet = set()
    exploredSet.add(problem.getStartState())
    fringeList = util.PriorityQueue()
    fringeSet = set()
    fringeSet.add(problem.getStartState())
    for successor in problem.getSuccessors(problem.getStartState()):
        successor = list(successor)
        successor.append(list())
        successor.append(successor[2] + heuristic(successor[0], problem))
        successor = tuple(successor)
        if successor[0] not in fringeSet:
            fringeList.push(successor, successor[4])
            fringeSet.add(successor[0])
        else:
            fringeList = getAStarFringeList(successor, fringeList)

    path = astarPath(problem, heuristic, fringeList, exploredSet, fringeSet)
    if len(path) > 0:
        return path
    else:
        print 'Path not found'


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
