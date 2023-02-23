"""Creating a chart with the amount of cumulative adoptions every week."""

import pytask
import matplotlib.pyplot as plt
import pandas as pd

from final_project.config import BLD

@pytask.mark.depends_on(
    {
        "data_train": BLD / "data" / "data_train.csv",
    }
    )
@pytask.mark.produces(
    {
        "cumulative_adoptions": BLD / "plots" / "cumulative_adoptions.pdf",
    }
    )

def task_7_creating_chart_cumulative_adoptions(depends_on, produces):
    data_train = pd.read_csv(depends_on["data_train"])

    plt.clf()
    plt.rcParams['font.size'] = 6
    
    # Plot the chart with the amount of cumulative adoptions every week
    plt.figure().set_figwidth(10)
    plt.plot(data_train.Date, data_train.HotspotsWeek)
    plt.title("Weekly Hotspot Adoptions (Cumulative)")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel("Number of Adoptions")
    plt.savefig(produces["cumulative_adoptions"])