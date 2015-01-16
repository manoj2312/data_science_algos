rm(list=ls())
library(ggplot2)
data.mat = read.csv("/home/jarvis/Documents/MeanReversion/MeanreversionEndOfStage1/Data for Mean RevesionProject.csv", header=TRUE)
stock.ratio=data.mat$Stock2/data.mat$Stock1
Time = 1:length(data.mat$Date)

mov_avg_var = function(data, window){
  mov_avg = rep(mean(data[1:window]),length(data))
  mov_var = rep(sd(data[1:window]),length(data))
  for(i in window:length(data)){
    mov_avg[i] = mean(data[seq(i-window+1, i, 1)])
    if(is.na(mov_avg[i])){
      print("NA found")
    }
  }
  result = data.frame(mov_avg, mov_var)
  return(result)
}
mov_avg_var_val = mov_avg_var(stock.ratio, 20)

# print( ggplot()
#        + ggtitle("Illustration of Mean Reversion")
# #        + geom_line(aes(Time, stock.ratio), colour = "blue")
#        + geom_line(aes(Time, stock.ratio, colour = "data")))

print( ggplot()
       + ggtitle("Illustration of Mean Reversion")
       + geom_line(aes(Time, stock.ratio, colour = "Stock ratio" ))
       + geom_line(data = mov_avg_var_val, aes(1:length(mov_avg),mov_avg, colour = "Moving average"), alpha = 1)
       + geom_line(data = mov_avg_var_val, aes(1:length(mov_var),mov_avg + 2*mov_var, colour = "Bollinger Bands\nwith 2 sigma"), alpha = 1)
       + geom_line(data = mov_avg_var_val, aes(1:length(mov_var),mov_avg - 2*mov_var, colour = "Bollinger Bands\nwith 2 sigma"), alpha = 1)
       + xlab("Time(in Days)")
       + ylab("Ratio of pair trading stocks")
       + theme(
         panel.grid.major = element_line(colour="green", linetype="dashed", size=0.2),
         panel.grid.minor = element_line(colour="green", linetype="dashed", size=0.2),
         panel.background = element_rect(fill="black"),
         panel.border = element_rect(colour="gray", fill=NA, size=2),
         axis.title.x = element_text(size = 20, colour = "cyan"),
         axis.title.y = element_text(size = 20, colour = "cyan"),
         axis.ticks.x = element_line(size = 2),
         axis.ticks.y = element_line(size = 2),
         plot.title=element_text(hjust = 0.5, vjust = -2.5, size = 20, colour = 'cyan'),
         plot.background = element_rect(fill = "black"),
         legend.background = element_rect(colour = "green"),
         legend.text = element_text(colour = "black", size = 12),
         legend.position = c(1,0.75), legend.justification = c(1,0))
       + scale_color_discrete(name="Mean Reversion")
       )