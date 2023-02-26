"""Creating a panel dataset."""

import pytask

from final_project.config import BLD
from final_project.config import SRC

@pytask.mark.depends_on(
    {
        "time_data": BLD / "data_inputs" / "data_with_time.csv",
        "all_hex": BLD / "data_inputs" / "all_hex.csv",
        "all_CW": BLD / "data_inputs"/ "all_CW.csv",
        "all_CWY": BLD / "data_inputs" / "all_CWY.csv",
        "all_YEAR": BLD / "data_inputs" / "all_YEAR.csv",
    }
    )
@pytask.mark.produces(
    {
    "data_without_neighbours": BLD / "data_for_analysis" / "data_without_neighbours.csv",
    #"data_with_neighbours": BLD / "data" / "data_with_neighbours.csv",
    #"panel_data_with_neighbours_without_lag": BLD / "data" / "panel_data_with_neighbours_without_lag.csv",
    }
    )
@pytask.mark.r(
    script=SRC / "data_management" / "function_2_create_panel_data.r", serializer="yaml"
)
def task_2_create_panel_data():
    pass
