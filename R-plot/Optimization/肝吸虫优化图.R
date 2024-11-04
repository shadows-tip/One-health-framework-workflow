#导入数据集
library(readxl)
library(stringr)
library(ggplot2)
library(ggpubr)
B <- read.csv('C:/Users/ASUS/Desktop/Picture/Optim/肝吸虫优化图/Optim0909.csv')
B$object_value = - B$object_value
table(B$object_value)



####Single interventions
B1_2 <- subset(B,(B$interv_measure==2)&(B$year==3))
B1_3 <- subset(B,(B$interv_measure==3)&(B$year==3))
B1_4 <- subset(B,(B$interv_measure==4)&(B$year==3))
B1_1 <- subset(B,(B$interv_measure==1)&(B$year==3))
B2_1 <- subset(B,(B$interv_measure==12)&(B$year==3))
B2_2 <- subset(B,(B$interv_measure==123)&(B$year==3))
B2_3 <- subset(B,(B$interv_measure==124)&(B$year==3))
B2_4 <- subset(B,(B$interv_measure==1234)&(B$year==3))
B1 <- rbind(B1_2,B1_3,B1_4,B1_1,B2_1,B2_2,B2_3,B2_4)

B1$object_value[B1$object_value == -750] <- 1
B1$object_value[B1$object_value == -1000] <- 2
B1$object_value[B1$object_value == -1250] <- 3
B1$object_value[B1$object_value == -1500] <- 4
B1$object_value[B1$object_value == -1700] <- 5

B1$interv_measure[B1$interv_measure == 2] <- "Chemotherapy(Efficacy=0.92)"
B1$interv_measure[B1$interv_measure == 3] <- "IEC(Efficacy=0.5408)"
B1$interv_measure[B1$interv_measure == 4] <- "Sanitation toilets(Efficacy=1)"
B1$interv_measure[B1$interv_measure == 1] <- "Fish vaccination(Efficacy=0.8)"
B1$interv_measure[B1$interv_measure == 12] <- "Fish vaccination(Efficacy=0.8)+ \nChemotherapy(Efficacy=0.92)"
B1$interv_measure[B1$interv_measure == 123] <- "Fish vaccination(Efficacy=0.8)+ \n Chemotherapy(Efficacy=0.92)+IEC(Efficacy=0.5408)"
B1$interv_measure[B1$interv_measure == 124] <- "Fish vaccination(Efficacy=0.8)+ \n Chemotherapy(Efficacy=0.92)+ \nSanitation toilets(Efficacy=1)"
B1$interv_measure[B1$interv_measure == 1234] <- "Fish vaccination(Efficacy=0.8)+ \n Chemotherapy(Efficacy=0.92)+IEC(Efficacy=0.5408)+ \n Sanitation toilets(Efficacy=1)"

opt_param_ranges= c(0,1) #优化参数范围
low_color = c("#9E9AC8")
high_color = c("#3F007D")
#[1] "#FCFBFD" "#EFEDF5" "#DADAEB" "#BCBDDC" "#9E9AC8" "#807DBA" "#6A51A3" "#54278F" "#3F007D"

B1=B1 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
B1$interv_measure <- factor(B1$interv_measure,levels = c("Chemotherapy(Efficacy=0.92)","IEC(Efficacy=0.5408)","Sanitation toilets(Efficacy=1)","Fish vaccination(Efficacy=0.8)",
                                                         "Fish vaccination(Efficacy=0.8)+ \nChemotherapy(Efficacy=0.92)",
                                                         "Fish vaccination(Efficacy=0.8)+ \n Chemotherapy(Efficacy=0.92)+IEC(Efficacy=0.5408)",
                                                         "Fish vaccination(Efficacy=0.8)+ \n Chemotherapy(Efficacy=0.92)+ \nSanitation toilets(Efficacy=1)",
                                                         "Fish vaccination(Efficacy=0.8)+ \n Chemotherapy(Efficacy=0.92)+IEC(Efficacy=0.5408)+ \n Sanitation toilets(Efficacy=1)"))

B1$object_value = - B1$object_value

P1 <- ggplot(B1, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1.5) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~interv_measure,nrow=2,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.title = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('1700','1500','1250','1000','750')) +
  labs(x="Transmission level", y="Target Health Goal",title = "Three Years' Intervention") +
  scale_fill_gradient(low = low_color, high = high_color, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges ) 





###################################################################
B1_2 <- subset(B,(B$interv_measure==2)&(B$year==3))
B2_1 <- subset(B,(B$interv_measure==12)&(B$year==3))
B3_1 <- subset(B,(B$interv_measure==23)&(B$year==3))
B3_2 <- subset(B,(B$interv_measure==24)&(B$year==3))
B2 <- rbind(B1_2,B2_1,B3_1,B3_2)

B2$object_value[B2$object_value == -750] <- 1
B2$object_value[B2$object_value == -1000] <- 2
B2$object_value[B2$object_value == -1250] <- 3
B2$object_value[B2$object_value == -1500] <- 4
B2$object_value[B2$object_value == -1700] <- 5

B2$interv_measure[B2$interv_measure == 2] <- "Chemotherapy(Efficacy=0.92)"
B2$interv_measure[B2$interv_measure == 12] <- "Chemotherapy(Efficacy=0.92)+ \n Fish vaccination(Efficacy=0.8)"
B2$interv_measure[B2$interv_measure == 23] <- "Chemotherapy(Efficacy=0.92)+ \n IEC(Efficacy=0.5408)"
B2$interv_measure[B2$interv_measure == 24] <- "Chemotherapy(Efficacy=0.92)+ \n Sanitation toilets(Efficacy=1)"

opt_param_ranges_1= c(0,1) #优化参数范围
low_color_1 = c("#9E9AC8")
high_color_1 = c("#3F007D")

B2=B2 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
B2$interv_measure <- factor(B2$interv_measure,levels = c("Chemotherapy(Efficacy=0.92)",
                                                         "Chemotherapy(Efficacy=0.92)+ \n Fish vaccination(Efficacy=0.8)",
                                                         "Chemotherapy(Efficacy=0.92)+ \n IEC(Efficacy=0.5408)",
                                                         "Chemotherapy(Efficacy=0.92)+ \n Sanitation toilets(Efficacy=1)"))

B2$object_value = - B2$object_value

P2 <- ggplot(B2, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1.5) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~interv_measure,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.title = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('1700','1500','1250','1000','750')) +
  labs(x="Transmission level", y="Target Health Goal",title = "Three Years' Intervention") +
  scale_fill_gradient(low = low_color_1, high = high_color_1, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_1 ) 
