import tensorflow as tf
import numpy as np


class FeedForwardNet:

    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.weights_hidden = []
        self.weights_output = []


    def init_weights(shape):
        """ Weight initialization """
        weights = tf.random_normal(shape, stddev=0.1)
        return tf.Variable(weights)


    def forwardprop(self, input):
        """
        Forward-propagation.
        IMPORTANT: yhat is not softmax since TensorFlow's softmax_cross_entropy_with_logits() does that internally.
        """
        h = tf.nn.sigmoid(tf.matmul(input, self.weights_hidden))  # The \sigma function
        yhat = tf.matmul(h, self.weights_output)  # The \varphi function
        return yhat


    def fit(self):
        # train_X, test_X, train_y, test_y = get_iris_data()

        # Layer's sizes
        x_size = self.input_size + 1 # train_X.shape[1]  # Number of input nodes: 4 features and 1 bias
        h_size = 256  # Number of hidden nodes
        y_size = self.output_size # train_y.shape[1]  # Number of outcomes (3 iris flowers)

        # Symbols
        input = tf.placeholder("float", shape=(None, x_size))
        output = tf.placeholder("float", shape=[None, y_size])

        # Weight initializations
        self.weights_hidden = init_weights((x_size, h_size))
        self.weights_output = init_weights((h_size, y_size))

        # Forward propagation
        yhat = forwardprop(input)
        predict = tf.argmax(yhat, axis=1)

        # Backward propagation
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=yhat))
        updates = tf.train.GradientDescentOptimizer(0.01).minimize(cost)

        # Run SGD
        sess = tf.Session()
        init = tf.global_variables_initializer()
        sess.run(init)

        for epoch in range(10):
            # Train with each example
            for i in range(len(train_X)):
                sess.run(updates, feed_dict={input: train_X[i: i + 1], output: train_y[i: i + 1]})

            train_accuracy = np.mean(np.argmax(train_y, axis=1) ==
                                     sess.run(predict, feed_dict={X: train_X, y: train_y}))
            test_accuracy = np.mean(np.argmax(test_y, axis=1) ==
                                    sess.run(predict, feed_dict={X: test_X, y: test_y}))

            print("Epoch = %d, train accuracy = %.2f%%, test accuracy = %.2f%%"
                  % (epoch + 1, 100. * train_accuracy, 100. * test_accuracy))

        sess.close()