

from learningAgents import LearningAgent
import sys
from othello import Othello
from agents import MinimaxAgent, GreedyAgent, AlphaBetaAgent
import numpy as np
import time
import tensorflow as tf



class Environment:
    def __init__(self, rival, game, tile = 'O', render = False):
        self.game = game
        self.tile = tile
        self.rival = rival
        self.render = render

    def getState(self, board):
        myMap = [0] * 64
        rivalMap = [0] * 64
        validMoves = [0] * 64
        for x in range(8):
            for y in range(8):
                pos = x * 8 + y
                if board[x][y] == self.tile:
                    myMap[pos] = 1
                elif board[x][y] == 'O' or board[x][y] == 'X':
                    rivalMap[pos] = 1
        possibleMoves = self.game.getValidMoves(board, self.tile)
        for x, y in possibleMoves:
            pos = x * 8 + y
            validMoves[pos] = 1

        return myMap + rivalMap + validMoves


    def step(self, action):
        done = False
        game = self.game
        tile1 = 'O'
        tile2 = 'X'

        score = game.getScoreOfBoard(game.board)[self.tile]

        if self.render:
            game.drawBoard(game.board)
            game.showPoints(tile1, tile2)

        game.makeMove(game.board, tile1, action[0], action[1])
        if game.getValidMoves(game.board, tile2) == []:
            done = True

        if done == False:
            x, y = self.rival.getMove()
            game.makeMove(game.board, tile2, x, y)
            if game.getValidMoves(game.board, tile1) == []:
                done = True

        reward = game.getScoreOfBoard(game.board)[self.tile] - score
        reward /= 64
        return self.getState(game.board), reward, done

    def reset(self):
        self.game.resetBoard()




# hyperparameters
H = 10  # number of hidden layer neurons
batch_size = 5  # every how many episodes to do a param update?
learning_rate = 1e-2  # feel free to play with this to train faster or more stably.
gamma = 0.99  # discount factor for reward

D = 64*3  # input dimensionality

tf.reset_default_graph()

x = tf.placeholder(tf.float32, shape=[None, D])
y_ = tf.placeholder(tf.float32, shape=[None, 1])

W1 = tf.get_variable("W1", shape=[D, H],
           initializer=tf.contrib.layers.xavier_initializer())
h_layer1 = tf.nn.relu(tf.matmul(x,W1))

W2 = tf.get_variable("W2", shape=[H, 1],
           initializer=tf.contrib.layers.xavier_initializer())

y = tf.nn.sigmoid(tf.matmul(h_layer1, W2))

mse = tf.sqrt(tf.reduce_mean(tf.square(y_ - y)))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(mse)


sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

game = Othello()
myTile = 'O'
rivalTile = 'X'
rival = AlphaBetaAgent(rivalTile, game, 4)
env = Environment(rival, game, tile=myTile, render=False)

action = [0,0]
observation, reward, done = env.step(action)

state = env.getState(game.board)

print(state)
#TODO: make tensorflow run
# score = sess.run(y, feed_dict={x: state})


    #(reward + gamma * q(new_state)) - q(prev_state) => error















