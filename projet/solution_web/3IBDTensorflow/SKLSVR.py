import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from config import *

# Params
gamma = 0.1
epsilon = 0.1
name_model = "train_models/SVR_w%s_h%s_c%s_bigdataset.h5" % (width, height, color)

# Load model
# svr_rbf = joblib.load(name_model)

# Generate sample data
X = np.sort(5 * np.random.rand(40, 1), axis=0)
Y = np.sin(X).ravel()

svr_rbf = SVR(kernel='rbf', gamma=gamma, epsilon=epsilon)
svr_rbf.fit(X, Y)



plt.plot(X, svr_rbf.predict(X), 'b', X, Y, 'k.')
plt.show()

# save model
joblib.dump(svr_rbf, name_model)
