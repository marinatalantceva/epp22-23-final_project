"""Creating plot of the whole bass model fit."""

import pytask
import matplotlib.pyplot as plt
import pandas as pd

from final_project.config import BLD

@pytask.mark.depends_on(
    {
        "data_train": BLD / "data" / "data_train.csv",
        "estimated_adoptions_whole_data": BLD / "data" / "estimated_adoptions_whole_data.csv",
        "adoptions_cumulative": BLD / "data" / "adoptions_cumulative.csv",
        "data_test": BLD / "data" / "data_test.csv",
    }
    )
@pytask.mark.produces(
    {
        "whole_bass_fit_train": BLD / "plots" / "whole_bass_fit_train.png",
        "whole_bass_fit": BLD / "plots" / "whole_bass_fit.png",
    }
    )

def task_12_creating_plot_whole_bass_fit(depends_on, produces):
    adoptions_cumulative = pd.read_csv(depends_on["adoptions_cumulative"])
    data_train = pd.read_csv(depends_on["data_train"])
    data_test = pd.read_csv(depends_on["data_test"])
    estimated_adoptions_whole_data = pd.read_csv(depends_on["estimated_adoptions_whole_data"])

    plt.clf()
    plt.rcParams['font.size'] = 5

    # Plot the whole bass model fit, which is only based on the adoptions_train dataset:
    plt.figure().set_figwidth(10)
    plt.plot(adoptions_cumulative.Date, estimated_adoptions_whole_data, label = "Fitted Bass Model")
    
    # Also plot the actual values of adoption_train dataset:
    plt.plot(data_train.Date, data_train.HotspotsWeek, label = "Actual Cumulative Hotspot Adoptions (Train)")
    
    plt.title("Cumulative Bass Model Adoptions vs Actual Cumulative Adoptions")
    plt.xticks([])
    #plt.xlabel("Date")
    #plt.xticks(rotation=90)
    plt.ylabel("Number of Adoptions")
    #plt.xticks(["2020-10", "2021-04", "2021-10", "2022-04", "2022-10"])
    plt.legend(loc="lower left", bbox_to_anchor=(0.01,0.77))
    plt.savefig(produces['whole_bass_fit_train'])

    # Finally, plot the the adoptions_test dataset, which the model has never seen before and compare
    # it to the prediction
    plt.plot(data_test.Date, data_test.HotspotsWeek, label = "Actual Cumulative Hotspot Adoptions (Test)")
    plt.savefig(produces['whole_bass_fit'])


