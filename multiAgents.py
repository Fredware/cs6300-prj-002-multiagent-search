# multiAgents.py
# Submission by:
#   Fredi R. Mino
#   u1424875
#
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


def compute_point_distance(point_a, point_b):
    """
    Calculates the l2-norm between two tuples
    """
    return sum((x1 - x2) ** 2 for x1, x2 in zip(point_a, point_b)) ** 0.5


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        food_positions = [(i, j) for i, row in enumerate(newFood) for j, is_food in enumerate(row) if is_food]
        food_distances = [compute_point_distance(newPos, food_position) for food_position in food_positions]
        ghost_positions = [ghost_state.getPosition() for ghost_state in newGhostStates]
        ghost_distances = [compute_point_distance(newPos, ghost_position) for ghost_position in ghost_positions]

        successor_score = successorGameState.getScore()
        # Avoid action if it results in death
        if successorGameState.isLose():
            return 0
        # Heavily encourage action if it results in win
        if successorGameState.isWin():
            successor_score += 1000
        # Encourage action if it results in food
        successor_score += 100.0 / (successorGameState.getNumFood() + 1)
        # Encourage action if it results in eaten capsule
        successor_score += 50.0 / (len(currentGameState.getCapsules())+1)
        # Discourage actions that increase distance between pacman and closest food pellet
        if food_distances:
            successor_score += 10.0 / min(food_distances)
        # Discourage actions that reduce distance between pacman and closest ghost
        if ghost_distances:
            successor_score += min(ghost_distances) / 10.0
        return successor_score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        print(gameState.getNumAgents())
        action, reward = self.get_minimax_solution(gameState, self.depth, 0)
        print(action, reward)
        return action

    def get_minimax_solution(self, gameState, depth, agent_id):
        if depth == 0 or self.is_terminal(gameState):
            return None, self.evaluationFunction(gameState)  # (action, reward) tuple

        if agent_id == 0:
            max_val = float("-inf")
            max_action = None
            for action in gameState.getLegalActions(agent_id):
                successor_state = gameState.generateSuccessor(agent_id, action)
                _, val = self.get_minimax_solution(successor_state, depth, (agent_id + 1) % gameState.getNumAgents())
                if val > max_val:
                    max_val = val
                    max_action = action
            return max_action, max_val

        else:
            min_val = float("inf")
            min_action = None
            for action in gameState.getLegalActions(agent_id):
                successor_state = gameState.generateSuccessor(agent_id, action)
                if agent_id == gameState.getNumAgents() - 1:
                    _, val = self.get_minimax_solution(successor_state, depth - 1,
                                                       (agent_id + 1) % gameState.getNumAgents())
                else:
                    _, val = self.get_minimax_solution(successor_state, depth,
                                                       (agent_id + 1) % gameState.getNumAgents())
                if val < min_val:
                    min_val = val
                    min_action = action
            return min_action, min_val

    def is_terminal(self, gameState):
        return gameState.isWin() or gameState.isLose()



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        action, reward = self.get_ab_solution(gameState, self.depth, 0, float("-inf"), float("inf"))
        print(action, reward)
        return action

    def get_ab_solution(self, gameState, depth, agent_id, alpha, beta):
        if depth == 0 or self.is_terminal(gameState):
            return None, self.evaluationFunction(gameState)  # (action, reward) tuple

        if agent_id == 0:
            max_val = float("-inf")
            max_action = None
            for action in gameState.getLegalActions(agent_id):
                successor_state = gameState.generateSuccessor(agent_id, action)
                _, val = self.get_ab_solution(successor_state, depth, (agent_id + 1) % gameState.getNumAgents(), alpha, beta)
                if val > max_val:
                    max_val = val
                    max_action = action
                alpha = max(alpha, val)
                if alpha > beta:
                    break
            return max_action, max_val

        else:
            min_val = float("inf")
            min_action = None
            for action in gameState.getLegalActions(agent_id):
                successor_state = gameState.generateSuccessor(agent_id, action)
                if agent_id == gameState.getNumAgents() - 1:
                    _, val = self.get_ab_solution(successor_state, depth - 1,
                                                       (agent_id + 1) % gameState.getNumAgents(), alpha, beta)
                else:
                    _, val = self.get_ab_solution(successor_state, depth,
                                                       (agent_id + 1) % gameState.getNumAgents(), alpha, beta)
                if val < min_val:
                    min_val = val
                    min_action = action
                beta = min(beta, val)
                if alpha > beta:
                    break
            return min_action, min_val

    def is_terminal(self, gameState):
        return gameState.isWin() or gameState.isLose()



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        action, reward = self.get_expectimax_solution(gameState, self.depth, 0)
        print(action, reward)
        return action

    def get_expectimax_solution(self, gameState, depth, agent_id):
        if depth == 0 or self.is_terminal(gameState):
            return None, self.evaluationFunction(gameState)  # (action, reward) tuple

        if agent_id == 0:
            max_val = float("-inf")
            max_action = None
            for action in gameState.getLegalActions(agent_id):
                successor_state = gameState.generateSuccessor(agent_id, action)
                _, val = self.get_expectimax_solution(successor_state, depth, (agent_id + 1) % gameState.getNumAgents())
                if val > max_val:
                    max_val = val
                    max_action = action
            return max_action, max_val

        else:
            mean_val = []
            min_action = None
            for action in gameState.getLegalActions(agent_id):
                successor_state = gameState.generateSuccessor(agent_id, action)
                if agent_id == gameState.getNumAgents() - 1:
                    _, val = self.get_expectimax_solution(successor_state, depth - 1,
                                                       (agent_id + 1) % gameState.getNumAgents())
                else:
                    _, val = self.get_expectimax_solution(successor_state, depth,
                                                       (agent_id + 1) % gameState.getNumAgents())
                mean_val.append(val)
            mean_val = sum(mean_val) / len(mean_val)
            return min_action, mean_val

    def is_terminal(self, gameState):
        return gameState.isWin() or gameState.isLose()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    My state value is equal to the current score + the immediate future expected reward over all legal actions in the
    current state.
    For the future reward, I care about 4 things in the following order:
        1) Prioritize eating all the food
        2) When possible, eat the pellets. It gives you protection against ghosts
        3) If given the chance, simplify the game by eating a ghost
        4) Add a small bias towards the closest food source
    Therefore my reward is a weighted linear combination of these features. My weights are separated by an order
        of magnitude or a factor of 2 depending on the priority of each feature.
    """
    "*** YOUR CODE HERE ***"
    current_score = currentGameState.getScore()
    future_expected_score = 0
    legal_actions = currentGameState.getLegalPacmanActions()
    if legal_actions:
        for action in legal_actions:
            successor_state = currentGameState.generatePacmanSuccessor(action)
            if successor_state.isLose():
                continue
            if successor_state.isWin():
                future_expected_score += 1000
            # Easy features
            remaining_food = successor_state.getNumFood()
            remaining_pellets = len(successor_state.getCapsules())
            remaining_agents = successor_state.getNumAgents()  # Don't count pacman
            print(remaining_food, remaining_pellets, remaining_agents)
            future_expected_score += (100.0/(remaining_food+1) + 50.0/(remaining_pellets+1) + 10.0/remaining_agents)

            # Distance-based feature
            pacman_position = successor_state.getPacmanPosition()
            food_grid = successor_state.getFood()
            food_positions = [(i, j) for i, row in enumerate(food_grid) for j, is_food in enumerate(row) if is_food]
            food_distances = [compute_point_distance(pacman_position, food_position) for food_position in food_positions]
            if food_distances:
                future_expected_score += 5.0/min(food_distances)
        future_expected_score = future_expected_score/len(legal_actions)
    return current_score + future_expected_score


# Abbreviation
better = betterEvaluationFunction
