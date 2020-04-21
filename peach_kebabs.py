# myTeam.py
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


# Artificial Intelligence - CS 4365 at UT Dallas
# Nisarg Desai - npd160030
# Sanketh Reddy


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
import operator

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'ReflexAgent', second = 'ReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]



class MyAgentData:
  
  def __init__(amRed):
    pass


class SearchState:
  
  def __init__(self, currentGameState, agentIndex, actionsSoFar, utilitySoFar, visitedPositions, currentFeatures):
    self.currentGameState = currentGameState
    self.agentIndex = agentIndex
    self.actionsSoFar = actionsSoFar
    self.utilitySoFar = utilitySoFar
    self.visitedPositions = visitedPositions
    self.currentFeatures = currentFeatures
  
  def __repr__(self):
    return str(self.agentIndex) + ' ' + str(self.actionsSoFar) + ' ' + str(self.utilitySoFar)


##########
# Agents #
##########

class ReflexAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)
    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """

    actionsList, utility = self.findAction(gameState, self.index)
    return actionsList[0]
    
    # nextGameState = gameState.generateSuccessor(self.index, action)
    # nextPosition = nextGameState.getAgentPosition(self.index)
    
    # currentFeatures = self.getFeatures(gameState)
    # nextFeatures = self.getFeatures(nextGameState)
    
    # currentWeight = self.getWeights(currentFeatures, gameState)
    # nextWeight = self.getWeights(nextFeatures, nextGameState)

    return successors[max_key]


  def findAction(self, gameState, agentIndex):
    visited = {}
    visitedPositions = [self.getPosition(gameState, self.index)]

    queue = util.Queue()
    actions = []

    startTime = time.time()

    startUtility = 0
    startFeatures = self.getFeatures(gameState)
    startWeights = self.getWeights(gameState)
    startState = SearchState(gameState, agentIndex, actions, startUtility, visitedPositions, startFeatures)
    queue.push((startState, 0))

    while not queue.isEmpty() and time.time() - startTime < 0.8:
      (searchState, utility) = queue.pop()
      nextActions = searchState.currentGameState.getLegalActions(self.index)
      if Directions.STOP in nextActions:
        nextActions.remove(Directions.STOP)



      print 'nextActions:', nextActions
      for action in nextActions:
        print 'checking action:', action
        nextGameState = searchState.currentGameState.generateSuccessor(searchState.agentIndex, action)
        nextPosition = self.getPosition(nextGameState, self.index)

        print 'nextPosition:', nextPosition, 'visited positions:', searchState.visitedPositions
        if nextPosition in searchState.visitedPositions and len(nextActions) > 1:
          continue

        nextStateUtility = 0
        if nextGameState not in visited:
          nextStateUtility = self.getUtility(nextGameState)
          visited[nextGameState] = nextStateUtility
        else:
          nextStateUtility = visited[nextGameState]

        print 'utility with ', action, '=', nextStateUtility
        totalUtilitySoFar = nextStateUtility + searchState.utilitySoFar

        nextSearchStateActions = searchState.actionsSoFar
        nextSearchStateActions.append(action)
        nextVisitedPositions = searchState.visitedPositions
        nextVisitedPositions.append(nextPosition)
        
        print 'nextSearchStateActions:', nextSearchStateActions
        nextSearchState = SearchState(nextGameState, agentIndex, nextSearchStateActions, totalUtilitySoFar, nextVisitedPositions, self.getFeatures(nextGameState))
        queue.push((nextSearchState, totalUtilitySoFar))

        # time.sleep(1)

    print 'queue:', len(queue.list)
    bestActions = []
    maxUtility = -99999999999999999
    while not queue.isEmpty():
      s, u = queue.pop()
      if u > maxUtility:
        maxUtility = u
        bestActions = s.actionsSoFar
    
    print 'bestActions:', bestActions, ' maxUtility:', maxUtility
    return bestActions, maxUtility

        # if nextPosition not in visitedPositions:
        #   tempVisitedPositions = state.visitedPositions
        #   tempVisitedPositions.append(nextPosition)


  def getUtility(self, gameState):
    features = self.getFeatures(gameState)
    weights = self.getWeights(gameState)
    return features * weights


  def getPosition(self, gameState, agentIndex):
    return gameState.getAgentPosition(agentIndex)


  def getDistToHome(self, gameState):
    current_position = gameState.getAgentPosition(self.index)


  def getFeatures(self, gameState):
    # print 'color:', gameState.getAgentState(agent)

    # print 'offensive index:', self.index

    features = util.Counter()

    agentStateData = gameState.getAgentState(self.index)
    agentPosition = agentStateData.getPosition()

    print 'agent', self.index, 'position:', agentPosition

    enemy_indices = self.getOpponents(gameState)
    foodList = self.getFood(gameState).asList()

    features['distanceToGhost'] = min(self.getMazeDistance(agentPosition, gameState.getAgentPosition(enemy_index)) for enemy_index in enemy_indices if not gameState.getAgentState(enemy_index).isPacman)
    features['numFoodLeft'] = len(gameState.getRedFood().asList() if self.red else gameState.getBlueFood().asList())
    features['distanceToNearestFood'] = min( [self.getMazeDistance(agentPosition, food) for food in foodList] )
    features['numCapsulesLeft'] = len(gameState.getRedCapsules() if self.red else gameState.getBlueCapsules())

    # time.sleep(5)
    # print agent, 'getting features:', features

    print 'offensive features:', features
    return features


  def getWeights(self, gameState):
    weights = util.Counter({
      'distanceToGhost' : 30,
      'numFoodLeft' : -15,
      'distanceToNearestFood' : -1000,
      'numCapsulesLeft' : -10
    })

    if not gameState.getAgentState(self.index).isPacman:
      weights['distanceToGhost'] = 0

    return weights



  # TODO: implement evaluation function
  def evaluation(self, gameState, agent):
    # print 'evaluating...'
    features = self.getFeatures(gameState, agent)
    weights = self.getWeights(gameState, agent)
    evaluation = weights * features
    print 'evaluation of agent', agent, ':', evaluation
    return evaluation


