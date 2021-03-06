# (1) Importing dependency
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten, Conv2D, MaxPooling2D,ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from sklearn.model_selection import train_test_split
import numpy as np
np.random.seed(1000)

# (2) Get Data
import tflearn.datasets.oxflower17 as oxflower17
x, y = oxflower17.load_data(one_hot=True)

########################################
#
# (1) Create Training (80%), test (20%) and validation (20%) dataset
#     Datasets (x and y) are loaded as numpy object from the previous step
x_train, x_test_pre, y_train, y_test_pre = train_test_split(x, y, test_size=0.20, random_state=42)
x_test, x_validation, y_test, y_validation = train_test_split(x_test_pre, y_test_pre, test_size=0.1)
#
# Check Shapes
print('Shape: x_train={}, y_train={}'.format(x_train.shape, y_train.shape))
print('Shape: x_test={}, y_test={}'.format(x_test.shape, y_test.shape))
print('Shape: x_validation={}, y_validation={}'.format(x_validation.shape, y_validation.shape))
#####################################

# (3) Create a sequential model
alexnet = Sequential()

img_shape=(224, 224, 3)
l2_reg=0.
# Layer 1
alexnet.add(Conv2D(96, (11, 11), input_shape=img_shape,
padding='same', kernel_regularizer=l2(l2_reg)))
alexnet.add(BatchNormalization())
alexnet.add(Activation('relu'))
alexnet.add(MaxPooling2D(pool_size=(2, 2)))

# Layer 2
alexnet.add(Conv2D(256, (5, 5), padding='same'))
alexnet.add(BatchNormalization())
alexnet.add(Activation('relu'))
alexnet.add(MaxPooling2D(pool_size=(2, 2)))

# Layer 3
alexnet.add(ZeroPadding2D((1, 1)))
alexnet.add(Conv2D(512, (3, 3), padding='same'))
alexnet.add(BatchNormalization())
alexnet.add(Activation('relu'))
alexnet.add(MaxPooling2D(pool_size=(2, 2)))

# Layer 4
alexnet.add(ZeroPadding2D((1, 1)))
alexnet.add(Conv2D(1024, (3, 3), padding='same'))
alexnet.add(BatchNormalization())
alexnet.add(Activation('relu'))

# Layer 5
alexnet.add(ZeroPadding2D((1, 1)))
alexnet.add(Conv2D(1024, (3, 3), padding='same'))
alexnet.add(BatchNormalization())
alexnet.add(Activation('relu'))
alexnet.add(MaxPooling2D(pool_size=(2, 2)))

# Layer 6
alexnet.add(Flatten())
alexnet.add(Dense(3072))
alexnet.add(BatchNormalization())
alexnet.add(Activation('relu'))
alexnet.add(Dropout(0.5))

# Layer 7
alexnet.add(Dense(4096))
alexnet.add(BatchNormalization())
alexnet.add(Activation('relu'))
alexnet.add(Dropout(0.5))

n_classes = 17
# Layer 8
alexnet.add(Dense(n_classes))
alexnet.add(BatchNormalization())
alexnet.add(Activation('softmax'))

alexnet.summary()

# (4) Compile 
alexnet.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# (5) Train
alexnet.fit(x, y, batch_size=64, epochs=1, verbose=1,  validation_split=0.2, shuffle=True)

alexnet.save_weights('alexnet.h5')
alexnet.load_weights('alexnet.h5')


#score = model.evaluate(test['features'], to_categorical(test['labels']))
score = alexnet.evaluate(x_validation, y_validation)
print('Test loss:', score[0])
print('Test accuracy:', score[1])





