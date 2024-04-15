from joblib import load
import os
import numpy as np
def predict(text):

        if not(os.path.exists('Kmenas_model.joblib')):
            return None
        
        if not(os.path.exists('word2vecmodel.joblib')):
            return None
        
        model = load('Kmenas_model.joblib')
        word2vecmodel = load('word2vecmodel.joblib')
    

        def text_to_vector(text):
                words = text.split()
                return word2vecmodel.wv.get_mean_vector(words)


        vector = text_to_vector(text)
        vector_2d = np.stack(vector)
  
        label = model.predict(vector_2d)
        return label
