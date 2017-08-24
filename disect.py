import numpy as np
import pandas as pd
import cv2

file_name = "training.npy"
train_data = np.load(file_name)
df = pd.DataFrame(train_data)

DataX = np.empty((2430,3072))
count = 0
for i in range(train_data.shape[0]):
    data = train_data[i]
    img = data[0]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.reshape(img, (1,3072))
    
    key = int(data[1])
    if(key == 6 or key == 0 or key == 1 or key == 2 or key == 3):
        DataX[count,:] = img
        count +=1
##    img = np.reshape(img, (48,64))
##    cv2.imshow('image', img)
##    if cv2.waitKey(25) & 0xFF==ord('q'):
##        cv2.destroyAllWindows()
##        break        

for i in range(DataX.shape[0]):        
    img = np.array(np.reshape(DataX[i], (48,64)), dtype='uint8')
    cv2.imshow('image', img)
    #print(img.shape)
    if cv2.waitKey(25) & 0xFF==ord('q'):
        cv2.destroyAllWindows()
        break        
