"""Creating a time series dataset. This dataset will be used for out Machine Learning models."""

import pytask

from final_project.config import BLD
from final_project.config import SRC


@pytask.mark.depends_on(
    {
        "panel_data": BLD / "data" / "panel_data_with_neighbours_without_lag.csv",
    }
    )
@pytask.mark.produces(
    {
        "ts_data": BLD / "data" / "time_series_data.csv",
    }
    )
@pytask.mark.r(
    script=SRC / "data_management" / "function_3_creating_time_series_data.r", serializer="yaml"
)
def task_3_creating_time_series_data():
    pass