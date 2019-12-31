require(ggplot2)
require(ggrepel)
require(tikzDevice)

coords <- data.frame(read.csv('language_locations.txt',header=F,sep='\t'))
colnames(coords) <- c('lang','code','lat','lon')

#coords$lang <- gsub('_','\\underline{\\phantom{X}}',coords$lang)
coords$lang <- gsub('_','.',coords$lang)

tikz('intro_map.tex',height=3,width=6)
ggplot()+
    borders(colour='peachpuff',fill='peachpuff')+coord_cartesian(xlim=c(-1.5,1.5)+range(coords$lon),ylim=c(-1.5,1.5)+range(coords$lat)) + 
	geom_point(data=unique(coords[,2:4]),aes(x=lon,y=lat)) + 
    geom_text_repel(data=unique(coords[,2:4]),aes(x=lon,y=lat,label=code),cex=2)+theme_bw()

dev.off()

#coords$lang_code <- paste(coords$lang,coords$code,'\\underline{\\phantom{X}}')
#coords$lang_code <- paste(coords$lang,coords$code,sep='.')


#tikz('intro_map.tex',height=3,width=6)
#ggplot()+
#    borders(colour='lightgray',fill='lightgray')+coord_cartesian(xlim=c(-1.5,1.5)+range(coords$lon),ylim=c(-1.5,1.5)+range(coords$lat)) + 
#	geom_point(data=coords,aes(x=lon,y=lat)) + 
#    geom_text_repel(data=coords,aes(x=lon,y=lat,label=lang_code),cex=2)+theme_bw()
#
#
#dev.off()