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

    #Creating Lag variable
    ts_data_lag <- ts_data %>% 
    mutate(LagHSW_1 = lag(HotspotsWeek, n=1, default = NA),
         LagHSW_2 = lag(HotspotsWeek, n=2, default = NA),
         LagHSW_3 = lag(HotspotsWeek, n=3, default = NA),
         LagHSW_4 = lag(HotspotsWeek, n=4, default = NA),
         LagHSW_8 = lag(HotspotsWeek, n=8, default = NA), #Lag for two months
         LagHSW_13 = lag(HotspotsWeek, n=13, default = NA), #Lag for a quarter
         LagHSW_26 = lag(HotspotsWeek, n=26, default = NA), #Lag for a half a year
         LagHSW_39 = lag(HotspotsWeek, n=39, default = NA), #Lag for three quarters of the year
         LagHSW_52 = lag(HotspotsWeek, n=52, default = NA) #Lag for a year
         )

    return(ts_data_lag)
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
panel_data <- read.csv(depends_on[["panel_data"]]) 

#Creating a time series dataset
ts_data = creating_time_series_data(panel_data)

#Saving the data
write.csv(ts_data, file = produces[["ts_data"]], row.names = FALSE)

