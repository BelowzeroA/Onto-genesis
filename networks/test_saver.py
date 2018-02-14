import tensorflow as tf


PATH_TO_MODEL = 'c:/work/ranhiggs/purchase/dssm/storedmodel/'
def main():
    x = tf.placeholder("float", None)
    x1 = tf.placeholder("float", None, name='placeholder1')
    x2 = tf.placeholder("float", None, name='placeholder2')
    var = tf.Variable([3.0, 1.0, 2.0])
    # y = tf.add(x1 * 3, tf.add(x2 * 2, var), name='op_to_restore')
    # y = tf.losses.cosine_distance(tf.multiply(x1, x2), name='op_to_restore')
    y = tf.losses.cosine_distance(x1, x2, dim=1)

    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    # result = sess.run(y, feed_dict={x1: [1, 2, 3], x2: [[1, 2, 3], [4, 5, 6]]})
    result = sess.run(y, feed_dict={x1: [1, 2, 3], x2: [4, 5, 6]})
    print(result)

    # saver = tf.train.Saver()
    # saver.save(sess, PATH_TO_MODEL + 'simple')

def restore():
    sess = tf.Session()

    saver = tf.train.import_meta_graph(PATH_TO_MODEL + 'simple.meta')
    saver.restore(sess, tf.train.latest_checkpoint(PATH_TO_MODEL))

    graph = tf.get_default_graph()
    x1 = graph.get_tensor_by_name("placeholder1:0")
    x2 = graph.get_tensor_by_name("placeholder2:0")
    feed_dict = {x1: [5, 0, 1], x2: [[1, 2, 3], [4, 5, 6]]}

    # Now, access the op that you want to run.
    op_to_restore = graph.get_tensor_by_name("op_to_restore:0")

    result = sess.run(op_to_restore, feed_dict=feed_dict)
    print(result)

if __name__ == "__main__":
    main()
    # restore()