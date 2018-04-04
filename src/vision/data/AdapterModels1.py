from sklearn.linear_model import LinearRegression
import numpy as np
import _pickle as pickle
import pandas as pd

if __name__ == '__main__':
    
    RobotX = np.array([80,220,360,500,640,780,920,1060,1200,1340,1480])
    RobotY = np.array([60,200,340,480,620,760,915])

    PixelX = np.array([81,134,188,241,295,348,402]).reshape(-1,1)
    PixelY = np.array([47,112,179,247,315,384,452,523,591,661,730]).reshape(-1,1)

    lrX = LinearRegression()
    lrX.fit(PixelY,RobotX.reshape(-1,1))
    
    lrY = LinearRegression()
    lrY.fit(PixelX,RobotY.reshape(-1,1))

    f = open('AdapterModels1.pkl','wb')
    pickle.dump(lrX,f)
    pickle.dump(lrY,f)
    f.close()

    
