# Creating a time series dataset to use for predictions in later work.

#This dataset will be the one that we use for out Machine Learning predictions.

# ======================================================================================
# Functions
# ======================================================================================

library(tidyverse)
library(dplyr)

#The point of the following function is to create a dataframe with two main features: time variables and cumulative number of hotspots.

creating_time_series_data = function(panel_data){
    #Making CalenderWeekYear to have unique value in order to find unique values of total number of hotspots for the week
    ts_data <- panel_data %>% group_by(CalendarWeek) %>% 
    summarise(HotspotsWeek=sum(Hotspots.Cumul), .groups = 'drop')

    # Adding missing rows (they are missing because during those weeks nobody adopted):
    adoptions_cumulative_raw <- ts_data %>% complete(CalendarWeek = 30:max(CalendarWeek), fill = list(HotspotsWeek = 0))
    
    for(i in 2:nrow(adoptions_cumulative_raw)){
        if(adoptions_cumulative_raw$HotspotsWeek[i] == 0){
            adoptions_cumulative_raw$HotspotsWeek[i] = adoptions_cumulative_raw$HotspotsWeek[i-1]
            }
        }
        
    return(adoptions_cumulative_raw)
}

# ======================================================================================
# Get produces and depends_on from pytask
# ======================================================================================

args <- commandArgs(trailingOnly = TRUE)
path_to_yaml <- args[length(args)]
config <- yaml::yaml.load_file(path_to_yaml)

produces <- config[["produces"]]
depends_on <- config[["depends_on"]]

# ======================================================================================
# Main
# ======================================================================================

#Downloading input data
panel_data <- read.csv(depends_on[["data_without_neighbours"]]) 

#Creating a time series dataset
adoptions_cumulative_raw = creating_time_series_data(panel_data)
adoptions_cumulative_raw <- apply(adoptions_cumulative_raw, 2, as.character)

#Saving the data
write.csv(adoptions_cumulative_raw, file = produces[["adoptions_cumulative_raw"]], row.names = FALSE)

