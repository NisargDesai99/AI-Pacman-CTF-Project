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
               first = 'OffensiveFlashAgent', second = 'DefensiveFlashAgent'):
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


class FlashAgent(CaptureAgent):
    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)


    def chooseAction(self, gameState):
        actionsList, utility = self.findAction(gameState, self.index)
        print 'chosenAction:', actionsList[0], 'utlity:', utility
        return actionsList[0]


    def findAction(gameState, agentIndex):
        print 'base flash agent findAction call'
        pass


class OffensiveFlashAgent(FlashAgent):
    def findAction(self, gameState, agentIndex):
        print 'offensive flash agent call'
        possibleActions = gameState.getLegalActions(self.index)
        return [random.choice(possibleActions)], 10


    def getFeatures(self, gameState):
        features = util.Counter({
            'distToHome': 0,
            'distToInvaders': 0,
            'distToDefender': 0,
            'distToFood': 0
        })
        return features


    def getWeights(self, gameState):
        weights = util.Counter({
            'distToHome': 0,
            'distToInvaders': 0,
            'distToDefender': 0,
            'distToFood': 0
        })
        return weights


    def evaluate(self, features, weights):
        return features * weights


class DefensiveFlashAgent(FlashAgent):
    def findAction(self, gameState, agentIndex):
        print 'defensive flash agent call'
        actions = gameState.getLegalActions(self.index)

        visited = {}
        queue = util.Queue()
        startState = SearchState(gameState, self.index, actions, 0, visited, self.getFeatures(gameState))
        queue.push(startState)

        startTime = time.time()

        if Directions.STOP in actions:
            actions.remove(Directions.STOP)

        while not queue.isEmpty() and time.time() - startTime < 0.75:
            currentSearchState = queue.pop()

            for action in actions:
                print 'considering action:', action




        return [random.choice(actions)], 10


    def getFeatures(self, gameState):
        features = util.Counter({
            'distToHome': 0,
            'distToInvaders': 0,
            'distToDefender': 0,
            'distToFood': 0
        })
        return features


    def getWeights(self, gameState):
        weights = util.Counter({
            'distToHome': 0,
            'distToInvaders': 0,
            'distToDefender': 0,
            'distToFood': 0
        })
        return weights


    def evaluate(self, features, weights):
        return features * weights


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
    print 'chosenAction:', actionsList[0], 'utlity:', utility
    return actionsList[0]


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
    actionsWithDistToHome = {}

    if Directions.STOP in nextActions:
      nextActions.remove(Directions.STOP)

    currMinAction = None
    currMinDist = 789798570918342

    # if there's food really close by, get it before anything else
    for action in nextActions:
      nextGameState = gameState.generateSuccessor(self.index, action)
      nextPosition = self.getPosition(nextGameState, self.index)
      nextFeatures = self.getFeatures(nextGameState)

      currentAgentState = gameState.getAgentState(self.index)

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

      closestGhostDistances = self.getDistanceToEnemyGhosts(gameState)
      minGhostDistance = min(closestGhostDistances.iteritems(), key=operator.itemgetter(1))[1]

      if minGhostDistance > 5 and self.getFood(gameState)[nextPosition[0]][nextPosition[1]] and gameState.getAgentState(self.index).isPacman:
        print 'getting food'
        # time.sleep(3)
        return [action], 10

      ghostDistancesNextGameState = self.getDistanceToEnemyGhosts(nextGameState)
      nextMinGhostDistance = min(ghostDistancesNextGameState.iteritems(), key=operator.itemgetter(1))[1]

      if self.isPositionInHome(gameState, nextPosition) and currentAgentState.isPacman and nextMinGhostDistance < 5 and self.getDistanceToHome(gameState) <= 1 and currentAgentState.numCarrying > 0:
        print 'distance to home:', self.getDistanceToHome(gameState)
        print 'trying to return home with action:', action
        time.sleep(3)
        return [action], 10

      distToHome = self.getDistanceToHome(gameState)
      if distToHome < currMinDist:
        currMinDist = distToHome
        currMinAction = action

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

    ghostDistancesThisGameState = self.getDistanceToEnemyGhosts(gameState)
    minGhostDistance = min(ghostDistancesThisGameState.iteritems(), key=operator.itemgetter(1))[1]

    if currMinDist < 3 and gameState.getAgentState(self.index).isPacman and minGhostDistance > 5 and minGhostDistance < 10 and gameState.getAgentState(self.index).numCarrying > 0:
      time.sleep(5)
      return [currMinAction], 10

    # minDist
    # if currentAgentState.isPacman and min(actionsWithDistToHome.iteritems(), key=operator.itemgetter(1))[1] < 5 currentAgentState.numCarrying > 0:
    #     print 'distance to home:', self.getDistanceToHome(gameState)
    #     print 'trying to return home with action:', action
    #     time.sleep(3)
    #     return [action], 10

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

        # if nextFeatures['distanceToEnemyGhost'] <= len(nextActions) and len(nextActions) < 5 and nextGameState.getAgentState(self.index).isPacman:
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

    print 'bestActions:', bestActions, ' maxUtility:', maxUtility
    # time.sleep(2)
    # print '------------------------------'
    print 'depthCounter:', depthCounter
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


  def getDistanceToHome(self, gameState):

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


  def getUtility(self, gameState):
    features = self.getFeatures(gameState)
    weights = self.getWeights(gameState, features)


    # # minimize
    # 'distanceToNearestFood' : 7,
    # 'numFoodLeft' : 2,
    # 'capturedFood' : 5,
    # 'distanceToEnemyPacman' : 0,
    # 'numCapsulesLeft' : 1,
    # 'distanceToHome' : 0,     # in certain cases

    # # maximize
    # 'distanceToEnemyGhost' : 0,
    # 'distanceToAlly' : 0,


    currentUtility = 0.0
    for feature, value in features.items():

      # there are certain features that should be minimized
      # so we get an inverse of those features
      if feature == 'distanceToNearestFood' and value != 0:
        currentUtility += float(weights[feature]) / value
      # elif feature == 'numFoodLeft' and value != 0:
      #   currentUtility += float(weights[feature]) / value
      elif feature == 'distanceToEnemyPacman' and value != 0:
        currentUtility += float(weights[feature]) / value
      elif feature == 'numEnemyPacmen' and value != 0:
        currentUtility += float(weights[feature]) / value
      elif feature == 'distanceToHome' and value != 0:
        currentUtility += float(weights[feature]) / value
      else:
        currentUtility += weights[feature] * value

    print 'utility:', currentUtility, ' self.index:', self.index, ' isPacman:', gameState.getAgentState(self.index).isPacman
    print 'features:', features
    print 'weights:', weights
    return currentUtility


  def getFeatures(self, gameState):
    features = util.Counter()

    agentStateData = gameState.getAgentState(self.index)
    agentPosition = agentStateData.getPosition()

    enemy_indices = self.getOpponents(gameState)
    foodList = self.getFood(gameState).asList()

    enemyPacmen = [ enemyAgent for enemyAgent in enemy_indices if gameState.getAgentState(enemyAgent).isPacman ]
    enemyGhosts = [ enemyAgent for enemyAgent in enemy_indices if not gameState.getAgentState(enemyAgent).isPacman ]

    # features['distanceToEnemyPacman'] = min([ self.getMazeDistance(agentPosition, gameState.getAgentPosition(enemy_index)) for enemy_index in enemy_indices if gameState.getAgentState(enemy_index).isPacman ])
    # features['distanceToEnemyGhost'] = min([ self.getMazeDistance(agentPosition, gameState.getAgentPosition(enemy_index)) for enemy_index in enemy_indices if not gameState.getAgentState(enemy_index).isPacman ])

    features['distanceToEnemyPacman'] = min(self.getDistanceToEnemyPacmen(gameState).iteritems(), key=operator.itemgetter(1))[1] if len(enemyPacmen) else 99999999
    features['distanceToEnemyGhost'] = min(self.getDistanceToEnemyGhosts(gameState).iteritems(), key=operator.itemgetter(1))[1] if len(enemyGhosts) else 99999999

    # features['numFoodLeft'] = len(gameState.getRedFood().asList() if self.red else gameState.getBlueFood().asList())
    features['distanceToNearestFood'] = min( [self.getMazeDistance(agentPosition, food) for food in foodList] )

    features['numCapsulesLeft'] = len(gameState.getRedCapsules() if self.red else gameState.getBlueCapsules())

    features['capturedFood'] = self.getNumCapturedFood(gameState)

    features['score'] = self.getScore(gameState)

    allyIndex = [ agent for agent in self.getTeam(gameState) if agent != self.index ][0]
    features['distanceToAlly'] = self.getMazeDistance(agentPosition, gameState.getAgentPosition(allyIndex))
    features['distanceToHome'] = self.getDistanceToHome(gameState)

    features['defend'] = 5

    features['numEnemyPacmen'] = len(enemyPacmen)

    # print 'distance to home:', features['distanceToHome']
    # time.sleep(10)

    return features


  def getWeights(self, gameState, features):

    # TODO: add weights for captured food to prevent suicides to get home to defend

    weights = util.Counter({

      # minimize
      'distanceToNearestFood' : 7,
      # 'numFoodLeft' : 2,
      'capturedFood' : 0,
      'distanceToEnemyPacman' : 0,
      'numCapsulesLeft' : 1,
      'distanceToHome' : 0,     # in certain cases
      'numEnemyPacmen' : 50,

      # maximize
      'distanceToEnemyGhost' : 0,
      'score' : 10,
      'distanceToAlly' : 0,


      # misc
      'defend' : 10
    })

    enemy_indices = self.getOpponents(gameState)

    enemyPacmen = [ enemyAgent for enemyAgent in enemy_indices if gameState.getAgentState(enemyAgent).isPacman ]
    enemyGhosts = [ enemyAgent for enemyAgent in enemy_indices if not gameState.getAgentState(enemyAgent).isPacman ]

    currentAgentState = gameState.getAgentState(self.index)

    # if gameState.getAgentState(self.index).isPacman:
    #   if features['capturedFood'] > 1:
    #     weights['distanceToHome'] = -10
    #   elif features['capturedFood'] > 3:
    #     weights['distanceToHome'] = -100
    #   elif features['capturedFood'] > 6:
    #     weights['distanceToHome'] = -200
    # else:
    #   weights['distanceToHome'] = 0

    pacmanWithMostFood = None
    if len(enemyPacmen):
      foodHeldByPacmen = { enemyAgent : gameState.getAgentState(enemyAgent).numCarrying for enemyAgent in enemyPacmen }
      pacmanWithMostFood = max(foodHeldByPacmen.iteritems(), key=operator.itemgetter(1))

    if not currentAgentState.isPacman:
      if len(enemyPacmen):
        # weights['numEnemyPacman'] += 100
        weights['distanceToEnemyPacman'] += 20 + (pacmanWithMostFood[1] * 500 if pacmanWithMostFood else 0)
        weights['distanceToNearestFood'] = 0
        weights['score'] = 0
        weights['capturedFood'] = 0

    distToEnemyGhosts = self.getDistanceToEnemyGhosts(gameState)
    minDistToEnemyGhost = min(distToEnemyGhosts.iteritems(), key=operator.itemgetter(1))[1]

    # large bfs depth causes it to realize that eating capsule
    # and hitting a ghost increases distance to enemy ghost
    scaredGhostTimers = {}
    for enemyGhostAgent in enemyGhosts:
      scaredTimer = gameState.getAgentState(enemyGhostAgent).scaredTimer
      if scaredTimer > 0:
        scaredGhostTimers[enemyGhostAgent] = scaredTimer

    if currentAgentState.isPacman:
      weights['distanceToNearestFood'] = 7
      weights['capturedFood'] = 3
      weights['distanceToEnemyGhost'] = 3

      if features['capturedFood'] == 0:
        weights['capturedFood'] = 15

      if minDistToEnemyGhost < 5:
        # TODO
        # weights['distanceToCapsule'] += 4
        # weights['distanceToEnemyGhost'] += 4
        weights['capturedFood'] += 10
        weights['score'] += 10
        weights['distanceToNearestFood'] = 0
        # weights['capturedFood']
        weights['distanceToEnemyPacman'] += 5
        weights['distanceToHome'] += 10

      if currentAgentState.numCarrying > 0:
        # weights['capturedFood'] += 20
        weights['distanceToHome'] += currentAgentState.numCarrying * 5

      if len(scaredGhostTimers):
        # weights['distanceToAlly'] = -2
        weights['distanceToEnemyGhost'] = 1 / weights['distanceToEnemyGhost']
        weights['distanceToHome'] += 2

      if len(enemyPacmen) and currentAgentState.numCarrying > 0:
        # may be more than one pacmen trying to capture food
        weights['distanceToNearestFood'] = 0
        weights['distanceToHome'] += 30 + (pacmanWithMostFood[1] * 10 if pacmanWithMostFood else 0)
        isAllyOnHomeSide = len([ agent for agent in self.getTeam(gameState) if self.isPositionInHome(gameState, gameState.getAgentPosition(agent)) ])
        # weights['defend'] = 20 if isAllyOnHomeSide else 100
        weights['score'] += 20
        print 'enemy pac index:', pacmanWithMostFood[0], ' numFood:', pacmanWithMostFood[1]
        weights['distanceToEnemyPacman'] += -(pacmanWithMostFood[1] * 5 if pacmanWithMostFood else 0)

    # if not gameState.getAgentState(self.index).isPacman:
    #   # print 'not pacman'
    #   weights['distanceToEnemyGhost'] = 0
    #   weights['distanceToEnemyPacman'] = -10
    # else:
    #   # agent is pacman
    #   weights['distanceToEnemyGhost'] = 20
    #   weights['distanceToEnemyPacman'] = 0


    return weights


  # def evaluation(self, gameState, agent):
  #   # print 'evaluating...'
  #   features = self.getFeatures(gameState, agent)
  #   weights = self.getWeights(gameState, agent)
  #   evaluation = weights * features
  #   print 'evaluation of agent', agent, ':', evaluation
  #   return evaluation
