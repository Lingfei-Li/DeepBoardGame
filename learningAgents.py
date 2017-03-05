

from agents import Agent
import math
import random
import numpy as np
import tensorflow as tf

# hyperparameters
H = 30  # number of hidden layer neurons
batch_size = 5  # every how many episodes to do a param update?
learning_rate = 1e-2  # feel free to play with this to train faster or more stably.
discount = 0.9  # discount factor for reward

D = 64*3  # input dimensionality

tf.reset_default_graph()

x_input = tf.placeholder(tf.float32, shape=[None, D])
y_target = tf.placeholder(tf.float32, shape=[None, 1])

W1 = tf.get_variable("W1", shape=[D, H],
                     initializer=tf.contrib.layers.xavier_initializer())
h_layer1 = tf.nn.relu(tf.matmul(x_input, W1))

W2 = tf.get_variable("W2", shape=[H, 1],
                     initializer=tf.contrib.layers.xavier_initializer())

y_output = tf.nn.sigmoid(tf.matmul(h_layer1, W2))

mse = tf.sqrt(tf.reduce_mean(tf.square(y_target - y_output)))

train_step = tf.train.AdamOptimizer(1e-4).minimize(mse)

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

print("Learning agent variables init compeleted")

prev_score = 0
prev_state = None

class LearningAgent(Agent):
    def __init__(self, tile, game, env):
        super(LearningAgent, self).__init__(tile, game)
        self.env = env
        self.prev_state = None
        self.prev_score = 0
        self.rival_tile = 'O' if tile=='X' else 'X'

    def train_step(self):
        game = self.game
        env = self.env
        if env.done:
            scores = game.getScoreOfBoard(game.board)
            reward = 2*(scores[self.tile] - scores[self.rival_tile])
            sess.run(train_step, feed_dict={x_input: [self.prev_state], y_target: [[reward]]})
            return -1, -1
        state = env.getState(game.board, self.tile)
        score = game.getScoreOfBoard(game.board)[self.tile]
        max_q_value = -1
        max_q_action = [-1, -1]
        valid_moves = np.reshape(state, (3, 8, 8))[2]
        for x in range(8):
            for y in range(8):
                if valid_moves[x][y] == 1:
                    board = game.getCopyOfBoardAfterMove(game.board, self.tile, x, y)
                    next_state = env.getState(board, self.tile)
                    q_val = sess.run(y_output, feed_dict={x_input: [next_state]})
                    if q_val > max_q_value:
                        max_q_value = q_val[0]
                        max_q_action = [x, y]

        state = env.step(max_q_action, self.tile)
        reward = score - self.prev_score
        if env.done:
            scores = game.getScoreOfBoard(game.board)
            reward = 2*(scores[self.tile] - scores[self.rival_tile])
            sess.run(train_step, feed_dict={x_input: [self.prev_state], y_target: [[reward]]})
            return -1, -1

        if not self.prev_state is None:
            sess.run(train_step, feed_dict={x_input: [self.prev_state], y_target: [reward + discount * max_q_value]})

        self.prev_score = score
        self.prev_state = state

        return max_q_action


# while True:
#     if env.done:
#         scores = game.getScoreOfBoard(game.board)
#         reward = 2*(scores[myTile] - scores[rivalTile])
#         sess.run(train_step, feed_dict={x: prev_state, y_: reward})
#         break
#
#     state = [env.getState(game.board, myTile)]
#     score = game.getScoreOfBoard(game.board)[myTile]
#
#     max_q_value = -1
#     max_q_action = [-1, -1]
#     valid_moves = np.reshape(state, (3, 8, 8))[2]
#     for x in range(8):
#         for y in range(8):
#             if valid_moves[x][y] == 1:
#                 board = game.getCopyOfBoardAfterMove(game.board, myTile, x, y)
#                 state = [env.getState(board, myTile)]
#                 q_val = sess.run(y, feed_dict={x: state})
#                 if q_val > max_q_value:
#                     max_q_value = q_val
#                     max_q_action = [x, y]
#
#     state = env.step(max_q_action, myTile)
#
#     reward = score - prev_score
#     if env.done:
#         scores = game.getScoreOfBoard(game.board)
#         reward = 2*(scores[myTile] - scores[rivalTile])
#         sess.run(train_step, feed_dict={x: prev_state, y_: reward})
#         break
#
#     if not prev_state is None:
#         sess.run(train_step, feed_dict={x: prev_state, y_: reward + discount * max_q_value})
#
#     prev_score = score
#     prev_state = state
