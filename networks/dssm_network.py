import numpy as np
import tensorflow as tf


class DssmNetwork:

    def __init__(self, input_size, output_size, hidden_sizes, rand_seed=42):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_sizes = hidden_sizes
        self.session = None
        self.yhat = None
        self.y = None
        self.placeholderX = None
        self.session = tf.Session()
        tf.set_random_seed(rand_seed)


    def _prepare_input_data(self, data):
        number_of_samples = len(data)
        X = np.zeros((number_of_samples, self.input_size))
        for i, sample in enumerate(data):
            if isinstance(sample, tuple):
                X[i,:] = sample[0]
            else:
                X[i,:] = sample
        return X


    def _prepare_output_data(self, data):
        Y = np.array([sample[1] for sample in data])
        return Y


    def _init_weights(self, shape):
        """ Weight initialization """
        weights = tf.random_normal(shape, stddev=0.1)
        return tf.Variable(weights)


    def _init_biases(self):
        biases = []
        for i in range(len(self.hidden_sizes) + 1):
            if i == len(self.hidden_sizes):
                in_size = self.output_size
            else:
                in_size = self.hidden_sizes[i]
            var = tf.Variable(tf.random_normal([in_size]))
            biases.append(var)
        return biases


    def _init_weights_array(self):
        weights_array = []
        for i in range(len(self.hidden_sizes) + 1):
            if i == 0:
                in_size = self.input_size
            else:
                in_size = self.hidden_sizes[i - 1]
            if i == len(self.hidden_sizes):
                out_size = self.output_size
            else:
                out_size = self.hidden_sizes[i]

            weights = self._init_weights((in_size, out_size))
            weights_array.append(weights)
        return weights_array


    def forwardprop(self, X, weights_array, biases_array):
        previous_layer = X
        for i, (weights, biases) in enumerate(zip(weights_array, biases_array)):
            if i == len(weights_array) - 1:
                # layer = tf.matmul(previous_layer, weights, name='output')  # The \varphi function
                layer = tf.add(tf.matmul(previous_layer, weights), biases, name='output')
            else:
                layer = tf.add(tf.matmul(previous_layer, weights), biases)
                # layer = tf.nn.sigmoid(tf.matmul(previous_layer, weights))
            previous_layer = layer
        return layer


    def init_base_variables(self):
        self.placeholderX = tf.placeholder("float", shape=(None, self.input_size))
        self.y = tf.placeholder("float", shape=[None, self.output_size])

        weights_array = self._init_weights_array()
        biases_array = self._init_biases()

        # Forward propagation
        self.final_vector1 = self.forwardprop(self.placeholderX, weights_array, biases_array)
        self.final_vector2 = self.forwardprop(self.placeholderX, weights_array, biases_array)
        # self.cosine = tf.losses.cosine_distance(self.final_vector1, self.final_vector2)


    def fit(self, dataset, number_of_epochs=20):
        Xdata = self._prepare_input_data(dataset)
        Ydata = self._prepare_output_data(dataset)

        self.init_base_variables()

        # Backward propagation
        # cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.y, logits=self.yhat))
        # self.cost = tf.losses.cosine_distance(self.final_vector1, self.final_vector2, dim=1)
        self.cost = tf.reduce_sum(tf.multiply(self.final_vector1, self.final_vector2))
        updates = tf.train.GradientDescentOptimizer(0.01).minimize(self.cost)
        # updates = tf.train.AdamOptimizer(0.01).minimize(cost)

        # predict = tf.argmax(self.yhat, axis=1)

        # Run SGD
        init = tf.global_variables_initializer()
        self.session.run(init)

        for epoch in range(number_of_epochs):
            # Train with each example
            for i in range(len(Xdata)):
                result = self.session.run(updates, feed_dict={self.placeholderX: Xdata[i: i + 1],
                                                              self.y: Ydata[i: i + 1]})
            # train_accuracy = np.mean(np.argmax(Ydata, axis=1) == self.session.run(predict,
            #     feed_dict={self.placeholderX: Xdata, self.y: Ydata}))
            #
            # if epoch % 10 == 0:
            #     print("Epoch = %d, train accuracy = %.2f%%"  % (epoch + 1, 100. * train_accuracy))


    def predict(self, dataset):
        # self.placeholderX = tf.placeholder("float", shape=(None, self.input_size + 1), name='input')
        # predict = tf.argmax(self.yhat, axis=1)
        # init = tf.global_variables_initializer()
        # self.session.run(init)

        # output_layer = tf.get_default_graph().get_operation_by_name(name='output')
        output_layer = tf.get_default_graph().get_tensor_by_name('output:0')
        output = tf.nn.softmax(self.yhat)
        Xdata = self._prepare_input_data(dataset)

        result = self.session.run(output, feed_dict={self.placeholderX: Xdata})
        return result


    def save_model(self, save_path, model_name):
        if not save_path[-1:] in ['\\', '/']:
            save_path += '/'
        saver = tf.train.Saver()
        saver.save(self.session, save_path + model_name)


    def load_model(self, save_path, model_name):
        if not save_path[-1:] in ['\\', '/']:
            save_path += '/'
        saver = tf.train.import_meta_graph(save_path + model_name + '.meta')
        saver.restore(self.session, tf.train.latest_checkpoint(save_path))
