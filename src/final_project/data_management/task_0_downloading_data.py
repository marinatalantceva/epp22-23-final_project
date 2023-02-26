"""Downloading of the file from url."""
import pytask
from final_project.config import SRC
from final_project.config import BLD


@pytask.mark.produces(BLD / "data_inputs" / "api_data.csv")
@pytask.mark.r(
    script=SRC / "data_management" / "function_0_downloading_data.r", serializer="yaml"
)
def task_0_downloading_data():
    pass
