import numpy as np

class DLModel:
    def predict(self, sequence):
        # pattern strength detection
        arr = np.array(sequence)

        momentum = np.mean(arr)
        volatility = np.std(arr)

        score = (momentum * 50) + (1 / (volatility + 0.1)) * 10

        # normalize
        prob = 1 / (1 + np.exp(-score / 10))
        return prob