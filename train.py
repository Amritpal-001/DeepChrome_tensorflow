import tensorflow as tf

import data
import model

def main(argv=None):
	next_element = data.get_training_data()

	x = tf.placeholder(tf.float32, [100,5])
	y = tf.placeholder(tf.float32)
	keep_prob = tf.placeholder(tf.float32)

	readout = model.get_model(x, keep_prob)

	print readout.shape
	print y.shape
	loss = tf.losses.log_loss(y, readout) ## IS THIS RIGHT?
	training_step = tf.train.AdamOptimizer(1e-4).minimize(loss)

	with tf.Session() as sess:
		print "BEGINNING TRANING..."
		sess.run(tf.global_variables_initializer())
		step = 0
		while True:
			try:
			    step += 1
			    print step
			    ex, label = sess.run(next_element)
			    sess.run(training_step, feed_dict={x: ex, y: label, keep_prob: 0.5})
			except tf.errors.OutOfRangeError:
			    print("DONE TRAINING")
			    break

if __name__ == "__main__":
	main()