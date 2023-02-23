"""Creating a time series dataset. This dataset will be used for out Machine Learning models."""

import pytask

from final_project.config import BLD
from final_project.config import SRC


@pytask.mark.depends_on(
    {
        "data_without_neighbours": BLD / "data" / "data_without_neighbours.csv",
    }
    )
@pytask.mark.produces(
    {
        "adoptions_cumulative_raw": BLD / "data" / "adoptions_cumulative_raw.csv",
    }
    )
@pytask.mark.r(
    script=SRC / "data_management" / "function_3_creating_time_series_data.r", serializer="yaml"
)
def task_3_creating_time_series_data():
    pass