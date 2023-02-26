"""Creating a chart that shows the amount of cumulative adoptions every week."""

import pytask
import matplotlib.pyplot as plt
import pandas as pd

from final_project.config import BLD

@pytask.mark.depends_on(
    {
        "data_train": BLD / "data_for_analysis" / "data_train.csv",
    }
    )
@pytask.mark.produces(
    {
        "cumulative_adoptions": BLD / "plots" / "cumulative_adoptions.png",
    }
    )

def task_7_creating_chart_cumulative_adoptions(depends_on, produces):
    data_train = pd.read_csv(depends_on["data_train"])

    plt.clf()
    plt.rcParams['font.size'] = 10
    
    # Plot the chart that shows the amount of cumulative adoptions every week
    plt.figure().set_figwidth(10)
    plt.plot(data_train.Date, data_train.HotspotsWeek)
    plt.title("Weekly Hotspot Adoptions (Cumulative)")
    plt.xticks([])
    plt.xlabel("Date")
    #plt.xticks(rotation=45)
    plt.ylabel("Number of Adoptions")
    plt.savefig(produces["cumulative_adoptions"])