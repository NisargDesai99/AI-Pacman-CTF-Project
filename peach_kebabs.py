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
    print 'chosenActionsList:', actionsList, '\nmax utlity:', utility
    # if actionsList[0] == Directions.SOUTH and utility > 3300 and utility < 3700:
    #   time.sleep(10)
    # if actionsList[0] == Directions.NORTH and utility > 6000 and utility < 7100:
    #   time.sleep(10)
    # time.sleep(0.5)
    return actionsList[0]

    # nextGameState = gameState.generateSuccessor(self.index, action)
    # nextPosition = nextGameState.getAgentPosition(self.index)

    # currentFeatures = self.getFeatures(gameState)
    # nextFeatures = self.getFeatures(nextGameState)

    # currentWeight = self.getWeights(currentFeatures, gameState)
    # nextWeight = self.getWeights(nextFeatures, nextGameState)

    # return successors[max_key]


  def findAction(self, gameState, agentIndex):
    visited = {}
    visitedPositions = [self.getPosition(gameState, self.index)]

    # queue = util.Stack()
    queue = util.Queue()
    actions = []

    startTime = time.time()

    startUtility = 0
    startFeatures = self.getFeatures(gameState)
    startWeights = self.getWeights(gameState, startFeatures)
    startState = SearchState(gameState, agentIndex, actions, startUtility, visitedPositions, startFeatures)
    queue.push((startState, 0))

    nextActions = gameState.getLegalActions(self.index)
    actionsWithDistToHome = {}

    if Directions.STOP in nextActions:
      nextActions.remove(Directions.STOP)

    currMinHomeAction = None
    currMinHomeDist = 7897985709183423

    currMinKillAction = None
    currMinKillDist = 7849332789473298

    currMinFoodAction = None
    currMinFoodDist = 7897982347892347

    currMinGhostKillAction = None
    currMinGhostKillDist = 7897982739812789

    # if there's food really close by, get it before anything else
    for action in nextActions:
      nextGameState = gameState.generateSuccessor(self.index, action)
      nextPosition = self.getPosition(nextGameState, self.index)
      # nextFeatures = self.getFeatures(nextGameState)

      currentAgentState = gameState.getAgentState(self.index)
      nextAgentState = nextGameState.getAgentState(self.index)

      # print 'nextPosition:', nextPosition, ' with action:', action

      # print 'nextActions:', nextActions
      # print '(21,12):', self.getFood(gameState)[21][12]
      # print '(21,11):', self.getFood(gameState)[21][11]
      # if nextPosition == (21,11) or nextPosition == (21,12):
      #   time.sleep(10)

      # closestPacmenDistances = self.getDistanceToEnemyPacmen(gameState)
      # minDistPacman = min(closestPacmenDistances.iteritems(), key=operator.itemgetter(1))
      enemyPositions = [ gameState.getAgentPosition(enemyAgent) for enemyAgent in self.getOpponents(gameState) ]
      if nextPosition in enemyPositions:
        return [action], 10

      closestGhostDistances = self.getDistancesToEnemyGhosts(gameState)
      minGhostDistItem = min(closestGhostDistances.iteritems(), key=operator.itemgetter(1)) if len(closestGhostDistances) else None
      if minGhostDistItem is not None:
        minGhostDistAgent = minGhostDistItem[0]
        minGhostDistance = minGhostDistItem[1]

      # if minGhostDistance < 2:
      #   print 'min ghost distance is less than 2'
      #   if currentAgentState.numCarrying > 0:
      #     print 'carrying more than 0'
        # time.sleep(5)

      capsulePositions = self.getCapsules(gameState)
      print 'capsule positions:', capsulePositions
      if currentAgentState.isPacman and (nextPosition in capsulePositions) and minGhostDistance < 5:
        print 'getting capsule'
        return [action], 10

      if minGhostDistItem is not None:
        if currentAgentState.isPacman:
          print 'minGhostDistance:', minGhostDistance
          print 'is next pos', nextPosition, ' food pos?', self.getFood(gameState)[nextPosition[0]][nextPosition[1]]
          if self.getFood(gameState)[nextPosition[0]][nextPosition[1]]:
            # time.sleep(1)
            print('NEXT POS IS FOOD')
            print('NEXT POS IS FOOD')
            print('NEXT POS IS FOOD')
            print('NEXT POS IS FOOD')

        if ((minGhostDistance >= 4 or gameState.getAgentState(minGhostDistAgent).scaredTimer > 0) and self.getFood(gameState)[nextPosition[0]][nextPosition[1]])\
                and len(nextActions) <= 2 and currentAgentState.isPacman:
          print 'getting food'
          # time.sleep(5)
          return [action], 10

        if len(nextActions) > 2 and minGhostDistance > 3 and self.getFood(gameState)[nextPosition[0]][nextPosition[1]]\
            and currentAgentState.isPacman:
          print 'GETTING FOOD 2'
          return [action], 10

      ghostDistancesNextGameState = self.getDistancesToEnemyGhosts(nextGameState)
      nextMinGhostDistance = min(ghostDistancesNextGameState.iteritems(), key=operator.itemgetter(1))[1] if ghostDistancesNextGameState else None

      if nextMinGhostDistance is not None:
        if self.isPositionInHome(gameState, nextPosition) and currentAgentState.isPacman and nextMinGhostDistance < 5 and self.getMinDistanceToHome(gameState) <= 1 and currentAgentState.numCarrying > 0:
          print 'distance to home:', self.getMinDistanceToHome(gameState), ' action: ', action
          # print 'trying to return home with action:', action
          # time.sleep(3)
          return [action], 10

      distToHome = self.getMinDistanceToHome(nextGameState)
      if distToHome < currMinHomeDist:
        currMinHomeDist = distToHome
        currMinHomeAction = action

      pacmanDistances = self.getDistancesToEnemyPacmen(nextGameState)
      if len(pacmanDistances):
        nextMinPacmanDistance = min( pacmanDistances.iteritems(), key=operator.itemgetter(1) )[1] if len(pacmanDistances) else None
        if nextMinPacmanDistance is not None:
          if nextMinPacmanDistance < currMinKillDist:
            currMinKillDist = nextMinPacmanDistance
            currMinKillAction = action

      minFoodDist = self.getMinDistanceToFood(nextGameState)
      if currMinFoodDist < minFoodDist:
        currMinFoodDist = minFoodDist
        currMinFoodAction = action


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

    ghostDistancesThisGameState = self.getDistancesToEnemyGhosts(gameState)
    minGhostDistItem = min(ghostDistancesThisGameState.iteritems(), key=operator.itemgetter(1)) if ghostDistancesThisGameState else None
    if minGhostDistItem is not None:
      minGhostIndex = minGhostDistItem[0]
      minGhostDistance = minGhostDistItem[1]

    aState = gameState.getAgentState(self.index)
    # ghostState = gameState.getAgentState(minGhostIndex)

    # to get home
    # if currMinHomeDist < 3 and gameState.getAgentState(self.index).isPacman and minGhostDistance > 5 and minGhostDistance < 10 and gameState.getAgentState(self.index).numCarrying > 0:
    if currMinHomeDist < 3 and aState.isPacman and aState.numCarrying > 0:
      # time.sleep(5)
      print 'currMinHomeAction'
      return [currMinHomeAction], 10

    # if enemy is killable (in home) and close by, prioritize the kill
    # if currMinKillDist < 4 and not gameState.getAgentState(self.index).isPacman:
    if currMinKillDist < 5 and aState.scaredTimer == 0:
      # print 'returning:', currMinKillAction, ' to try to kill enemy pacman'
      # time.sleep(5)
      return [currMinKillAction], 10

    # if currMinGhostKillDist < 5 and not aState.isPacman and ghostState.scaredTimer > currMinGhostKillDist and (aState.numCarrying < 3):
    #   return [currMinGhostKillDist], 10

    # if currMinFoodDist < 4 and minGhostDistance > currMinFoodDist * 2:
    #   return [currMinFoodAction], 10

    # minDist
    # if currentAgentState.isPacman and min(actionsWithDistToHome.iteritems(), key=operator.itemgetter(1))[1] < 5 currentAgentState.numCarrying > 0:
    #     print 'distance to home:', self.getDistanceToHome(gameState)
    #     print 'trying to return home with action:', action
    #     time.sleep(3)
    #     return [action], 10

    # print '------------------------------'

    depthCounter = 300
    # while depthCounter >= 0 and not queue.isEmpty() and time.time() - startTime < 0.8:
    while not queue.isEmpty() and time.time() - startTime < 0.65:
    # while depthCounter >= 0:
      (searchState, utility) = queue.pop()
      nextActions = searchState.currentGameState.getLegalActions(self.index)
      
      # TODO: create a way to assume enemy actions
      # nextEnemyActions = []
      
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

        # if nextFeatures['distanceToEnemyGhosts'] <= len(nextActions) and len(nextActions) < 5 and nextGameState.getAgentState(self.index).isPacman:
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
    # time.sleep(2)
    # print '------------------------------'
    # print 'depthCounter:', depthCounter
    return bestActions, maxUtility

        # if nextPosition not in visitedPositions:
        #   tempVisitedPositions = state.visitedPositions
        #   tempVisitedPositions.append(nextPosition)


  def isPositionInHome(self, gameState, position):
    gridHalf = gameState.getWalls().width / 2
    if self.red:
      return position[0] < gridHalf
    else:
      return position[0] > gridHalf


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


  def getMinDistanceToFood(self, gameState):
    agentState = gameState.getAgentState(self.index)
    agentPosition = gameState.getAgentPosition(self.index)

    foodList = self.getFood(gameState).asList()
    minDist = min([self.getMazeDistance(agentPosition, foodPosition) for foodPosition in foodList])

    return minDist

  def getMinDistanceToHome(self, gameState):

    agentState = gameState.getAgentState(self.index)
    if not agentState.isPacman:
      return 0

    currentPosition = gameState.getAgentPosition(self.index)
    gridHalf = self.getFood(gameState).width / 2

    if (currentPosition[0] < gridHalf and self.red) or (currentPosition[0] > gridHalf and not self.red):
      return 0

    # yBorderPos = [ (gridHalf, y) for y in range(self.getFood(gameState).height) if not gameState.hasWall(gridHalf, y) ]
    yBorderPos = [ (gridHalf, y) for y in range(gameState.getWalls().height) if not gameState.hasWall(gridHalf, y) ]
    distances = [ self.getMazeDistance(currentPosition, position) for position in yBorderPos ]

    return min(distances) if distances else 0


  def getDistancesToEnemyPacmen(self, gameState):
    enemyAgents = self.getOpponents(gameState)
    enemyPacmen = [ agent for agent in enemyAgents if gameState.getAgentState(agent).isPacman ]

    selfPosition = gameState.getAgentPosition(self.index)
    distances = { enemy : self.getMazeDistance(selfPosition, gameState.getAgentPosition(enemy)) for enemy in enemyPacmen }

    return distances


  def getDistancesToEnemyGhosts(self, gameState):
    enemyAgents = self.getOpponents(gameState)
    enemyGhosts = [ agent for agent in enemyAgents if not gameState.getAgentState(agent).isPacman ]

    selfPosition = gameState.getAgentPosition(self.index)
    distances = { enemy : self.getMazeDistance(selfPosition, gameState.getAgentPosition(enemy)) for enemy in enemyGhosts }

    return distances


  def getNumCapturedFood(self, gameState):
    return gameState.getAgentState(self.index).numCarrying


  def getUtility(self, gameState):
    features = self.getFeatures(gameState)
    weights = self.getWeights(gameState, features)


    # # minimize
    # 'distanceToNearestFood' : 7,
    # 'numFoodLeft' : 2,
    # 'capturedFood' : 5,
    # 'distanceToEnemyPacmen' : 0,
    # 'numCapsulesLeft' : 1,
    # 'distanceToHome' : 0,     # in certain cases

    # # maximize
    # 'distanceToEnemyGhosts' : 0,
    # 'distanceToAlly' : 0,

    currentUtility = 0.0
    for feature, value in features.items():

      # there are certain features that should be minimized
      # so we get an inverse of those features

      if value != 0 and weights[feature] != 0:
        if feature == 'distanceToNearestFood':
          currentUtility += float(weights[feature]) / value
          # currentUtility += 1 / (float(weights[feature]) * value)
        elif feature == 'numFoodLeft':
          currentUtility += float(weights[feature]) / value
          # currentUtility += 1 / (float(weights[feature]) * value)
        elif feature == 'distanceToEnemyPacmen':
          currentUtility += float(weights[feature]) / value
          # currentUtility += 1 / (float(weights[feature]) * value)
        elif feature == 'numEnemyPacmen':
          currentUtility += float(weights[feature]) / value
          # currentUtility += 1 / (float(weights[feature]) * value)
        elif feature == 'distanceToHome':
          currentUtility += float(weights[feature]) / value
          # currentUtility += 1 / (float(weights[feature]) * value)
        elif feature == 'distanceToNearestCapsule':
          currentUtility += float(weights[feature]) / value
          # currentUtility += 1 / (float(weights[feature]) * value)
        elif feature == 'distanceToMyCapsule':
          currentUtility += float(weights[feature]) / value
          # currentUtility += 1 / (float(weights[feature]) * value)


      # if feature == 'distanceToFood' and value != 0:
      #   print 'feature == distanceToFood'
      #   currentUtility += 1 / ( float(weights[feature]) * value )
      # elif feature == 'distanceToPacmen' and value != 0:
      #   print 'feature == distanceToPacmen'
      #   currentUtility += 1 / ( float(weights[feature]) * value )
      # elif feature == 'distanceToHome' and value != 0:
      #   print 'feature == distanceToHome'
      #   currentUtility += 1 / ( float(weights[feature]) * value )

      else:
        currentUtility += weights[feature] * value

    print 'utility:', currentUtility, ' self.index:', self.index, ' isPacman:', gameState.getAgentState(self.index).isPacman
    # print 'features:', features
    # print 'weights:', weights
    return currentUtility


  def getFeatures2(self, gameState):

    features = util.Counter()
    agentStateData = gameState.getAgentState(self.index)
    agentPosition = agentStateData.getPosition()
    foodList = self.getFood(gameState).asList()

    enemyIndices = self.getOpponents(gameState)
    enemyPacmen = [ enemyAgent for enemyAgent in enemyIndices if gameState.getAgentState(enemyAgent).isPacman ]
    enemyGhosts = [ enemyAgent for enemyAgent in enemyIndices if not gameState.getAgentState(enemyAgent).isPacman ]

    features['distanceToFood'] = min([ self.getMazeDistance(agentPosition, foodPos) for foodPos in foodList ])
    features['distanceToGhosts'] = min([ self.getMazeDistance(agentPosition, gameState.getAgentPosition(ghost)) for ghost in enemyGhosts ]) if len(enemyGhosts) else 0
    features['distanceToPacmen'] = min([ self.getMazeDistance(agentPosition, gameState.getAgentPosition(pacman)) for pacman in enemyPacmen ]) if len(enemyPacmen) else 0
    features['distanceToHome'] = self.getMinDistanceToHome(gameState)
    features['score'] = self.getScore(gameState)

    return features


  def getWeights2(self, gameState, features):
    # sum(features['distanceToFood']) + 500 if features['distanceToFood'] else 0

    weights = util.Counter({
      'distanceToFood' : 8,
      'distanceToPacmen' : 1,
      'distanceToGhosts' : 3,
      'distanceToHome' : 1,
      'score' : 10,
    })

    agentStateData = gameState.getAgentState(self.index)
    agentPosition = agentStateData.getPosition()
    foodList = self.getFood(gameState).asList()

    enemyIndices = self.getOpponents(gameState)
    enemyPacmen = [ enemyAgent for enemyAgent in enemyIndices if gameState.getAgentState(enemyAgent).isPacman ]
    enemyGhosts = [ enemyAgent for enemyAgent in enemyIndices if not gameState.getAgentState(enemyAgent).isPacman ]

    scaredEnemyGhostTimers = {}
    for enemyGhostAgent in enemyGhosts:
      scaredTimer = gameState.getAgentState(enemyGhostAgent).scaredTimer
      if scaredTimer > 0:
        scaredEnemyGhostTimers[enemyGhostAgent] = scaredTimer

    if not agentStateData.isPacman:
      weights['distanceToFood'] = 5
      weights['distanceToPacmen'] = 0
      weights['distanceToGhosts'] = 2
      weights['distanceToHome'] = 0

      if len(enemyPacmen):
        weights['distanceToFood'] = 2
        weights['distanceToPacmen'] += 10
        weights['distanceToGhosts'] = -1
    else:
      weights['distanceToFood'] = 10
      weights['distanceToPacmen'] = 2

      if len(scaredEnemyGhostTimers):
        # time.sleep(5)
        weights['distanceToGhosts'] = 1 / 50
      else:
        weights['distanceToGhosts'] = 5

      weights['distanceToHome'] = agentStateData.numCarrying + (5 if features['distanceToGhosts'] < 5 else 1)
      # weights['distanceToHome'] = agentStateData.numCarrying * 10 + (50 if features['distanceToGhosts'] < 5 else 5)

    print 'features:', features
    print 'weights', weights

    return weights


  def getFeatures(self, gameState):
    features = util.Counter()

    agentStateData = gameState.getAgentState(self.index)
    agentPosition = agentStateData.getPosition()

    enemy_indices = self.getOpponents(gameState)
    foodList = self.getFood(gameState).asList()

    enemyPacmen = [ enemyAgent for enemyAgent in enemy_indices if gameState.getAgentState(enemyAgent).isPacman ]
    enemyGhosts = [ enemyAgent for enemyAgent in enemy_indices if not gameState.getAgentState(enemyAgent).isPacman ]

    # features['distanceToEnemyPacmen'] = min([ self.getMazeDistance(agentPosition, gameState.getAgentPosition(enemy_index)) for enemy_index in enemy_indices if gameState.getAgentState(enemy_index).isPacman ])
    # features['distanceToEnemyGhosts'] = min([ self.getMazeDistance(agentPosition, gameState.getAgentPosition(enemy_index)) for enemy_index in enemy_indices if not gameState.getAgentState(enemy_index).isPacman ])

    # features['distanceToEnemyPacmen'] = [v for k,v in self.getDistancesToEnemyPacmen(gameState).items()] if len(enemyPacmen) else 99999
    # features['distanceToEnemyGhosts'] = min(self.getDistancesToEnemyGhosts(gameState).iteritems(), key=operator.itemgetter(1))[1] if len(enemyGhosts) else 99999

    features['distanceToEnemyPacmen'] = [v for k, v in self.getDistancesToEnemyPacmen(gameState).items()] if len(enemyPacmen) else 99999
    features['distanceToEnemyGhosts'] = [v for k, v in self.getDistancesToEnemyghosts(gameState).items()] if len(enemyGhosts) else 99999

    # features['numFoodLeft'] = len(gameState.getRedFood().asList() if self.red else gameState.getBlueFood().asList())
    features['distanceToNearestFood'] = min( [self.getMazeDistance(agentPosition, food) for food in foodList] )

    features['numCapsulesLeft'] = len(gameState.getRedCapsules() if self.red else gameState.getBlueCapsules())

    features['capturedFood'] = self.getNumCapturedFood(gameState)

    features['score'] = self.getScore(gameState)

    allyIndex = [ agent for agent in self.getTeam(gameState) if agent != self.index ][0]
    features['distanceToAlly'] = self.getMazeDistance(agentPosition, gameState.getAgentPosition(allyIndex))
    features['distanceToHome'] = self.getMinDistanceToHome(gameState)

    features['numAlliesOnHomeSide'] = len([agent for agent in self.getTeam(gameState) if not gameState.getAgentState(agent).isPacman])

    # features['defend'] = 5

    features['numEnemyPacmen'] = len(enemyPacmen)

    capsuleDistances = [ self.getMazeDistance(agentPosition, capsulePosition) for capsulePosition in self.getCapsules(gameState) ]
    features['distanceToNearestCapsule'] = min(capsuleDistances) if len(capsuleDistances) else 0

    # print 'distance to home:', features['distanceToHome']
    # time.sleep(10)

    return features


  def getWeights(self, gameState, features):

    # TODO: add weights for captured food to prevent suicides to get home to defend

    weights = util.Counter({

      # minimize
      'distanceToNearestFood' : 7,
      # 'numFoodLeft' : 2,
      'distanceToEnemyPacmen' : 0,
      'numCapsulesLeft' : 1,
      'distanceToHome' : 0,     # in certain cases
      'numEnemyPacmen' : 10,
      'distanceToNearestCapsule' : 0,
      'distanceToMyCapsule' : 0,

      # maximize
      'distanceToEnemyGhosts' : 0,
      'capturedFood': 0,
      'score' : 10,
      'distanceToAlly' : 0,

      'numAlliesOnHomeSide' : 0,

      # misc
      # 'defend' : 10
    })

    # TODO: if my ghosts have a scared timer -> prioritize capturing food over going for enemy pacman

    enemyAgents = self.getOpponents(gameState)

    enemyPacmen = [ agent for agent in enemyAgents if gameState.getAgentState(agent).isPacman ]
    enemyGhosts = [ agent for agent in enemyAgents if not gameState.getAgentState(agent).isPacman ]

    currentAgentState = gameState.getAgentState(self.index)

    # may be more than one pacmen trying to capture food, get pacman with max food
    pacmanWithMostFood = None
    if len(enemyPacmen):
      foodHeldByPacmen = { enemyAgent : gameState.getAgentState(enemyAgent).numCarrying for enemyAgent in enemyPacmen }
      pacmanWithMostFood = max(foodHeldByPacmen.iteritems(), key=operator.itemgetter(1))

    distToEnemyGhosts = self.getDistancesToEnemyGhosts(gameState)
    minDistToEnemyGhost = min(distToEnemyGhosts.iteritems(), key=operator.itemgetter(1))[1] if len(distToEnemyGhosts) else 0

    minDistToEnemyPacman = features['distanceToEnemyPacmen'] if features['distanceToEnemyPacmen'] else 0

    # large bfs depth causes it to realize that eating capsule
    # and hitting a ghost increases distance to enemy ghost
    scaredEnemyGhostTimers = {}
    sumOfEnemyTimers = 0
    for enemyGhostAgent in enemyGhosts:
      scaredTimer = gameState.getAgentState(enemyGhostAgent).scaredTimer
      if scaredTimer > 0:
        scaredEnemyGhostTimers[enemyGhostAgent] = scaredTimer
        sumOfEnemyTimers += scaredTimer

    allyScaredTimers = {}
    sumOfAllyTimers = 0
    for allyAgent in self.getTeam(gameState):
      scaredTimer = gameState.getAgentState(allyAgent).scaredTimer
      if scaredTimer > 0:
        allyScaredTimers[allyAgent] = scaredTimer
        sumOfAllyTimers = scaredTimer

    # if len(allyScaredTimers):
      # print 'ally is scared:', allyScaredTimers
      # time.sleep(1)

    if not currentAgentState.isPacman:
      if len(enemyPacmen):
        if len(allyScaredTimers):
          weights['distanceToNearestFood'] += 10
          weights['capturedFood'] += 10
          weights['distanceToEnemyGhosts'] += 5
          weights['distanceToEnemyPacmen'] += 1.0/10.0
        else:
          # weights['numEnemyPacman'] += 100
          # TODO: maybe change to 4 or 5, 5 worked well for killing pacman
          weights['distanceToAlly'] = 2
          # weights['distanceToEnemyPacmen'] += 20 + (10 if sumOfAllyTimers / 2 < minDistToEnemyPacman else 0)
          weights['distanceToEnemyPacmen'] += 30
          weights['distanceToMyCapsule'] += 5
          weights['distanceToNearestFood'] -= 5
          weights['score'] = 0
          weights['capturedFood'] = 0
      else:
        weights['distanceToNearestFood'] += 10
        weights['distanceToEnemyGhosts'] += 5

      # TODO: change this back to 5 after testing
      if minDistToEnemyGhost < 5:
        weights['distanceToEnemyGhosts'] += 20
        # TODO: maybe add this to incentivize more movement
        # weights['distanceToCurrentPosition'] += 20
        weights['distanceToEnemyPacmen'] += 20 if len(enemyPacmen) else 0
        weights['distanceToNearestFood'] -= 5
        print 'distance to enemy ghost is less than 5 and is ghost'
        print 'weights:', weights
        # time.sleep(1)

    else:   # agent is pacman
      weights['distanceToNearestFood'] = 7
      weights['capturedFood'] = 3
      weights['distanceToEnemyGhosts'] = 3
      # TODO: 10 works well for distance to ally
      weights['distanceToAlly'] = 8

      if len(allyScaredTimers) and gameState.getAgentState(self.index).scaredTimer > 0:
        weights['distanceToNearestFood'] += 10
        weights['capturedFood'] += 10
        weights['distanceToEnemyGhosts'] += 10
        weights['distanceToEnemyPacmen'] = 1

      if not len(enemyPacmen):       # no invaders
        if minDistToEnemyGhost > 5:
          weights['distanceToNearestFood'] += 30
          weights['distanceToEnemyGhosts'] += 15
          weights['capturedFood'] += 20
          # weights['distanceToNearestCapsule'] += 15
        else:
          weights['distanceToNearestCapsule'] += 10
          weights['distanceToEnemyGhosts'] += 10
          # weights['capturedFood'] += 10
          # weights['score'] += 50
          weights['distanceToNearestFood'] = 3
          # weights['distanceToEnemyPacmen'] += 5
          weights['distanceToHome'] += 20
      else:                          # there are invaders
        weights['distanceToEnemyPacmen'] += 5 + (5 * features['distanceToEnemyPacmen'])
        if features['numAlliesOnHomeSide'] == 0:
          weights['numAlliesOnHomeSide'] = 10
          weights['distanceToAlly'] = 5
        elif features['numAlliesOnHomeSide'] == 1:
          weights['numAlliesOnHomeSide'] = 4
        elif features['numAlliesOnHomeSide'] == 2:
          weights['distanceToEnemyPacmen'] += 10

      if currentAgentState.numCarrying > 0:
        print 'there are ENEMY PACMEN and CARRYING > 0'
        weights['distanceToNearestFood'] = 10
        # weights['distanceToHome'] += 30 + (pacmanWithMostFood[1] * 10 if pacmanWithMostFood else 0)
        weights['distanceToHome'] += 15

        # isAllyOnHomeSide = len([agent for agent in self.getTeam(gameState) if
        #                         self.isPositionInHome(gameState, gameState.getAgentPosition(agent))])

        weights['distanceToEnemyGhosts'] += 15
        weights['score'] += 100
        weights['distanceToEnemyPacmen'] += 10
      elif currentAgentState.numCarrying == 0:
        print 'there are ENEMY PACMEN and CARRYING == 0'
        # TODO: this if statement below could help with agents not prioritizing
        # defense after already scoring some points -> defense becomes increasingly
        # important if your score is already good
        if self.getScore(gameState) > 0:
          # TODO: weight of 50 makes them sit at the edge until there is a pacman?
          weights['distanceToEnemyPacmen'] += 40
          weights['distanceToAlly'] = 20
        weights['distanceToNearestFood'] += 10
        weights['capturedFood'] += 5
        weights['distanceToEnemyGhosts'] += 7

      if len(scaredEnemyGhostTimers):
        # weights['distanceToAlly'] = -2
        weights['distanceToNearestFood'] += 60
        # weights['distanceToEnemyGhosts'] = 1
        # weights['distanceToEnemyGhosts'] = 1 / weights['distanceToEnemyGhosts']
        weights['distanceToHome'] += 10

      # if len(enemyPacmen) and currentAgentState.numCarrying > 0:
      #   weights['distanceToNearestFood'] = 0
      #   weights['distanceToHome'] += 30 + (pacmanWithMostFood[1] * 10 if pacmanWithMostFood else 0)
      #
      #   isAllyOnHomeSide = len([ agent for agent in self.getTeam(gameState) if self.isPositionInHome(gameState, gameState.getAgentPosition(agent)) ])
      #   weights['score'] += 20
      #   weights['distanceToEnemyPacmen'] += (pacmanWithMostFood[1] * 5 if pacmanWithMostFood else 0)

      # if len(enemyPacmen) and currentAgentState.numCarrying == 0:
      #   weights['distanceToNearestFood'] += 100
      #   weights['capturedFood'] += 20
      #   weights['distanceToEnemyGhosts'] += 20

      # if not len(enemyPacmen) and minDistToEnemyGhost > 5:
      #   weights['distanceToNearestFood'] += 30 * minDistToEnemyGhost
      #   weights['distanceToEnemyGhosts'] += 8
      #   weights['capturedFood'] += 10
      #   weights['distanceToNearestCapsule'] += 15
      #
      # if minDistToEnemyGhost < 5:
      #   # TODO
      #   weights['distanceToNearestCapsule'] += 15
      #   weights['distanceToEnemyGhosts'] += 10
      #   # weights['capturedFood'] += 10
      #   # weights['score'] += 50
      #   weights['distanceToNearestFood'] = 0
      #   weights['distanceToEnemyPacmen'] += 5
      #   weights['distanceToHome'] += 10

      # if features['capturedFood'] > 0:
      #   # weights['capturedFood'] += 20
      #   weights['distanceToHome'] += features['capturedFood'] * 5

      # if len(scaredEnemyGhostTimers):
      #   # weights['distanceToAlly'] = -2
      #   weights['distanceToNearestFood'] += 30
      #   # weights['distanceToEnemyGhosts'] = 1 / weights['distanceToEnemyGhosts']
      #   weights['distanceToHome'] += 10

      # if not gameState.getAgentState(self.index).isPacman:
    #   # print 'not pacman'
    #   weights['distanceToEnemyGhosts'] = 0
    #   weights['distanceToEnemyPacmen'] = -10
    # else:
    #   # agent is pacman
    #   weights['distanceToEnemyGhosts'] = 20
    #   weights['distanceToEnemyPacmen'] = 0

    # if len(allyScaredTimers):
    # print 'features:', features
    # print 'weights:', weights
    # time.sleep(0.3)
    return weights


  # def evaluation(self, gameState, agent):
  #   # print 'evaluating...'
  #   features = self.getFeatures(gameState, agent)
  #   weights = self.getWeights(gameState, agent)
  #   evaluation = weights * features
  #   print 'evaluation of agent', agent, ':', evaluation
  #   return evaluation


