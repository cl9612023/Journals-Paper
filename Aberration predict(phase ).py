# %tensorflow_version 1.x
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Input, Conv2D, MaxPooling2D, Activation,concatenate
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.layers.convolutional import  AveragePooling2D
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import gc
from math import pi
import random
#Google Cloud permissions
from google.colab import drive
drive.mount('/content/drive')



#(x,y) to (r,theta)
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

#定義32階係數的名稱a1-a32
column_names = []
for i in range(0,32,1):
  i = str(i+1)
  a = 'a'+i
  column_names.append(a)
print(column_names)

#產生相位資訊
def phase(rho,theta,c):
    phi =c[0,0]*1 \
            +c[0,1]* 2 * rho * np.sin(theta) \
            +c[0,2]* 2 * rho * np.cos(theta)\
            +c[0,3]*np.sqrt(6)*rho**2 * np.sin(2*theta)\
            +c[0,4]*np.sqrt(3)*(2*rho**2 - 1)\
            +c[0,5]*np.sqrt(6)*rho**2 * np.cos(2*theta)\
            +c[0,6]*np.sqrt(8)*rho**3 * np.sin(3*theta)\
            +c[0,7]*np.sqrt(8)*(3*rho**3 - 2*rho) * np.sin(theta)\
            +c[0,8]*np.sqrt(8)*(3*rho**3 - 2*rho) * np.cos(theta)\
            +c[0,9]*np.sqrt(8)*rho**3 * np.cos(3*theta)\
            +c[0,10]*np.sqrt(10)*rho**4* np.sin(4*theta)\
            +c[0,11]*np.sqrt(10)*(4*rho**4 - 3*rho**2) * np.sin(2*theta)\
            +c[0,12]*np.sqrt(5)*(6*rho**4 - 6*rho**2 + 1)\
            +c[0,13]*np.sqrt(10)*(4*rho**4 - 3*rho**2) * np.cos(2*theta)\
            +c[0,14]*np.sqrt(10)*rho**4* np.cos(4*theta)\
            +c[0,15]*np.sqrt(12)*rho**5* np.sin(5*theta)\
            +c[0,16]*np.sqrt(12)*(5*rho**5 - 4*rho**3) * np.sin(3*theta)\
            +c[0,17]*np.sqrt(12)*(10*rho**5 - 12*rho**3 + 3*rho) * np.sin(theta)\
            +c[0,18]*np.sqrt(12)*(10*rho**5 - 12*rho**3 + 3*rho) * np.cos(theta)\
            +c[0,19]*np.sqrt(12)*(5*rho**5 - 4*rho**3) * np.cos(3*theta)\
            +c[0,20]*np.sqrt(12)*rho**5* np.cos(5*theta)\
            +c[0,21]*np.sqrt(14)*rho**6* np.sin(6*theta)\
            +c[0,22]*np.sqrt(14)*(6*rho**6 - 5*rho**4) * np.sin(4*theta)\
            +c[0,23]*np.sqrt(14)*(15*rho**6 - 20*rho**4 + 6*rho**2) * np.sin(2*theta)\
            +c[0,24]*np.sqrt(7)*(20*rho**6 - 30*rho**4 + 12*rho**2 - 1)\
            +c[0,25]*np.sqrt(14)*(15*rho**6 - 20*rho**4 + 6*rho**2) * np.cos(2*theta)\
            +c[0,26]*np.sqrt(14)*(6*rho**6 - 5*rho**4) * np.cos(4*theta)\
            +c[0,27]*np.sqrt(14)*rho**6* np.cos(6*theta)\
            +c[0,28]*4 * rho**7* np.sin(7*theta)\
            +c[0,29]*4 *(7*rho**7 - 6*rho**5) * np.sin(5*theta)\
            +c[0,30]*4 *(21*rho**7 - 30*rho**5 + 10*rho**3) * np.sin(3*theta)\
            +c[0,31]*4 *(35*rho**7 - 60*rho**5 + 30*rho**3 - 4*rho) * np.sin(theta)
    return phi

#GoogleNet架構
def Conv2d_BN(x, nb_filter, kernel_size, padding='same', strides=(1, 1)):
    x = Conv2D(nb_filter, kernel_size, padding=padding, strides=strides, activation='tanh')(x)
    return x

def Inception(x, nb_filter):
    branch1x1 = Conv2d_BN(x, nb_filter, (1, 1), padding='same', strides=(1, 1))

    branch3x3 = Conv2d_BN(x, nb_filter, (1, 1), padding='same', strides=(1, 1))
    branch3x3 = Conv2d_BN(branch3x3, nb_filter, (1, 3), padding='same', strides=(1, 1))
    branch3x3 = Conv2d_BN(branch3x3, nb_filter, (3, 1), padding='same', strides=(1, 1))

    branch5x5 = Conv2d_BN(x, nb_filter, (1, 1), padding='same', strides=(1, 1))
    branch5x5 = Conv2d_BN(branch3x3, nb_filter, (1, 3), padding='same', strides=(1, 1))
    branch5x5 = Conv2d_BN(branch3x3, nb_filter, (3, 1), padding='same', strides=(1, 1))
    branch5x5 = Conv2d_BN(branch3x3, nb_filter, (1, 3), padding='same', strides=(1, 1))
    branch3x3 = Conv2d_BN(branch3x3, nb_filter, (3, 1), padding='same', strides=(1, 1))

    branchpool = MaxPooling2D(pool_size=(3, 3), strides=(1, 1), padding='same')(x)
    branchpool = Conv2d_BN(branchpool, nb_filter, (1, 1), padding='same', strides=(1, 1))

    x = concatenate([branch1x1, branch3x3, branch5x5, branchpool], axis=3)

    return x

inpt = Input(shape=(256, 256, 1))    
x = Conv2d_BN(inpt,64, (7, 7),  strides=(2, 2), padding='same')
x  = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)
x  = Conv2d_BN(x, 192, (3, 3), strides=(1, 1), padding='same')
x  = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)
x  = Inception(x, 64)  
x  = Inception(x, 120)  
x  = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)
x  = Inception(x, 128)  
x  = Inception(x, 128)
x  = Inception(x, 128)
x  = Inception(x, 132)  
x  = Inception(x, 208)  
x  = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)
x  = Inception(x, 208)
x  = Inception(x, 256)  
x  = AveragePooling2D(pool_size=(7, 7), strides=(7, 7), padding='same')(x)
x = Flatten()(x)
x = Dense(2048, activation='tanh')(x)
x = Dense(1024, activation='tanh')(x)
x = Dense(1024, activation='tanh')(x)
x = Dense(32, activation='linear')(x)
model = Model(inpt, x, name='inception')

#loss function、優化器選擇
model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(lr=0.00001), metrics=['accuracy'])
model.summary()

#產生驗證數據
num =5000
a = np.linspace(-256, 255, 256)
xv,yv = np.meshgrid( a , a )
yv = yv*-1
rho,theta = cart2pol( xv , yv )
m =rho.max()*0.7
rho = rho/m
rho[rho>1]=np.nan
COE = np.zeros([num,32])
Y = np.zeros((num, 256, 256))
for i in tqdm(range(0,num,1)):
    c =(np.random.rand(1,32)*2-1)/2
    c = c.round(6)
    COE[i,:]=c
    phi=phase(rho,theta,c)
    phi[np.isnan(phi)] = 0
    Y[i] = phi

raw = pd.DataFrame(COE,columns=column_names)
Y=Y.reshape(num, 256, 256,1)
X_test, y_test = Y , raw

def train_batch_generator(ran):
    a = np.linspace(-256, 255, 256)
    xv,yv = np.meshgrid( a , a )
    yv = yv*-1
    rho,theta = cart2pol( xv , yv )
    m =rho.max()*0.7
    rho = rho/m
    rho[rho>1]=np.nan

    z = np.zeros([ran,32])
    X = np.zeros((ran, 256, 256))

    for i in tqdm(range(0,ran,1)):
        c =(np.random.rand(1,32)*2-1)/2
        c = c.round(6)
        z[i,:]=c
        phi=phase(rho,theta,c)
        phi[np.isnan(phi)] = 0
        X[i] = phi
    
    raw_dataset = pd.DataFrame(z,columns=column_names)
    X=X.reshape(ran, 256, 256,1)
    X_train, y_train = X , raw_dataset
    gc.collect()
    yield (X_train, y_train)

#訓練過程
weight_saver = ModelCheckpoint('/content/drive/My Drive/Masterpiece/modle/finaltest4(512).h5', monitor='val_loss', save_best_only=True,verbose=2)
earlystop = EarlyStopping(monitor='accuracy', patience=20,verbose=2)
rle = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=20,verbose=1,min_lr=1e-10)
NUM_EPOCHS = 10
history_all = {}
for i in range(NUM_EPOCHS):
    print('################{0} epochs#############'.format(i+1))
    for X_train, y_train in train_batch_generator():
      history = model.fit(X_train, y_train,
                  validation_data=(X_test, y_test),
                  epochs= 50, batch_size=16,verbose=2,callbacks = [weight_saver,earlystop,rle])
      if len(history_all) == 0:
        history_all = {key: [] for key in history.history}
      for key in history_all:
        history_all[key].extend(history.history[key])

#展示accuracy和loss的變化
logs = history_all

plt.plot(logs['accuracy'])
plt.plot(logs['val_accuracy'])
plt.title('acc')

plt.plot(logs['loss'])
plt.plot(logs['val_loss'])
plt.title('loss')

