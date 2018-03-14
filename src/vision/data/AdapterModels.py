from sklearn.linear_model import LinearRegression
import numpy as np
import _pickle as pickle
import pandas as pd

if __name__ == '__main__':
    
    #x = pd.read_csv('PixelCoordinates.csv')

    #PixelX = x['PixelX'].values
    #PixelY= x['PixelY'].values
    #RobotX = x['RobotX'].values
    #RobotY = x['RobotY'].values

    f = open('demo3_model_data.pkl','rb')
    RobotX = np.array(pickle.load(f))
    RobotY = np.array(pickle.load(f))
    PixelX = np.array(pickle.load(f))
    PixelY = np.array(pickle.load(f))
    
    data = np.c_[PixelX,PixelY]
    print(data.shape)
    lrX = LinearRegression()
    lrX.fit(PixelY.reshape(-1,1),RobotX.reshape(-1,1))
    
    lrY = LinearRegression()
    lrY.fit(PixelX.reshape(-1,1),RobotY.reshape(-1,1))

    lrXXY = LinearRegression()
    lrXXY.fit(data,RobotX.reshape(-1,1))

    lrXYY = LinearRegression()
    lrXYY.fit(data,RobotY.reshape(-1,1))

    f = open('AdapterModels.pkl','wb')
    pickle.dump(lrX,f)
    pickle.dump(lrY,f)
    pickle.dump(lrXXY,f)
    pickle.dump(lrXYY,f)
    f.close()

    
