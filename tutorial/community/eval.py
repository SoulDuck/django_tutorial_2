#-*- coding:utf-8 -*-
import os
import numpy as np
import tensorflow as tf
import cam


def eval(model_path ,test_images , batch_size  , actmap_folder , ):
    """
    만약 actmap folder 가 None 이면 actmap 을 저장하지 않습니다.
    actmap folder 을 지정하고 만약 해당 폴더가 없으면 생상합니다.
    모델 path은 fullpath 가 필요합니다 . E.G) /dir/model
    :param model_path:
    :param test_images:
    :param batch_size:
    :param actmap_folder:
    :return:
    """
    print '########## EVAL ##########'
    # Normalize
    if np.max(test_images) > 1:
        test_images = test_images / 255.
    # Reconstruct Model
    sess = tf.Session()
    saver = tf.train.import_meta_graph(meta_graph_or_file=model_path+'.meta') #example model path ./models/fundus_300/5/model_1.ckpt
    saver.restore(sess, save_path=model_path) # example model path ./models/fundus_300/5/model_1.ckpt
    x_ = tf.get_default_graph().get_tensor_by_name('x_:0')
    y_ = tf.get_default_graph().get_tensor_by_name('y_:0')
    pred_ = tf.get_default_graph().get_tensor_by_name('softmax:0')
    is_training_=tf.get_default_graph().get_tensor_by_name('is_training:0')
    top_conv = tf.get_default_graph().get_tensor_by_name('top_conv:0')
    logits = tf.get_default_graph().get_tensor_by_name('logits:0')
    cam_ = tf.get_default_graph().get_tensor_by_name('classmap:0')
    cam_ind = tf.get_default_graph().get_tensor_by_name('cam_ind:0')

    # Get Predictions from model.
    if not actmap_folder is None:
        if not os.path.isdir(actmap_folder):
            os.makedirs(actmap_folder)
        cam.eval_inspect_cam(sess, cam_, cam_ind, top_conv, test_images[:], x_, y_, is_training_, logits, actmap_folder)
    share=len(test_images)/batch_size
    remainder=len(test_images)%batch_size
    predList=[]
    for s in range(share):
        pred = sess.run(pred_ , feed_dict={x_ : test_images[s*batch_size:(s+1)*batch_size],is_training_:False})
        predList.extend(pred)
    if not remainder == 0:
        pred = sess.run(pred_, feed_dict={x_: test_images[-1*remainder:], is_training_: False})
        predList.extend(pred)
    assert len(predList) == len(test_images), '# pred : {} # imgaes : {} should be SAME!'.format(len(predList),
                                                                                                 len(test_images))
    # Reset Graph
    tf.reset_default_graph()
    return np.asarray(predList)