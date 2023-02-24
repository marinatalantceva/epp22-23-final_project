"""Create the final plot that is comparing the Diffusion Graph (Adoption Graph) to the historical price data of HNT (data from yahoo finance)."""

import pytask
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

from final_project.config import BLD


@pytask.mark.depends_on(
    {
        "HNT_data": BLD / "data" / "HNT_data.csv",
        "adoptions_cumulative": BLD / "data" / "adoptions_cumulative.csv",
        "estimated_adoptions_whole_data": BLD / "data" / "estimated_adoptions_whole_data.csv",
    }
    )
@pytask.mark.produces(
    {
        "HNT_comparison_plot": BLD / "plots" / "HNT_comparison_plot.png",
    }
    )

def task_14_creating_plot_HNT_comparison(depends_on, produces):
    HNT_data = pd.read_csv(depends_on["HNT_data"])
    adoptions_cumulative = pd.read_csv(depends_on["adoptions_cumulative"])
    estimated_adoptions_whole_data = pd.read_csv(depends_on["estimated_adoptions_whole_data"])

    #Specifying parameters of the plot
    x = HNT_data.Date
    y1 = estimated_adoptions_whole_data
    y2 = adoptions_cumulative.HotspotsWeek
    y3 = HNT_data.Close
    
    plt.clf()
    
    #Specifying subplots
    fig, ax1 = plt.subplots()
    
    #First plot ('Predicted adoptions')
    ax1.plot(x, y1, 'darkblue', label = "Predicted Adoptions")
    
    #Second plot ('Actual Adoptions')
    ax2 = ax1.twiny()
    ax2.plot(x, y2, 'royalblue', label = "Actual Adoptions")
    
    #Third plot ('Historical prices')
    ax3 = ax1.twinx()
    ax3.plot(x, y3, 'green', label = "HNT Price")
    
    ax1.set_ylabel("Adoptions", color = "blue")
    ax3.set_ylabel("Price", color = "green")
    
    ax1.tick_params(axis='y', colors = "blue")
    ax3.tick_params(axis='y', colors = "green")
    
    ax3.spines['right'].set_color('green')
    ax3.spines['left'].set_color('blue')

    ax1.set_xticks([])
    ax2.set_xticks([])
    
    #ax1.set_xticks(["2020-10", "2021-04", "2021-10", "2022-04", "2022-10"])
    #ax2.set_xticks(["2020-10", "2021-04", "2021-10", "2022-04", "2022-10"])
    
    fig.set_figwidth(10)
    fig.legend(loc="lower left", bbox_to_anchor=(0.13,0.65))
    
    plt.savefig(produces['HNT_comparison_plot'])