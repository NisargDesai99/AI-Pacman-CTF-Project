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
    startWeights = self.getWeights(gameState, startFeatures)
    startState = SearchState(gameState, agentIndex, actions, startUtility, visitedPositions, startFeatures)
    queue.push((startState, 0))

    nextActions = gameState.getLegalActions(self.index)

    # if there's food really close by, get it before anything else
    for action in nextActions:
      nextGameState = gameState.generateSuccessor(self.index, action)
      nextPosition = self.getPosition(nextGameState, self.index)
      nextFeatures = self.getFeatures(nextGameState)
      
      # print 'nextPosition:', nextPosition, ' with action:', action
      
      # print 'nextActions:', nextActions
      # print '(21,12):', self.getFood(gameState)[21][12]
      # print '(21,11):', self.getFood(gameState)[21][11]
      # if nextPosition == (21,11) or nextPosition == (21,12):
      #   time.sleep(10)

      if self.getFood(gameState)[nextPosition[0]][nextPosition[1]] and gameState.getAgentState(self.index).isPacman:
        print 'getting food'
        # time.sleep(10)
        return [action], 10
      else:
        print 'nextPosition:', nextPosition
        print self.getFood(gameState)[nextPosition[0]][nextPosition[1]]
        # time.sleep(10)


      # currentPosition = self.getPosition(gameState, self.index)
      # nearbyPositions = []
      # for i in range(3):
      #   for j in range(3):
      #     if self.isLegalPosition((currentPosition[0] + i, currentPosition[1] + j), gameState):
      #       nearbyPositions.append( (currentPosition[0] + i, currentPosition[1] + j) )

      # # nearbyPositions = [[ (nextPosition[0] + i, nextPosition[1] + j) for j in range(3) if self.isLegalPosition((nextPosition[0] + i, nextPosition[1] + j), nextGameState)] for i in range(3)]
      # nearbyPositionDistances = { pos : self.getMazeDistance(currentPosition, pos) for pos in nearbyPositions }
      # minFoodDistPosition = min(nearbyPositionDistances.iteritems(), key=operator.itemgetter(1))

      # closestGhostDistances = self.getDistanceToEnemyGhosts(gameState)
      # minGhostDistance = min(closestGhostDistances.iteritems(), key=operator.itemgetter(1))[1]

      # # print 'nearbyPositionDistances:', nearbyPositionDistances
      # # print 'minFoodDist:', minFoodDistPosition
      # # print 'minGhostDistance:', minGhostDistance

      # if gameState.getAgentState(self.index).isPacman:
      #   if minFoodDistPosition[1] > 0 and minGhostDistance > 3:
      #     return [action], 10

      # if self.getMazeDistance(nextPosition, food)


    print '------------------------------'

    depthCounter = 100
    # while depthCounter >= 0 and not queue.isEmpty() and time.time() - startTime < 0.8:
    while not queue.isEmpty() and time.time() - startTime < 0.8:
      (searchState, utility) = queue.pop()
      nextActions = searchState.currentGameState.getLegalActions(self.index)
      if Directions.STOP in nextActions:
        nextActions.remove(Directions.STOP)

      exploredActionTree = len(nextActions) == 1
      
      # FFFFFFFFFFFFFFFFFFFFTFTTFFFFFF

      for action in nextActions:
        nextGameState = searchState.currentGameState.generateSuccessor(searchState.agentIndex, action)
        nextPosition = self.getPosition(nextGameState, self.index)
        nextFeatures = self.getFeatures(nextGameState)
        
        # print 'nextPosition:', nextPosition, 'visited positions:', searchState.visitedPositions
        # if nextPosition in searchState.visitedPositions and not exploredActionTree:
        if nextPosition in searchState.visitedPositions:
        # if nextPosition in searchState.visitedPositions and exploredActionTree:
          continue

        # if nextFeatures['distanceToGhost'] <= len(nextActions) and len(nextActions) < 5 and nextGameState.getAgentState(self.index).isPacman:
        #   continue

        if nextGameState not in visited:
          nextStateUtility = self.getUtility(nextGameState)
          visited[nextGameState] = nextStateUtility
        else:
          nextStateUtility = visited[nextGameState]

        totalUtilitySoFar = nextStateUtility + searchState.utilitySoFar

        # nextSearchStateActions = searchState.actionsSoFar
        # nextSearchStateActions = [ a for a in searchState.actionsSoFar ]
        nextSearchStateActions = list(searchState.actionsSoFar)
        nextSearchStateActions.append(action)
        nextVisitedPositions = list(searchState.visitedPositions)
        nextVisitedPositions.append(nextPosition)

        nextSearchState = SearchState(nextGameState, agentIndex, nextSearchStateActions, totalUtilitySoFar, nextVisitedPositions, self.getFeatures(nextGameState))
        queue.push((nextSearchState, totalUtilitySoFar))

        depthCounter -= 1
        # time.sleep(1)

    # print 'queue:', len(queue.list)
    bestActions = []
    maxUtility = -99999999999999999
    # minUtility = 99999999999999999
    while not queue.isEmpty():
      s, u = queue.pop()
      # if u < minUtility:
      # print 'state:', str(s), ' utility:', u
      if u > maxUtility:
        maxUtility = u
        bestActions = s.actionsSoFar
    
    # print 'bestActions:', bestActions, ' maxUtility:', maxUtility
    # print '------------------------------'
    return bestActions, maxUtility

        # if nextPosition not in visitedPositions:
        #   tempVisitedPositions = state.visitedPositions
        #   tempVisitedPositions.append(nextPosition)


  def getUtility(self, gameState):
    features = self.getFeatures(gameState)
    weights = self.getWeights(gameState, features)
    return features * weights


  def isLegalPosition(self, position, gameState):
    # print 'checking position:', position
    walls = gameState.getWalls()
    validX = position[0] < walls.width
    validY = position[1] < walls.height
    # print 'height:', walls.height
    # print 'width:', walls.width
    if not validX or not validY:
      return False
    else:
      return not gameState.hasWall(position[0], position[1])


  def getPosition(self, gameState, agentIndex):
    return gameState.getAgentPosition(agentIndex)


  def getDistanceToHome(self, gameState):

    currentPosition = gameState.getAgentPosition(self.index)
    gridHalf = self.getFood(gameState).width

    # yBorderPos = [ (gridHalf, y) for y in range(self.getFood(gameState).height) if not gameState.hasWall(gridHalf, y) ]
    yBorderPos = [ (gridHalf, y) for y in range(gameState.getWalls().height) if not gameState.hasWall(gridHalf-1, y) ]

    distances = [ self.getMazeDistance(currentPosition, (gridHalf, y)) for y in yBorderPos ]

    return min(distances) if distances else 0


  def getDistanceToEnemyPacmen(self, gameState):
    enemyAgents = self.getOpponents(gameState)

    selfPosition = gameState.getAgentPosition(self.index)
    distances = { enemy : self.getMazeDistance(selfPosition, gameState.getAgentPosition(enemy)) for enemy in enemyAgents }

    return distances

  def getDistanceToEnemyGhosts(self, gameState):
    enemyAgents = self.getOpponents(gameState)

    selfPosition = gameState.getAgentPosition(self.index)
    distances = { enemy : self.getMazeDistance(selfPosition, gameState.getAgentPosition(enemy)) for enemy in enemyAgents }

    return distances


  def getNumCapturedFood(self, gameState):
    return gameState.getAgentState(self.index).numCarrying


  def getFeatures(self, gameState):
    features = util.Counter()

    agentStateData = gameState.getAgentState(self.index)
    agentPosition = agentStateData.getPosition()

    enemy_indices = self.getOpponents(gameState)
    foodList = self.getFood(gameState).asList()

    enemyPacmen = [ enemyAgent for enemyAgent in enemy_indices if gameState.getAgentState(enemyAgent).isPacman ]
    enemyGhosts = [ enemyAgent for enemyAgent in enemy_indices if not gameState.getAgentState(enemyAgent).isPacman ]

    # features['distanceToEnemyPacman'] = min([ self.getMazeDistance(agentPosition, gameState.getAgentPosition(enemy_index)) for enemy_index in enemy_indices if gameState.getAgentState(enemy_index).isPacman ])
    # features['distanceToGhost'] = min([ self.getMazeDistance(agentPosition, gameState.getAgentPosition(enemy_index)) for enemy_index in enemy_indices if not gameState.getAgentState(enemy_index).isPacman ])
    
    features['distanceToEnemyPacman'] = min(enemyPacmen) if len(enemyPacmen) else 99999999
    features['distanceToGhost'] = min(enemyGhosts) if len(enemyGhosts) else 99999999
    
    features['numFoodLeft'] = len(gameState.getRedFood().asList() if self.red else gameState.getBlueFood().asList())
    features['distanceToNearestFood'] = min( [self.getMazeDistance(agentPosition, food) for food in foodList] )
    
    features['numCapsulesLeft'] = len(gameState.getRedCapsules() if self.red else gameState.getBlueCapsules())

    features['capturedFood'] = self.getNumCapturedFood(gameState)

    # features['score'] = self.getScore(gameState)
    
    features['distanceToHome'] = self.getDistanceToHome(gameState)

    # print 'distance to home:', features['distanceToHome']

    # time.sleep(10)

    return features


  def getWeights(self, gameState, features):

    enemy_indices = self.getOpponents(gameState)

    enemyPacmen = [ enemyAgent for enemyAgent in enemy_indices if gameState.getAgentState(enemyAgent).isPacman ]
    enemyGhosts = [ enemyAgent for enemyAgent in enemy_indices if not gameState.getAgentState(enemyAgent).isPacman ]

    weights = util.Counter({
      'distanceToEnemyPacman' : -4,
      'distanceToGhost' : 3,
      'numFoodLeft' : -1,
      'distanceToNearestFood' : -10,
      'numCapsulesLeft' : -1,
      'distanceToHome': 0
    })

    if gameState.getAgentState(self.index).isPacman:
      if features['capturedFood'] > 1:
        weights['distanceToHome'] = -10
      elif features['capturedFood'] > 3:
        weights['distanceToHome'] = -100
      elif features['capturedFood'] > 6:
        weights['distanceToHome'] = -200
    else:
      weights['distanceToHome'] = 0

    if not gameState.getAgentState(self.index).isPacman:
      # print 'not pacman'
      weights['distanceToGhost'] = 0
      weights['distanceToEnemyPacman'] = -10
    else:
      # agent is pacman
      weights['distancetoGhost'] = 20
      weights['distanceToEnemyPacman'] = 0


    return weights


  # def evaluation(self, gameState, agent):
  #   # print 'evaluating...'
  #   features = self.getFeatures(gameState, agent)
  #   weights = self.getWeights(gameState, agent)
  #   evaluation = weights * features
  #   print 'evaluation of agent', agent, ':', evaluation
  #   return evaluation


