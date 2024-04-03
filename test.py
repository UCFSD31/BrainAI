import numpy as np
for i in range(2):
    for j in range(2):
        W = np.array([[-3, -1, 2],
                    [-2, 2, -2]])

        x = np.array([[i],
                    [j]])

        w = np.array([[1],
                    [1],
                    [1]])

        b = np.array([[0],
                      [-1],
                      [-1]])


        y = np.dot(w.transpose(),(np.maximum((np.dot(W.transpose(), x) + b),0)))
        z = np.maximum((np.dot(W.transpose(), x) + b),0).transpose()


        #y = np.dot(w.transpose(), h)

        print("y when x = " + str(i) + str(j) + ": " + str(y))
        print(z)