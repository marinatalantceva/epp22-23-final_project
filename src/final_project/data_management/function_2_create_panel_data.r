#Creating a panel dataset to use for predictions in later work

#This code takes about 3 minutes to run, since some dataframes are quite large.

# ======================================================================================
# Functions
# ======================================================================================
library(tidyverse)
library(dplyr)
library(data.table)


create_panel_data_starting_points = function(all.hex, all.CW, all.CWY, all.YEAR, time_data, results){
    
    #Making the dataframes to be matrixes
    all.hex = as.matrix(all.hex)
    all.CW = as.matrix(all.CW)
    all.CWY = as.matrix(all.CWY)
    all.YEAR = as.matrix(all.YEAR)

    #A loop for the results data frame
    for(hex in all.hex){
        hex.matrix <- matrix(0, nrow = length(all.CW), ncol = 5)

        #Create panel data columns.
        colnames(hex.matrix) <- c("location_hex", "CalendarWeek", "CalenderWeekYear", "Year", "NumberOfHotspots")
        hex.matrix[,1] <- hex
        hex.matrix[,2] <- all.CW
        hex.matrix[,3] <- all.CWY
        hex.matrix[,4] <- all.YEAR
        
        # Formatting columns
        hex.matrix <- hex.matrix %>% as.data.frame()
        hex.matrix$CalendarWeek <- hex.matrix$CalendarWeek %>% as.numeric()
        hex.matrix$CalenderWeekYear <- hex.matrix$CalenderWeekYear %>% as.numeric()
        hex.matrix$NumberOfHotspots <- hex.matrix$NumberOfHotspots %>% as.numeric()
        
        # Identify number of Hotspots that have been added to the blockchain in a given Calendar Week
        dummy <- time_data[time_data$location_hex == hex,] #filter for current hexagon
        word.count <- dummy %>% group_by(CalendarWeek) %>% summarise(count=n()) #create word count list
        colnames(word.count) <- c("CalendarWeek", "NumberOfHotspots")
        
        # Formatting columns
        word.count$CalendarWeek <- word.count$CalendarWeek %>% as.numeric()
        word.count$NumberOfHotspots <- word.count$NumberOfHotspots %>% as.numeric()
        
        # Merge dataframes 
        hex.results <- left_join(hex.matrix, word.count, by = c("CalendarWeek"))
        hex.results <- cbind(hex.results[1:4],
                       "NumberOfHotspots" = with(hex.results, ifelse(is.na(`NumberOfHotspots.y`), `NumberOfHotspots.x`, `NumberOfHotspots.y`)))
                       
        # Create additional column containing the cumulative number of hotspots
        hex.results <- hex.results %>% mutate(Hotspots.Cumul = cumsum(NumberOfHotspots))
        
        # Export results from for loop
        results <- rbind(results, hex.results)
        }
    return(results)
}


#The following code is made to include the neighbors of the hotspots into dataframe. We do not use them in our analysis, and therefore
#mute these lines of code to save the time running.

#Note:
#If you do not have h3jsr package installed, simply remove the muting sign from the following line and run pytask again
#remotes::install_github("obrl-soil/h3jsr")
#library(h3jsr)

#collecting_neighbours = function(results){
    # Collect the 6 neighbors of each hexagon
#    results.neigh <- results
#    
#    results.neigh$neighbor_1 <- NA
#    results.neigh$neighbor_2 <- NA
#    results.neigh$neighbor_3 <- NA
#    results.neigh$neighbor_4 <- NA
#    results.neigh$neighbor_5 <- NA
#    results.neigh$neighbor_6 <- NA
#    
#    for(i in seq(1, nrow(results.neigh), 1)) {
#        hex_loc <- results.neigh$location_hex[i]
#        
#        neighbors <- get_disk_list(h3_address = hex_loc, ring_size = 1)
#        results.neigh$neighbor_1[i] <- neighbors[[1]][[2]][1]
#        results.neigh$neighbor_2[i] <- neighbors[[1]][[2]][2]
#       results.neigh$neighbor_3[i] <- neighbors[[1]][[2]][3]
#        results.neigh$neighbor_4[i] <- neighbors[[1]][[2]][4]
#        results.neigh$neighbor_5[i] <- neighbors[[1]][[2]][5]
#        results.neigh$neighbor_6[i] <- neighbors[[1]][[2]][6]
#        if(i%%1000 == 0){print(i)} #Helps to keep track of loop progress 
#        }
#    return(results.neigh)
#}

# Collect the number of neighboring hotspots
#collecting_neighbours_cumulative = function(results.neigh){
#    data <- results.neigh
#    data$NeighborsCumul <- NA #creating a new columns that stores the number of neighboring hotspots
#    hex.unique <- unique(data$location_hex) #all hexagons that need to be iterated through
#    i <- 1
#
#    for(hex in hex.unique){
#        data.hex <- filter(data, grepl(hex, location_hex))
#        n1 <- data.hex$neighbor_1[1]
#        n2 <- data.hex$neighbor_2[1]
#        n3 <- data.hex$neighbor_3[1]
#        n4 <- data.hex$neighbor_4[1]
#        n5 <- data.hex$neighbor_5[1]
#        n6 <- data.hex$neighbor_6[1]
#        
#        data.n1 <- filter(data, grepl(n1, location_hex))
#        data.n2 <- filter(data, grepl(n2, location_hex))
#        data.n3 <- filter(data, grepl(n3, location_hex))
#        data.n4 <- filter(data, grepl(n4, location_hex))
#        data.n5 <- filter(data, grepl(n5, location_hex))
#        data.n6 <- filter(data, grepl(n6, location_hex))
        
#        if(nrow(rbind(data.n1, data.n2, data.n3, data.n4, data.n5, data.n6)) > 0){
#            data.neigh <- rbind(data.n1, data.n2, data.n3, data.n4, data.n5, data.n6)
#            
#            neigh.cumul <- aggregate(data.neigh$Hotspots.Cumul, list(data.neigh$CalendarWeek), sum)
#            neigh.cumul$location_hex <- hex
#            colnames(neigh.cumul) <- c("CalendarWeek", "NeighborsCumul", "location_hex")
#            
#            data <- left_join(data, neigh.cumul, by = c("CalendarWeek", "location_hex"))
#            data <- cbind(data[1:13],
#                     "NeighborsCumul"=with(data, ifelse(is.na(`NeighborsCumul.y`), `NeighborsCumul.x`, `NeighborsCumul.y`)))
#            if(i%%100 == 0){print(i)} #Helps to keep track of loop progress
#            i <- i + 1
#            }
#        }
#    return(data)
#}



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

#Downloading all the existing data
time_data = read.csv(depends_on[["time_data"]])      
all.hex = read.csv(depends_on[["all_hex"]])
all.CW = read.csv(depends_on[["all_CW"]])
all.CWY = read.csv(depends_on[["all_CWY"]])
all.YEAR =   read.csv(depends_on[["all_YEAR"]])

results = data.frame() #empty data frame that stores the loop results

#Running all the functions
data_without_neighbours = create_panel_data_starting_points(all.hex, all.CW, all.CWY, all.YEAR, time_data, results)
#data_with_neighbours = collecting_neighbours(data_without_neighbours)
#panel_data_with_neighbours_without_lag = collecting_neighbours_cumulative(data_with_neighbours)

#Saving all the datasets
write.csv(data_without_neighbours, file = produces[["data_without_neighbours"]], row.names = FALSE)
#write.csv(data_with_neighbours, file = produces[["data_with_neighbours"]], row.names = FALSE)
#write.csv(panel_data_with_neighbours_without_lag, file = produces[["panel_data_with_neighbours_without_lag"]], row.names = FALSE)
