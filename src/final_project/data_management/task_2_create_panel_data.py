"""Creating a panel dataset."""

import pytask

from final_project.config import BLD
from final_project.config import SRC

@pytask.mark.depends_on(
    {
        "time_data": SRC / "data" / "data_with_time.csv",
        "all_hex": SRC / "data" / "all_hex.csv",
        "all_CW": SRC / "data" / "all_CW.csv",
        "all_CWY": SRC / "data" / "all_CWY.csv",
        "all_YEAR": SRC / "data" / "all_YEAR.csv",
    }
    )
@pytask.mark.produces(
    {
    "data_without_neighbours": BLD / "data" / "data_without_neighbours.csv",
    "data_with_neighbours": BLD / "data" / "data_with_neighbours.csv",
    "panel_data_with_neighbours_without_lag": BLD / "data" / "panel_data_with_neighbours_without_lag.csv",
    }
    )
@pytask.mark.r(
    script=SRC / "data_management" / "function_2_create_panel_data.r", serializer="yaml"
)
def task_2_create_panel_data():
    pass
