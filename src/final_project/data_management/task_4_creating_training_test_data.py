"""Creating train and test dataframes."""

import pytask
import numpy as np
import pandas as pd

from final_project.config import BLD
from final_project.config import SRC

@pytask.mark.depends_on(
    {
        "data": BLD / "data" / "adoptions_cumulative_raw.csv",
    }
    )
@pytask.mark.produces(
    {
        "data_train": BLD / "data" / "data_train.csv",
        "data_test": BLD / "data" / "data_test.csv",
    }
    )


def task_4_creating_training_test_data(depends_on, produces):
    ## Read the the csv document from the previous E file ###
    adoptions_cumulative_raw = pd.read_csv(depends_on["data"])
    # Date column needs to be attached:
    adoptions_cumulative_raw['Date'] = pd.date_range(start = '22/07/2019', end = '26/12/2022', freq = 'W-MON')
    # We define the time frame that we want to analyze
    # We decide to cut off the first 55 entries auf the data, because during this time the Helium Network
    # was still young, and therefore the adoption process had not yet started rolling at that point.
    # The analyzed timeframe is: 2020-08-10 to 2020-12-26.
    min_range = 55
    max_range = 180
    adoptions_cumulative = adoptions_cumulative_raw[min_range:max_range]
    # We devide the data into a train and test dataset.
    data_train = adoptions_cumulative[0:65]
    data_test = adoptions_cumulative[64:125]
    data_train.to_csv(produces['data_train'], index=False)
    data_test.to_csv(produces['data_test'], index=False)