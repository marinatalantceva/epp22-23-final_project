# Downloading data from URL

library(tidyverse)
library(readr)
library(data.table)

# Matching the coordinates with URL
url_with_coordinates <- function(url, swlat, swlon, nelat, nelon) {
  base_url <- paste0(url, "swlat=", swlat, "&swlon=", swlon, "&nelat=", nelat, "&nelon=", nelon)
  return(base_url)
}

# Downloading the data from URL
calling_api <- function(base_url) {
  ## call API:
  api_call <- httr::GET(base_url)
  return(api_call)
}

character_api <- function(api_call) {
  ## convert response to usable data:
  api_char <- rawToChar(api_call$content)
  return(api_char)
}

JSON_api <- function(api_char) {
  ## convert response to usable data:
  api_JSON <- jsonlite::fromJSON(api_char, flatten = TRUE)
  return(api_JSON)
}

download_from_url <- function(base_url, api_call, api_char, api_JSON) {
  api_data <- api_JSON[["data"]]
  cursor <- api_JSON[["cursor"]]
  for (i in 1:1000) {
    print(paste0(i, " = ", cursor))
    full_url <- paste0(base_url, "&cursor=", cursor)
    api_call <- httr::GET(full_url)
    api_char <- rawToChar(api_call$content)
    api_JSON <- jsonlite::fromJSON(api_char, flatten = TRUE)
    api_data <- rbind(api_data, api_JSON[["data"]])
    if (is.null(api_JSON[["cursor"]])) {
      break
    }
    cursor <- api_JSON[["cursor"]]
    Sys.sleep(1) # loop sleep might need to be increased when api is "too busy"
  }
  unique(api_data$name) %>% length()
  return(api_data)
}

# ======================================================================================
# Get produces and depends_on from pytask
# ======================================================================================

args <- commandArgs(trailingOnly = TRUE)
path_to_yaml <- args[length(args)]
config <- yaml::yaml.load_file(path_to_yaml)

produces <- config[["produces"]]

# ======================================================================================
# Main
# ======================================================================================
swlat <- 40.593 # South West latitude
swlon <- -74.048 # South West longitude
nelat <- 40.812 # North East latitude
nelon <- -73.88 # North East longitude
url <- "https://api.helium.io/v1/hotspots/location/box/?"
base_url <- url_with_coordinates(url, swlat, swlon, nelat, nelon)
api_call <- calling_api(base_url)
api_char <- character_api(api_call)
api_JSON <- JSON_api(api_char)
api_data <- download_from_url(base_url, api_call, api_char, api_JSON)
api_data <- apply(api_data, 2, as.character)
write.csv(api_data, file = produces, row.names = FALSE)
# fwrite(api_data, file =produces, row.names=FALSE)
