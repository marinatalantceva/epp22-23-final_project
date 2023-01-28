"""Downloading of the file from url."""
import pytask
from final_project.config import SRC


@pytask.mark.produces(SRC / "data" / "api_data.csv")
@pytask.mark.r(
    script=SRC / "data_management" / "function_downloading_data.r", serializer="yaml"
)
def task_0_downloading_data():
    pass
