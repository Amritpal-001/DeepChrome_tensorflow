import tensorflow as tf
import math

EXAMPLE_WIDTH = 100
NUM_CONV_FILTERS = 50
CONV_FILTER_SIZE = 10
POOLING_SIZE = 5
FIRST_FC_LAYER_NODE_COUNT = 625
SECOND_FC_LAYER_NODE_COUNT = 125

def get_model(x, keep_prob):
	def weight_variables(shape, name="weights"):
		with tf.name_scope('weights'):
			return tf.get_variable(name, shape, 
				initializer=tf.truncated_normal_initializer(stddev=.1))
	def bias_variables(shape):
		with tf.name_scope('biases'):
			return tf.get_variable("biases", shape, 
				initializer=tf.constant_initializer(0.1))
	def conv_layer(inputs, filter_shape):
		with tf.name_scope('conv'):
			return tf.nn.conv1d(inputs, filter_shape, stride=1,
					padding='VALID')
	def pooling_layer(inputs):
		with tf.name_scope('pool'):
			return tf.nn.pool(inputs, window_shape=[POOLING_SIZE], pooling_type='MAX',
					padding='VALID', strides=[POOLING_SIZE])
	with tf.name_scope('initialize'):
	    # Add a dimension to the input for multiple convolutional layers.
		 example = tf.expand_dims(tf.transpose(x), [-1])

	with tf.variable_scope('conv'):
		# 1-D convolution + pooling
		conv_weights = weight_variables([CONV_FILTER_SIZE, 1, NUM_CONV_FILTERS])
		conv_biases = bias_variables([NUM_CONV_FILTERS])

		conv = tf.nn.relu(conv_layer(example, conv_weights) + conv_biases)
		pool = pooling_layer(conv)

	with tf.variable_scope('dropout'):
		total_nodes = ((EXAMPLE_WIDTH - CONV_FILTER_SIZE) / POOLING_SIZE) * NUM_CONV_FILTERS # 900
		pool_flat = tf.reshape(pool, [-1, total_nodes])

		dropout_layer = tf.nn.dropout(pool_flat, keep_prob)

	with tf.variable_scope('first_fc_layer'):
		first_fc_weights = weight_variables([total_nodes, FIRST_FC_LAYER_NODE_COUNT])
		first_fc_biases = bias_variables([FIRST_FC_LAYER_NODE_COUNT])
		first_fc_layer = tf.nn.relu(tf.matmul(dropout_layer, first_fc_weights) + first_fc_biases)

	with tf.variable_scope('second_fc_layer'):
		second_fc_weights = weight_variables([FIRST_FC_LAYER_NODE_COUNT, SECOND_FC_LAYER_NODE_COUNT])
		second_fc_biases = bias_variables([SECOND_FC_LAYER_NODE_COUNT])
		second_fc_layer = tf.nn.relu(tf.matmul(first_fc_layer, second_fc_weights) + second_fc_biases)

	with tf.variable_scope('readout'):
		readout_weights = weight_variables([SECOND_FC_LAYER_NODE_COUNT, 1])
		readout_biases = bias_variables([1])
		readout = tf.matmul(second_fc_layer, readout_weights) + readout_biases

	return readout
