"""Preparing the variables that are needed to run the Linear Regression and exctracting the coefficiants of the regression."""

import pytask
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

from final_project.config import BLD

@pytask.mark.depends_on(
    {
        "data_train": BLD / "data" / "data_train.csv",
        "data_train_fd": BLD / "data" / "data_train_fd.csv",
    }
    )
@pytask.mark.produces(
    {
        "a": BLD / "data" / "a.csv",
        "b": BLD / "data" / "Y.csv",
        "c": BLD / "data" / "c.csv",
    }
    )

def task_8_coefficients_of_regression(depends_on, produces):
    data_train = pd.read_csv(depends_on["data_train"])
    min_range = 55

    # Preparing the variables that are needed to run the Linear Regression, which is subsequently needed
    # to calculate the coeffictient of innovation (p), coefficient of imitation (q) and the market size (m)
    adoptions_ts = data_train.HotspotsWeek[0:len(data_train)-1]
    Y = adoptions_ts-adoptions_ts[min_range]
    # Series that contains the amount of the total amount of past
    # adoptions. We substract the first entry of the series from
    # all entries to achieve a better model fit
    
    Ysq = Y**2 # The quadratic term of the Bass model
    
    X = np.transpose(np.array([Y, Ysq])) # Combining both variables into an ndarray for the linear regression
    
    # Run the regression:
    reg = LinearRegression().fit(X,new_adoptions)
    
    # Extract the coefficients in order to calculate the Bass Model parameters p, q and m_
    a = reg.intercept_
    b = reg.coef_[0]
    c = reg.coef_[1]

    a.to_csv(produces['a'], index=False)
    b.to_csv(produces['b'], index=False)
    c.to_csv(produces['c'], index=False)
