"""Creating a time dataset."""
import pytask
from final_project.config import SRC
from final_project.config import BLD


@pytask.mark.depends_on(
    {
        "api_data": BLD / "data_inputs" / "api_data.csv",
    }
)
@pytask.mark.produces(
    {
<<<<<<< HEAD
        "time_data": BLD / "data_inputs" / "data_with_time.csv",
        "all_hex": BLD / "data_inputs" / "all_hex.csv",
        "all_CW": BLD / "data_inputs"/ "all_CW.csv",
        "all_CWY": BLD / "data_inputs" / "all_CWY.csv",
        "all_YEAR": BLD / "data_inputs" / "all_YEAR.csv",
=======
        "time_data": SRC / "data" / "data_with_time.csv",
        "all_hex": SRC / "data" / "all_hex.csv",
        "all_CW": SRC / "data" / "all_CW.csv",
        "all_CWY": SRC / "data" / "all_CWY.csv",
        "all_YEAR": SRC / "data" / "all_YEAR.csv",
>>>>>>> eeeb50596a9127be592ad22489ff05309ebd461b
    }
)
@pytask.mark.r(
    script=SRC / "data_management" / "function_1_creating_time_dataset.r",
    serializer="yaml",
)
def task_1_creating_time_dataset():
    pass
