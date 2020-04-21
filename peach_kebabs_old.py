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
               first = 'OffensiveMiniMaxAgent', second = 'DefensiveMiniMaxAgent'):
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
    print 'registering initial state...'

    print 'start positions:', gameState.getAgentPosition(self.index), gameState.getAgentPosition((self.index + 2) % 4)

    # self.startingFoodAmount = gameState.getRedFood() if self.red else gameState.getBlueFood()

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """

    # TODO: get true agent counts
    totalAgents = 4
    myAgents = 2
    depth = myAgents * 4
    currAgentNum = 0

    print 'red agents:', gameState.getRedTeamIndices()
    print 'blue agents:', gameState.getBlueTeamIndices()

    legalActions = gameState.getLegalActions(self.index)
    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)

    values = { action : self.minimax(gameState.generateSuccessor(self.index, action), depth - 1, self.index, totalAgents) for action in legalActions }

    # successors = { (gameState.generateSuccessor(self.index, action)) : action for action in legalActions }
    # values = { (successorState) : (self.minimax(successorState, depth-1, self.index, totalAgents)) for successorState, action in successors.items() }
    # max_key = max(values.iteritems(), key=operator.itemgetter(1))[0]

    print 'values chooseAction:', values
    max_item = max(values.iteritems(), key=operator.itemgetter(1))
    print ('OFFENSIVE' if isinstance(self, OffensiveMiniMaxAgent) else 'DEFENSIVE'), 'chosen action:', max_item
    return max_item[0]


  def minimax(self, gameState, depth, agent, numAgents):
    
    print 'depth:', depth, ' agent:', agent, ' numAgents:', numAgents

    if depth == 0 or self.getFood(gameState).count() <= 2:
      print 'depth == 0'
      time.sleep(0.2)
      return self.evaluation(gameState, agent)
    else:

      actions = gameState.getLegalActions(agent)
      if Directions.STOP in actions:
        actions.remove(Directions.STOP)

      values = {}
      for action in actions:
        minimax_val = self.minimax(gameState.generateSuccessor(agent, action), depth-1, (agent+2)%numAgents, numAgents)
        print 'minimax_val:', minimax_val
        key = [action]
        if isinstance(minimax_val, list):
          key[pos:pos] = minimax_val[0]
        if key in values:
          values[key] += minimax_val[1]
        else:
          values[key] = minimax_val[1]

      # values = { [action] : self.minimax(gameState.generateSuccessor(agent, action), depth - 1, (agent+2) % numAgents, numAgents) for action in actions }
      print 'values minimax:', values
      max_item = max(values.iteritems(), key=operator.itemgetter(1))

      return max_item

      # successors = { (gameState.generateSuccessor(agent, action)) : action for action in actions }
      # if gameState.isOnRedTeam(agent) == self.red:
      #   values = {}
      #   print 'depth:', depth, ' agent:', agent, ' numAgents:', numAgents, ' | successors:', successors
      #   for nextGameState, action in successors.items():
      #     d = depth - 1
      #     a = (agent + 2) % numAgents
      #     n = numAgents
      #     values[nextGameState] = self.minimax(nextGameState, d, a, n)
      #     print 'minimax(nextGameState,', d, ',', a, ',', n, ') =', values[nextGameState], ' with action:', action

      #   print 'values dictionary:', values
      #   max_item = max(values.iteritems(), key=operator.itemgetter(1))
      #   print 'max_item:', max_item
      #   temp = { successors[max_item[0]] : max_item[1] }
      #   print 'returning:', temp
      #   return temp


  def isEnemyGhost(self, gameState, agent):
    isRedAgent = gameState.isOnRedTeam(agent)
    agentPosition = gameState.getAgentPosition(agent)
    isRedPosition = gameState.isRed(agentPosition)
    return isRedAgent == isRedPosition


  # TODO: implement evaluation function
  def evaluation(self, gameState, agent):
    # print 'evaluating...'
    features = self.getFeatures(gameState, agent)
    weights = self.getWeights(gameState, agent)
    evaluation = weights * features
    print 'evaluation of agent', agent, ':', evaluation
    return evaluation



class OffensiveMiniMaxAgent(ReflexAgent):

  def getFeatures(self, gameState, agent):

    # print 'color:', gameState.getAgentState(agent)

    print 'offensive index:', self.index

    features = util.Counter()

    agentStateData = gameState.getAgentState(agent)
    agentPosition = agentStateData.getPosition()
    isRedAgent = gameState.isOnRedTeam(agent)

    print 'agent position:', agentPosition

    enemy_indices = gameState.getBlueTeamIndices() if isRedAgent else gameState.getRedTeamIndices()
    foodList = (gameState.getBlueFood() if isRedAgent else gameState.getRedFood()).asList()

    features['distanceToGhost'] = min(self.getMazeDistance(agentPosition, gameState.getAgentPosition(enemy_index)) for enemy_index in enemy_indices if not gameState.getAgentState(enemy_index).isPacman)
    features['numFoodLeft'] = len(gameState.getRedFood().asList() if self.red else gameState.getBlueFood().asList())
    features['distanceToNearestFood'] = min( [self.getMazeDistance(agentPosition, food) for food in foodList] )
    features['numCapsulesLeft'] = len(gameState.getRedCapsules() if self.red else gameState.getBlueCapsules())

    # time.sleep(5)
    # print agent, 'getting features:', features

    print 'offensive features:', features
    return features
  

  def getWeights(self, gameState, agent):
    weights = util.Counter({
      'distanceToGhost' : 30,
      'numFoodLeft' : -15,
      'distanceToNearestFood' : -1000,
      'numCapsulesLeft' : -10
    })

    if not gameState.getAgentState(agent).isPacman:
      weights['distanceToGhost'] = 0

    return weights


class DefensiveMiniMaxAgent(ReflexAgent):
  
  def getFeatures(self, gameState, agent):
    # print 'getting features for defensive agent'

    # features = util.Counter()

    # myState = successor.getAgentState(self.index)
    # myPos = myState.getPosition()

    # # Computes whether we're on defense (1) or offense (0)
    # features['onDefense'] = 1
    # if myState.isPacman: features['onDefense'] = 0

    # # Computes distance to invaders we can see
    # enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    # invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    # features['numInvaders'] = len(invaders)
    # if len(invaders) > 0:
    #   dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
    #   features['invaderDistance'] = min(dists)

    # if action == Directions.STOP: features['stop'] = 1
    # rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    # if action == rev: features['reverse'] = 1

    # return features

    print 'defensive index:', self.index, ' current index:', agent

    features = util.Counter()

    agentStateData = gameState.getAgentState(agent)
    agentPosition = agentStateData.getPosition()
    isRedAgent = gameState.isOnRedTeam(agent)

    enemy_indices = gameState.getBlueTeamIndices() if isRedAgent else gameState.getRedTeamIndices()
    foodList = (gameState.getBlueFood() if isRedAgent else gameState.getRedFood()).asList()

    enemies = [gameState.getAgentState(i) for i in enemy_indices]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    
    print 'defensive agent position:', agentPosition

    features['defense'] = 1
    if agentStateData.isPacman: features['defense'] = 0
    
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(agentPosition, a.getPosition()) for a in invaders]
      features['distanceToInvader'] = min(dists)

    features['distanceToInvader'] = min(self.getMazeDistance(agentPosition, gameState.getAgentPosition(enemy_index)) for enemy_index in enemy_indices if enemy_index)
    # features['numFoodLeft'] = len(gameState.getRedFood().asList() if self.red else gameState.getBlueFood().asList())
    # features['distanceToNearestFood'] = min( [self.getMazeDistance(agentPosition, food) for food in foodList] )
    # features['numCapsulesLeft'] = len(gameState.getRedCapsules() if self.red else gameState.getBlueCapsules())

    # time.sleep(5)
    # print 'getting features:', features

    # return util.Counter({'numInvaders' : 0})

    print 'defensive features:', features
    return features


  def getWeights(self, gameState, agent):
    
    # return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}

    return util.Counter({
      'defend': 100,
      'numInvders' : -50,
      'distanceToInvader': -100
    })


  # def chooseAction(self, gameState):
  #   """
  #   Picks among actions randomly.
  #   """

  #   numAgents = gameState.getNumAgents()
  #   depth = numAgents * 4
  #   actions = gameState.getLegalActions(self.index)
    
  #   successors = [ (gameState.generateSuccessor(self.index, action)) for action in actions ]
  #   # print 'successors:', successors

  #   '''
  #   You should change this in your own agent.
  #   '''

  #   print 'choosing defensive action'

  #   time.sleep(0.5)
  #   return random.choice(actions)


  # # implement evaluation function
  # def evaluation(self, state):
  #   # temporary value
  #   return 100


  # def minimax(self, gameState, depth, maximizingPlayer):
  #   if depth == 0 or 'state.gameOver()':
  #     return self.evaluation(state)

