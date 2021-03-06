#!usr/local/env python
#!coding:utf-8
# here our network is still the last one in firstNN_05
# however, we are going to visualize whole net structure and training process
# Nework architecture: input_layer_size = 1, hiddden_layer_size = 10, outpit_layer_size = 1
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

# basic procedure for net construction
def add_layer(inputs, in_size, out_size, layer_name = 'layer', active_fun = lambda x: x):
    """ function to add a layer into NN """
    with tf.name_scope(layer_name):
        with tf.name_scope('weights'):
            weights = tf.Variable(tf.random_normal([in_size, out_size]), name = 'W')
        with tf.name_scope('biases'):
            biases = tf.Variable(tf.zeros([1, out_size]) + 0.1, name = 'b')
        with tf.name_scope('Wx'):
            linear_struct = tf.add(tf.matmul(inputs, weights), biases)
        outputs = active_fun(linear_struct)
        return outputs

# set placeholders
with tf.name_scope('inputs'):
    x_in = tf.placeholder(tf.float32, [None, 1], name = 'x_in')
    y_in = tf.placeholder(tf.float32, [None, 1], name = 'y_in')

# add a hidden layer
hd_1 = add_layer(x_in, 1, 10, 'hidden_layer', active_fun = tf.nn.relu)

# add output layer
pred = add_layer(hd_1, 10, 1, 'output_layer')

# loss function, L2
# understand parameter reduction_indicates, just like numpy axis
with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(y_in - pred), reduction_indices = [1]))
    
# set lr = 0.1
with tf.name_scope('train'):
    train = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

# create some phony data
X_tr = np.linspace(-1, 1, 300)[:, np.newaxis] # np.linspace, np.newaxis
noise = np.random.normal(0, 0.05, X_tr.shape)
y_tr = np.square(X_tr) - 0.5 + noise # suppose the data set satisfy 2-level relationship

# initialize all variables
init = tf.global_variables_initializer()

# scatter graph of data
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(X_tr, y_tr)
plt.ion() # told plt to show images in sequence
plt.show()

# note that x_in and y_in will be changed in training steps
data_dict = {x_in: X_tr, y_in: y_tr}
with tf.Session() as sess:
    sess.run(init)
    for it in range(1000 + 1):
        sess.run(train,data_dict)
        if it % 50 == 0:
            if 'lines' in locals().keys():
                ax.lines.remove(lines[0])
            # calculate prediction value
            predict_val = sess.run(pred, feed_dict = {x_in: X_tr})
            # plot the prediction on graph
            lines = ax.plot(X_tr, predict_val, 'r-', lw = 5)
            plt.pause(0.1) # pause 0.1s 
            print('iter = %d, loss = '%(it), sess.run(loss, data_dict))
    plt.ioff()
    plt.show()
    # write things on tensorboard
    tf.summary.FileWriter("logs/", sess.graph)

    


