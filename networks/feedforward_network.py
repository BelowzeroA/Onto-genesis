import numpy as np
import tensorflow as tf


class FeedforwardNetwork:

    def __init__(self, input_size, output_size, hidden_sizes):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_sizes = hidden_sizes


    def _prepare_input_data(self, data):
        # Prepend the column of 1s for bias
        number_of_samples = len(data)
        X = np.ones((number_of_samples, self.input_size + 1))
        for i, sample in enumerate(data):
            X[i, 1:] = sample[0]
        return X


    def _prepare_output_data(self, data):
        vector = [sample[1] for sample in data]
        # Convert into one-hot vectors
        num_labels = len(np.unique(vector))
        Y = np.eye(num_labels)[vector]  # One liner trick!
        return Y


    def _init_weights(self, shape):
        """ Weight initialization """
        weights = tf.random_normal(shape, stddev=0.1)
        return tf.Variable(weights)


    def _init_weights_array(self):
        weights_array = []
        for i in range(len(self.hidden_sizes) + 1):
            if i == 0:
                in_size = self.input_size + 1
            else:
                in_size = self.hidden_sizes[i - 1]
            if i == len(self.hidden_sizes):
                out_size = self.output_size
            else:
                out_size = self.hidden_sizes[i]

            weights = self._init_weights((in_size, out_size))
            weights_array.append(weights)
        return weights_array


    def forwardprop(self, X, weights_array):
        """
        Forward-propagation.
        IMPORTANT: yhat is not softmax since TensorFlow's softmax_cross_entropy_with_logits() does that internally.
        """
        previous_layer = X
        for i, weights in enumerate(weights_array):
            if i == len(weights_array) - 1:
                layer = tf.matmul(previous_layer, weights)  # The \varphi function
            else:
                layer = tf.nn.sigmoid(tf.matmul(previous_layer, weights))
            previous_layer = layer
        return layer


    def fit(self, dataset, number_of_epochs=20):

        Xdata = self._prepare_input_data(dataset)
        Ydata = self._prepare_output_data(dataset)

        X = tf.placeholder("float", shape=(None, self.input_size + 1))
        y = tf.placeholder("float", shape=[None, self.output_size])

        weights_array = self._init_weights_array()

        # Forward propagation
        yhat = self.forwardprop(X, weights_array)
        predict = tf.argmax(yhat, axis=1)

        # Backward propagation
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=yhat))
        updates = tf.train.GradientDescentOptimizer(0.02).minimize(cost)

        # Run SGD
        sess = tf.Session()
        init = tf.global_variables_initializer()
        sess.run(init)

        for epoch in range(number_of_epochs):
            # Train with each example
            for i in range(len(Xdata)):
                result = sess.run(updates, feed_dict={X: Xdata[i: i + 1], y: Ydata[i: i + 1]})


