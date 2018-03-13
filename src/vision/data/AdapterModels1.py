from sklearn.linear_model import LinearRegression
import numpy as np
import _pickle as pickle
import pandas as pd

if __name__ == '__main__':
    
    PixelX = np.array([45.75,112.75,177.25,243.5,310.5,376.25,510.5,577.5,645.25,712]).reshape(-1,1)
    PixelY = np.array([59.875,106,152.375,198.625,245.5]).reshape(-1,1)

    RobotX = np.array([55,200,335,480,615])
    RobotY = np.array([55,195,325,465,605,750,890,1030,1180,1320])

    lrX = LinearRegression()
    lrX.fit(PixelY,RobotX.reshape(-1,1))
    
    lrY = LinearRegression()
    lrY.fit(PixelX,RobotY.reshape(-1,1))

    f = open('AdapterModels1.pkl','wb')
    pickle.dump(lrX,f)
    pickle.dump(lrY,f)
    f.close()

    
