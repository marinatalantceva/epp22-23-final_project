"""Compute estimated Bass model on the whole time frame."""

import pytask
import pandas as pd
import math
import numpy as np
from numpy import savetxt

from final_project.config import BLD

from final_project.data_management.function_4_bass_model import (
    bass_model,
)

@pytask.mark.depends_on(
    {
        "a": BLD / "data" / "a.csv",
        "b": BLD / "data" / "b.csv",
        "c": BLD / "data" / "c.csv",
        "adoptions_cumulative": BLD / "data" / "adoptions_cumulative.csv",
        "data_train": BLD / "data" / "data_train.csv",
    }
    )
@pytask.mark.produces(
    {
        "estimated_adoptions_whole_data": BLD / "data" / "estimated_adoptions_whole_data.csv",
    }
    )

def task_11_calculating_bass_model_whole_data(depends_on, produces):
    # Calculate the Bass Model Parameters using the formulas from the literature:
    a = pd.read_csv(depends_on["a"], header = None)
    b = pd.read_csv(depends_on["b"], header = None)
    c = pd.read_csv(depends_on["c"], header = None)
    adoptions_cumulative = pd.read_csv(depends_on["adoptions_cumulative"], header = None)
    data_train_header = pd.read_csv(depends_on["data_train"])

    adoptions_ts = data_train_header.HotspotsWeek[0:len(data_train_header)-1]
    adoptions_ts = np.asarray(adoptions_ts)
    adoptions_ts = pd.DataFrame(adoptions_ts)
    lower_bound = adoptions_ts[0][0]

    a = float(a[0][1])
    b = float(b[0][1])
    c = float(c[0][1])
    
    m = (-b - math.sqrt(b**2-4*a*c))/(2*c)
    p = a/m
    q = b + p
    
    # Now, we are predicting the bass model for the whole timeframe. 
    estimated_adoptions_whole_data = bass_model(p,q,m,len(adoptions_cumulative))

    # Transforming the ndarray to cumulative data (since the bass model only returns number of new 
    # adoptions per week) and adding back the previously discarded adoptions.
    estimated_adoptions_whole_data = np.cumsum(estimated_adoptions_whole_data) + lower_bound

    savetxt(produces['estimated_adoptions_whole_data'], estimated_adoptions_whole_data)