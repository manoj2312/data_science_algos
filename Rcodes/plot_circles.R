rm(list=ls())
library(ggplot2)
library(igraph)
# gd <- graph(c(1,2, 2,1, 2,3, 2,4, 1,4, 5,5, 3,6))
# plot(gd)
library(gcookbook)
col1 = madmen$Name1
col2 = madmen$Name2
for(name in col1){
  name = strsplit(name, split =" ")[[1]][1]
}
for(name in col2){
  name = strsplit(name, split =" ")[[1]][1]
}
newcol1 = c(col1,col2)
newcol2 = c(col2,col1)
data = data.frame(newcol1,newcol2)
g <- graph.data.frame(data, directed=TRUE)
par(mar=c(0,0,0,0))
plot(g, layout=layout.fruchterman.reingold, vertex.size=8, edge.arrow.size=0.5)


# g <- graph.data.frame(madmen, directed=FALSE)
# par(mar=c(0,0,0,0)) # Remove unnecessary margins
# plot(g, layout=layout.circle, vertex.size=8)

# plot(x=c(1,3), y = c(5,5), fg = "white", bg = "blue", bty='o',
#      xlab = "", ylab = "", main = "Supply Demand Matching",
#      xlim = c(0,4), ylim = c(0,9), xaxt='n', yaxt = 'n')
# symbols(x=c(1,3), y = c(5,5), circles = c(2,2), inches = 1, add = T, fg="black", bg="gray")
# matplot(x=c(1,1,1,1,1), y=c(3,4,5,6,7), type = "p",col ="blue",pch =2, add =TRUE)
# matplot(x=c(3,3,3,3,3), y=c(3,4,5,6,7), type = "p",col = "red", pch = 6, add =TRUE)
# matplot(x=c(1,3), y=c(7,5), type = "l",pch =2, add =TRUE)
# matplot(x=c(1,3), y=c(6,4), type = "l",pch =2, add =TRUE)
# matplot(x=c(1,3), y=c(5,3), type = "l",pch =2, add =TRUE)
# matplot(x=c(1,3), y=c(4,7), type = "l",pch =2, add =TRUE)
# matplot(x=c(1,3), y=c(3,6), type = "l",pch =2, add =TRUE)

# circleFun <- function(center = c(0,0),diameter = 1, npoints = 100){
#   r = diameter / 2
#   tt <- seq(0,2*pi,length.out = npoints)
#   xx <- center[1] + r * cos(tt)
#   yy <- center[2] + r * sin(tt)
#   return(data.frame(x = xx, y = yy))
# }
# 
# dat1 <- circleFun(c(2,6), 2, npoints = 100)
# dat2 <- circleFun(c(6,6), 2, npoints = 100)
# #geom_path will do open circles, geom_polygon will do filled circles
# print(ggplot(dat1,aes(x,y)) + geom_polygon() + geom_polygon(data = dat2), aes(x,y))