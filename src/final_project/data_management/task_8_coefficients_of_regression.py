"""Preparing the variables that are needed to run the Linear Regression and exctracting the coefficiants of the regression."""

import pytask
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from numpy import savetxt
import math

from final_project.config import BLD

@pytask.mark.depends_on(
    {
        "data_train": BLD / "data_for_analysis" / "data_train.csv",
        "data_train_fd": BLD / "data_for_analysis" / "data_train_fd.csv",
    }
    )
@pytask.mark.produces(
    {
        "a": BLD / "data_for_analysis" / "bass_model_parameters" / "a.csv",
        "b": BLD / "data_for_analysis" / "bass_model_parameters"  / "b.csv",
        "c": BLD / "data_for_analysis" / "bass_model_parameters"  / "c.csv",
    }
    )

def task_8_coefficients_of_regression(depends_on, produces):
    data_train = pd.read_csv(depends_on["data_train"])
    data_train_fd = pd.read_csv(depends_on["data_train_fd"])
    
    # Preparing the variables that are needed to run the Linear Regression, which is subsequently needed
    # to calculate the coeffictien of innovation (p), coefficient of imitation (q) and the market size (m)
    adoptions_ts = data_train.HotspotsWeek[0:len(data_train)-1]
    adoptions_ts = np.asarray(adoptions_ts)
    adoptions_ts = pd.DataFrame(adoptions_ts)
    lower_bound = adoptions_ts[0][0]
    
    Y = adoptions_ts-lower_bound # Series that contains the amount of the total amount of past
                                        # adoptions. We substract the first entry of the series from
                                        # all entries to achieve a better model fit.
                                  
    Ysq = Y[0]**2 # The quadratic term of the Bass model
    
    X = np.transpose(np.array([Y[0], Ysq])) # Combining both variables into an ndarray for the linear regression
    
    # Run the regression:
    
    reg = LinearRegression().fit(X,data_train_fd.HotspotsWeek)
    
    # Extract the coefficients in order to calculate the Bass Model parameters p, q and m
    
    a = reg.intercept_
    a = a.reshape(1,-1)
    b = reg.coef_[0]
    b = b.reshape(1,-1)
    c = reg.coef_[1]
    c = c.reshape(1,-1)


    savetxt(produces['a'], a, header = 'a')
    savetxt(produces['b'], b, header = 'b')
    savetxt(produces['c'], c, header = 'c')
    
