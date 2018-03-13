from sklearn.linear_model import LinearRegression
import numpy as np
import _pickle as pickle
import pandas as pd

if __name__ == '__main__':
    
    x = pd.read_csv('PixelCoordinates.csv')

    PixelX = x['PixelX'].values
    PixelY= x['PixelY'].values
    RobotX = x['RobotX'].values
    RobotY = x['RobotY'].values

    data = np.c_[PixelX,PixelY]
    print(data.shape)
    lrX = LinearRegression()
    lrX.fit(data,RobotX.reshape(-1,1))
    
    lrY = LinearRegression()
    lrY.fit(data,RobotY.reshape(-1,1))

    f = open('AdapterModels.pkl','wb')
    pickle.dump(lrX,f)
    pickle.dump(lrY,f)
    f.close()

    
