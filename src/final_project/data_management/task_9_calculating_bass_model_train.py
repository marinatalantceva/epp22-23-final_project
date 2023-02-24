"""Compute estimated Bass model on a training sample."""

import pytask
import pandas as pd
import math
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
        "data_train": BLD / "data" / "data_train.csv",
    }
    )
@pytask.mark.produces(
    {
        "estimated_adoptions_train": BLD / "data" / "estimated_adoptions_train.csv",
    }
    )

def task_9_calculating_bass_model_train(depends_on, produces):
    # Calculate the Bass Model Parameters using the formulas from the literature:
    a = pd.read_csv(depends_on["a"], header = None)
    b = pd.read_csv(depends_on["b"], header = None)
    c = pd.read_csv(depends_on["c"], header = None)
    data_train = pd.read_csv(depends_on["data_train"], header = None)

    a = float(a[0][1])
    b = float(b[0][1])
    c = float(c[0][1])
    
    m = (-b - math.sqrt(b**2-4*a*c))/(2*c)
    p = a/m
    q = b + p
    
    # First, we are fitting the bass model with the same length as the train dataset. This way, we compare
    # the actual data with our bass model fit
    estimated_adoptions_train = bass_model(p,q,m,len(data_train))

    savetxt(produces['estimated_adoptions_train'], estimated_adoptions_train)
