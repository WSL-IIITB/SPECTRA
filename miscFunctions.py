import numpy as np

def softmax(ar):
    return np.exp(ar)/np.sum(np.exp(ar))