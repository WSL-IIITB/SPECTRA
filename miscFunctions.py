import numpy as np

def softmax(ar):
    # return np.exp(ar)/np.sum(np.exp(ar))
    e_x = np.exp(ar-np.max(ar))
    return e_x/e_x.sum()