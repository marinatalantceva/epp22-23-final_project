"""Creating plot with weekly adoptions."""

import pytask
import matplotlib.pyplot as plt
import pandas as pd

from final_project.config import BLD

@pytask.mark.depends_on(
    {
        "data_train_fd": BLD / "data" / "data_train_fd.csv",
        "data_train": BLD / "data" / "data_train.csv",
    }
    )
@pytask.mark.produces(
    {
        "weekly_adoptions": BLD / "plots" / "weekly_adoptions.pdf",
    }
    )

def task_6_creating_plot_weekly_adoptions(depends_on, produces):
    data_train_fd = pd.read_csv(depends_on["data_train_fd"])
    data_train = pd.read_csv(depends_on["data_train"])

    plt.rcParams['font.size'] = 6
    plt.figure().set_figwidth(10)
    plt.plot(data_train.Date.iloc[1:], data_train_fd)
    plt.title("Weekly Hotspot Adoptions")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel("Number of Adoptions")
    plt.savefig(produces["weekly_adoptions"])

