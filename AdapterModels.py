from sklearn.linear_model import LinearRegression
import numpy as np
import cPickle as pickle

if __name__ == '__main__':

    Y_pixel = np.array([40,95,148,203,259,315,341]).reshape(-1,1)
    Y_robot = np.array([0,120,250,390,530,680,750]).reshape(-1,1)

    X_pixel = np.array([457,527,593,664,732,801,765]).reshape(-1,1)
    X_robot = np.array([870,1010,1160,1300,1440,1575,1700]).reshape(-1,1)

    dataX = np.c_[X_pixel,X_robot]
    dataY = np.c_[Y_pixel,Y_robot]

    print(dataX.shape,dataY.shape)

    lrX = LinearRegression()
    lrX.fit(X_pixel,X_robot)

    lrY = LinearRegression()
    lrY.fit(Y_pixel,Y_robot)

    f = open('AdapterModels.pkl','w')
    pickle.dump(lrX,f)
    pickle.dump(lrY,f)
    f.close()

    
