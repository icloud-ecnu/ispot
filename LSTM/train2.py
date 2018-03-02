import tensorflow as tf
import numpy as np
import math
import random
import sys
import os


total = 0

# read data
train_data = []
test_data = []

with open(sys.argv[1]+'/1'+sys.argv[2]+'-train.txt') as f:
    for line in f:
        train_data.append(float(line))
        total+=1
with open(sys.argv[1]+'/1'+sys.argv[2]+'-test.txt') as f:
    for line in f:
        test_data.append(float(line))
    test_data.append(float(0))

print 'len of test data',len(test_data)

def get_batch(batch_size):
    batch_x = np.ndarray([batch_size,n_steps*n_input],np.float32)
    batch_y = np.ndarray([batch_size,1],np.float32)
    for i in range(batch_size):
        s = random.randint(0,total-n_steps*n_input-2)
        for j in range(n_steps*n_input):
            batch_x[i,j] = train_data[s+j]
        # print s,n_steps*n_input
        batch_y[i,0]=train_data[s+n_steps*n_input]
    return batch_x, batch_y


def test_batch():
    size = len(test_data) - n_input*n_steps
    batch_x = np.ndarray([size,n_input*n_steps],np.float32)
    batch_y = np.ndarray([size,1],np.float32)
    for i in range(size):
        for j in range(n_input*n_steps):
            batch_x[i,j] = test_data[i+j]
        batch_y[i,0] = test_data[i+n_input*n_steps]
    return batch_x,batch_y


# parameter
lr = 0.001
steps = 6000
batch_size = 256
n_steps = 20
n_input = 1
n_hidden = 32

x = tf.placeholder(tf.float32,[None,n_steps*n_input])
y = tf.placeholder(tf.float32,[None,1])

w = tf.Variable(tf.random_normal([n_hidden,1]))

b = tf.Variable(tf.zeros([1]))


# net
def net(x,w,b):
    x = tf.reshape(x,[-1,n_steps,n_input])
    x = tf.transpose(x,[1,0,2])
    x = tf.reshape(x,[-1,n_input])
    #x = tf.split(0, n_steps, x)
    x = tf.split(x, n_steps, 0)

    lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(n_hidden,state_is_tuple=True)
    #outputs, states = tf.nn.rnn(lstm_cell, x, dtype=tf.float32)
    outputs, states = tf.contrib.rnn.static_rnn(lstm_cell, x, dtype=tf.float32)
    return tf.matmul(outputs[-1], w) + b


pred = net(x,w,b)
cost = tf.reduce_mean(tf.abs(pred-y)/y)
train = tf.train.AdamOptimizer(lr).minimize(cost)

init = tf.global_variables_initializer()
saver = tf.train.Saver()


# train and test
with tf.Session() as sess:
    sess.run(init)
    test_x,test_y = test_batch()
    for step in range(steps+1):
        batch_x,batch_y = get_batch(batch_size)
        _,cost_val = sess.run([train,cost],feed_dict={x:batch_x,y:batch_y})
        if step % 1200 == 0 and step>0:
            pred_val,cost_val = sess.run([pred,cost],feed_dict={x:test_x,y:test_y})
            print "acc",cost_val,'at step',step
            type=sys.argv[1]
            dir = os.path.join('model2', type[-2:], sys.argv[2])
            if not os.path.exists(dir):
                os.makedirs(dir)
            save_path = os.path.join(dir, 'model.cpkt')
            print 'save model at',save_path
            saver.save(sess,save_path)
    print 'finished!!!'
    with open(os.path.join(sys.argv[1], '2-'+sys.argv[2]+'-pred.csv'), 'w') as f:
        #f.writelines('real,prediction\n')
        '''
        for i in range(len(test_data)-n_steps*n_input):
            f.writelines("%f,%f\n"%(test_data[i+n_steps*n_input], pred_val[i,0]))
        '''
        f.writelines("%f\n"%pred_val[0,0])
        #print pred_val
    print 'final accuracy',cost_val
