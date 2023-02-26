"""Creating a time dataset."""
import pytask
from final_project.config import SRC


@pytask.mark.depends_on(
    {
        "api_data": SRC / "data" / "api_data.csv",
    }
)
@pytask.mark.produces(
    {
        "time_data": SRC / "data" / "data_with_time.csv",
        "all_hex": SRC / "data" / "all_hex.csv",
        "all_CW": SRC / "data" / "all_CW.csv",
        "all_CWY": SRC / "data" / "all_CWY.csv",
        "all_YEAR": SRC / "data" / "all_YEAR.csv",
    }
)
@pytask.mark.r(
    script=SRC / "data_management" / "function_1_creating_time_dataset.r",
    serializer="yaml",
)
def task_1_creating_time_dataset():
    pass
