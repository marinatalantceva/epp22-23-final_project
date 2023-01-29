# Creating a time dataset to use for predictions in later work

# ======================================================================================
# Functions
# ======================================================================================
library(tidyverse)
library(dplyr)
library(data.table)

data_format <- function(api_data) {
  # Properly format the "timestamp_added" variable
  api_data$timestamp_added <- gsub(".{17}$", "", api_data$timestamp_added)
  api_data$timestamp_added <- api_data$timestamp_added %>% as.Date()

  return(api_data)
}

add_time_variables <- function(api_data_format) {
  # Add column containing the corresponding Calendar Week
  api_data_format$CalendarWeekYear <- strftime(api_data_format$timestamp_added, format = "%V")
  api_data_format$CalendarWeekYear <- api_data_format$CalendarWeekYear %>% as.numeric()

  # Add a year variable
  api_data_format$Year <- gsub(".{6}$", "", api_data_format$timestamp_added) %>% as.numeric()

  # Edit the days at the turn of the year. Add the days to the years to whose calendar week they belong.
  for (i in 1:nrow(api_data_format)) {
    if (api_data_format$timestamp_added[i] >= as.IDate("2019-12-30") & api_data_format$timestamp_added[i] <= as.IDate("2019-12-31")) {
      api_data_format$Year[i] <- 2020
    } # make last days of 2019 count for 2020
    if (api_data_format$timestamp_added[i] >= as.IDate("2021-01-01") & api_data_format$timestamp_added[i] <= as.IDate("2021-01-03")) {
      api_data_format$Year[i] <- 2020
    } # make first days of 2021 count for 2020
    if (api_data_format$timestamp_added[i] >= as.IDate("2022-01-01") & api_data_format$timestamp_added[i] <= as.IDate("2022-01-02")) {
      api_data_format$Year[i] <- 2021
    } # make first days of 2022 count for 2021
  }

  # Create a second continuous CalendarWeek variable
  # (It has to be checked whether a specific year has 52 or 53 weeks)

  data2019 <- subset(api_data_format, Year == "2019")
  data2019$CalendarWeek <- data2019$CalendarWeekYear

  data2020 <- subset(api_data_format, Year == "2020")
  data2020$CalendarWeek <- 52 + data2020$CalendarWeekYear

  data2021 <- subset(api_data_format, Year == "2021")
  data2021$CalendarWeek <- 52 + 53 + data2021$CalendarWeekYear

  data2022 <- subset(api_data_format, Year == "2022")
  data2022$CalendarWeek <- 52 + 53 + 52 + data2022$CalendarWeekYear

  api_data_with_time <- rbind(data2019, data2020, data2021, data2022)

  api_data_with_time <- api_data_with_time[order(api_data_with_time$timestamp_added), ] # sort by timestamp_added

  return(api_data_with_time)
}

# Save all given Hexagons and Calendar Weeks
# data_sorting = function(api_data_with_time){

#    return(api_data_with_time)
# }

unique_hexagons <- function(api_data_with_time) {
  # all.hex <-  select(api_data_with_time, location_hex)
  # all.hex = unique(all.hex)
  all.hex <- unique(api_data_with_time$location_hex)
  return(all.hex)
}

unique_calendar_weeks <- function(api_data_with_time) {
  all.CW <- unique(api_data_with_time$CalendarWeek)
  return(all.CW)
}

week_year <- function(api_data_with_time) {
  all.CWY <- cbind(api_data_with_time$CalendarWeekYear, api_data_with_time$Year)
  all.CWY <- all.CWY[!duplicated(all.CWY), ] %>% as.data.frame()
  return(all.CWY)
}

year_data <- function(all.CWY) {
  all.YEAR <- all.CWY$V2
  return(all.YEAR)
}

week_year_data <- function(all.CWY) {
  all.CWY <- all.CWY$V1
  return(all.CWY)
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

api_data <- read.csv(depends_on[["api_data"]]) # import the data set from the "hotspot_crawler.R" dataset

api_data_format <- data_format(api_data)
api_data_with_time <- add_time_variables(api_data_format)
api_data_with_time <- as.data.frame(api_data_with_time)
# api_data_with_time <- apply(api_data_with_time, 2, as.character)
write.csv(api_data_with_time, file = produces[["time_data"]], row.names = FALSE)

# Save all given Hexagons and Calendar Weeks
# all_sorted = data_sorting(api_data_with_time)
all.hex <- unique_hexagons(api_data_with_time)
all.CW <- unique_calendar_weeks(api_data_with_time)
all.CWY <- week_year(api_data_with_time)
all.YEAR <- year_data(all.CWY)
all.CWY <- week_year_data(all.CWY)

# all_sorted <- apply(all_sorted, 2, as.character)
all.hex <- lapply(all.hex, as.character)
all.hex <- transpose(as.data.frame(all.hex))
all.CW <- lapply(all.CW, as.character)
all.CW <- transpose(as.data.frame(all.CW))
all.CWY <- lapply(all.CWY, as.character)
all.CWY <- transpose(as.data.frame(all.CWY))
all.YEAR <- lapply(all.YEAR, as.character)
all.YEAR <- transpose(as.data.frame(all.YEAR))


# write.csv(all_sorted, file = produces[["all_sorted"]], row.names = FALSE)
write.csv(all.hex, file = produces[["all_hex"]], row.names = FALSE)
write.csv(all.CW, file = produces[["all_CW"]], row.names = FALSE)
write.csv(all.CWY, file = produces[["all_CWY"]], row.names = FALSE)
write.csv(all.YEAR, file = produces[["all_YEAR"]], row.names = FALSE)
