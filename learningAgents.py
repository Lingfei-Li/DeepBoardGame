

from agents import Agent
import math
import random
import numpy as np
import tensorflow as tf


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

# hyperparameters
H1 = 30  # number of hidden layer neurons
H2 = 50  # number of hidden layer neurons
batch_size = 5  # every how many episodes to do a param update?
learning_rate = 1e-2  # feel free to play with this to train faster or more stably.
discount = 0.9  # discount factor for reward

D = 64*3  # input dimensionality

tf.reset_default_graph()

x_input = tf.placeholder(tf.float32, shape=[None, D])
x_image = tf.reshape(x_input, [-1, 8, 8, 3])
y_target = tf.placeholder(tf.float32, shape=[None, 1])

#CNN:
W_conv1 = weight_variable([3, 3, 3, 32])        #param: height, width, depth, #filters
b_conv1 = bias_variable([32])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([3, 3, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([2*2*64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 2*2*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

W_fc2 = weight_variable([1024, 1])
b_fc2 = bias_variable([1])
y_output = tf.matmul(h_fc1, W_fc2) + b_fc2


#ANN:
# W1 = tf.get_variable("W1", shape=[D, H1],
#                      initializer=tf.contrib.layers.xavier_initializer())
# b1 = tf.Variable(tf.zeros([H1]))
#
# h_layer1 = tf.nn.relu(tf.matmul(x_input, W1) + b1)
#
# W2 = tf.get_variable("W2", shape=[H1, H2],
#                      initializer=tf.contrib.layers.xavier_initializer())
# b2 = tf.Variable(tf.zeros([H2]))
#
# h_layer2 = tf.nn.relu(tf.matmul(h_layer1, W2) + b2)
#
# W3 = tf.get_variable("W3", shape=[H2, 1],
#                      initializer=tf.contrib.layers.xavier_initializer())
#
# y_output = tf.nn.sigmoid(tf.matmul(h_layer2, W3))
#

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
                    if q_val[0][0] > max_q_value:
                        max_q_value = q_val[0][0]
                        max_q_action = [x, y]

        state = env.step(max_q_action, self.tile)
        reward = score - self.prev_score
        if env.done:
            scores = game.getScoreOfBoard(game.board)
            reward = 2*(scores[self.tile] - scores[self.rival_tile])
            sess.run(train_step, feed_dict={x_input: [self.prev_state], y_target: [[reward]]})
            return -1, -1

        if not self.prev_state is None:
            sess.run(train_step, feed_dict={x_input: [self.prev_state], y_target: [[reward + discount * max_q_value]]})

        self.prev_score = score
        self.prev_state = state

        return max_q_action


