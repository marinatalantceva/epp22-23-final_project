"""Creating dataframe with first differences of cumulative sales."""

import pytask
import pandas as pd

from final_project.config import BLD

@pytask.mark.depends_on(
    {
        "data": BLD / "data" / "data_train.csv",
    }
    )
@pytask.mark.produces(
    {
        "data_train_fd": BLD / "data" / "data_train_fd.csv",
    }
    )

def task_5_creating_first_differences_training_data(depends_on, produces):
    data_train = pd.read_csv(depends_on["data"])

    # We compute the first difference of the cumulative sales to explore the amount of new adoptions per week
    # (since the other dataframes present only total amount of adoptions).
    data_train_fd = data_train.HotspotsWeek.diff().iloc[1:]
    data_train_fd.to_csv(produces['data_train_fd'], index=False)

