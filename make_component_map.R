require(ggplot2)
require(ggrepel)
require(scatterpie)
require(tikzDevice)

comp <- read.table('iran_components.txt',header=F)


comp[,5:ncol(comp)][comp[,5:ncol(comp)] < .05] <- 0

#comp[,5:ncol(comp)] <- comp[,5:ncol(comp)]-.05
#comp[,5:ncol(comp)][comp[,5:ncol(comp)] < 0] <- 0

colnames(comp)[1:4] <- c('lang','glotto','lat','lon')



world <- map_data('world')

cbp1 <- c(#"#999999", 
          "#E69F00", 
          "#56B4E9",
          "#F0E442",
          "#009E73",
          "#0072B2", 
          "#D55E00", 
          "#CC79A7")


#pdf('iran_component_map.pdf',width=9,height=6)
tikz('iran_component_map.tex',width=9,height=6)
ggplot() + borders(colour='lightgray',fill='lightgray') +  coord_cartesian(xlim=c(-1.5,1.5)+range(comp$lon),ylim=c(-1.5,1.5)+range(comp$lat)) +	
  geom_scatterpie(aes(x=lon, y=lat, r=.5), data=comp, cols=colnames(comp)[5:ncol(comp)], color=NA, alpha=.8) + 
  geom_text_repel(data=comp,aes(x=lon,y=lat,label=lang),cex=2)+theme_bw() + scale_fill_manual(values=cbp1) + 
  theme(legend.position="none")


dev.off()



#p <- #ggplot(world, aes(lon, lat)) +
#geom_map(map=world, aes(map_id=region), fill=NA, color="black") +
#coord_quickmap()
#ggplot() + borders(colour='lightgray',fill='lightgray') +  coord_cartesian(xlim=c(-1.5,1.5)+range(coords$lon),ylim=c(-1.5,1.5)+range(coords$lat)) +	
#  geom_scatterpie(aes(x=lon, y=lat, r=1.25),
#                  data=coords, cols=c('k=1','k=2','k=3'), color=NA, alpha=.8) + 
#  theme(legend.position="none")




#ggplot() + borders(colour='lightgray',fill='lightgray') +  coord_cartesian(xlim=c(-1.5,1.5)+range(coords$lon),ylim=c(-1.5,1.5)+range(coords$lat)) +	geom_text_repel(data=coords,aes(x=lon,y=lat,label=lang),cex=2)+theme_bw() + geom_scatterpie(aes(x=lon, y=lat, r=1.25), data=coords, cols=c('k=1','k=2','k=3'), color=NA, alpha=.8)