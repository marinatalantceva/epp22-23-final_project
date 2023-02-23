"""Creating plot of Bass Model Adoptions vs Actual Adoptions."""

import pytask
import matplotlib.pyplot as plt
import pandas as pd

from final_project.config import BLD

@pytask.mark.depends_on(
    {
        "data_train_fd": BLD / "data" / "data_train_fd.csv",
        "data_train": BLD / "data" / "data_train.csv",
        "estimated_adoptions_train": BLD / "data" / "estimated_adoptions_train.csv",
    }
    )
@pytask.mark.produces(
    {
        "bass_vs_actual": BLD / "plots" / "bass_vs_actual.pdf",
    }
    )

def task_10_creating_plot_bass_vs_actual(depends_on, produces):
    data_train_fd = pd.read_csv(depends_on["data_train_fd"])
    data_train = pd.read_csv(depends_on["data_train"])
    estimated_adoptions_train = pd.read_csv(depends_on["estimated_adoptions_train"])

    plt.clf()
    plt.rcParams['font.size'] = 5

    plt.figure().set_figwidth(10)
    plt.plot(data_train.Date, estimated_adoptions_train, label = "Fitted Bass Model")
    plt.plot(data_train.Date.iloc[1:], data_train_fd, label = "Actual New Hotspot Adotions")
    plt.title("Bass Model Adoptions vs Actual Adoptions")
    plt.xlabel("Date")
    plt.xticks(rotation=90)
    plt.ylabel("Number of Adoptions")
    plt.legend(loc="lower left", bbox_to_anchor=(0.01,0.77))
    plt.savefig(produces['bass_vs_actual'])