"""Calculate the Bass Model Parameters using the formulas."""

import numpy as np

def bass_model(p,q,m,T):
        """Creates estimated adoption data based on actual adoption data.
        
        Args:
        p (float): Coefficient of innovation, calculated from the linear regression results.
        q (float): Coefficient of immitation, calculated from the linear regression results.
        m (float): Parameter that indicated the market size and provides the scale of the demand forecast. Also calculated from the linear regression results.
        T (float): The timeframe for which the estimated time series should be returned
        
        Returns:
        ndarray: Contains adoptions per week estimated by the bass model. 
        """

        A = np.zeros(T)
        Y = np.zeros(T+1)
        
        for t in range(T):
            A[t] = p*m + (q-p) * Y[t] - (q/m) * Y[t]**2
            Y[t+1] = Y[t] + A[t]
        
        return A