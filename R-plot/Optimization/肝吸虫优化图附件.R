#导入数据集
library(readxl)
library(stringr)
library(ggplot2)
library(ggpubr)
##########################肝吸虫图片保存width=1200,height=350
####Single interventions 
C <- read.csv('D:/Picture/Optim/肝吸虫优化图/Optim241014(cases).csv')
C$object_value = - C$object_value

C$object_value[C$object_value == -500] <- 1
C$object_value[C$object_value == -1000] <- 2
C$object_value[C$object_value == -1500] <- 3
C$object_value[C$object_value == -2000] <- 4
C$object_value[C$object_value == -2500] <- 5

#########################1
C11_1 <- subset(C,(C$interv_measure==1)&(C$year==1))
C11_3 <- subset(C,(C$interv_measure==1)&(C$year==3))
C11_5 <- subset(C,(C$interv_measure==1)&(C$year==5))
C11 <- rbind(C11_1,C11_3,C11_5)
C11$interv_measure[C11$interv_measure==1] <- "Fish vaccination(Efficacy=0.99)"
C11$year[C11$year==1] <- "One year's intervention"
C11$year[C11$year==3] <- "Three years' intervention"
C11$year[C11$year==5] <- "Five years' intervention"

opt_param_ranges_10= c(0,1) #优化参数范围
low_color_10 = c("#9ecae1")
high_color_10 = c("#0D539c")

C11=C11 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C11$year <- factor(C11$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C11$object_value = - C11$object_value


C11a <- ggplot(C11, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C11$interv_measure) +
  scale_fill_gradient(low = low_color_10, high = high_color_10, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_10 ) 


#########################2
C12_1 <- subset(C,(C$interv_measure==2)&(C$year==1))
C12_3 <- subset(C,(C$interv_measure==2)&(C$year==3))
C12_5 <- subset(C,(C$interv_measure==2)&(C$year==5))
C12 <- rbind(C12_1,C12_3,C12_5)
C12$interv_measure[C12$interv_measure==2] <- "Chemotherapy(Efficacy=0.92)"
C12$year[C12$year==1] <- "One year's intervention"
C12$year[C12$year==3] <- "Three years' intervention"
C12$year[C12$year==5] <- "Five years' intervention"

opt_param_ranges_11= c(0,1) #优化参数范围
low_color_11 = c("#9ecae1")
high_color_11 = c("#0D539c")

C12=C12 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C12$year <- factor(C12$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C12$object_value = - C12$object_value

C12a <- ggplot(C12, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C12$interv_measure) +
  scale_fill_gradient(low = low_color_11, high = high_color_11, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_11 ) 


#########################3
C13_1 <- subset(C,(C$interv_measure==3)&(C$year==1))
C13_3 <- subset(C,(C$interv_measure==3)&(C$year==3))
C13_5 <- subset(C,(C$interv_measure==3)&(C$year==5))
C13 <- rbind(C13_1,C13_3,C13_5)
C13$interv_measure[C13$interv_measure==3] <- "IEC(Efficacy=0.5408)"
C13$year[C13$year==1] <- "One year's intervention"
C13$year[C13$year==3] <- "Three years' intervention"
C13$year[C13$year==5] <- "Five years' intervention"

opt_param_ranges_12= c(0,1) #优化参数范围
low_color_12 = c("#9ecae1")
high_color_12 = c("#0D539c")

C13=C13 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C13$year <- factor(C13$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C13$object_value = - C13$object_value

C13a <- ggplot(C13, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C13$interv_measure) +
  scale_fill_gradient(low = low_color_12, high = high_color_12, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_12 ) 

#########################4
C14_1 <- subset(C,(C$interv_measure==4)&(C$year==1))
C14_3 <- subset(C,(C$interv_measure==4)&(C$year==3))
C14_5 <- subset(C,(C$interv_measure==4)&(C$year==5))
C14 <- rbind(C14_1,C14_3,C14_5)
C14$interv_measure[C14$interv_measure==4] <- "Sanitation toilets(Efficacy=1)"
C14$year[C14$year==1] <- "One year's intervention"
C14$year[C14$year==3] <- "Three years' intervention"
C14$year[C14$year==5] <- "Five years' intervention"

opt_param_ranges_13= c(0,1) #优化参数范围
low_color_13 = c("#9ecae1")
high_color_13 = c("#0D539c")

C14=C14 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C14$year <- factor(C14$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C14$object_value = - C14$object_value

C14a <- ggplot(C14, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C14$interv_measure) +
  scale_fill_gradient(low = low_color_13, high = high_color_13, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_13 ) 







####Combination interventions 
C <- read.csv('D:/Picture/Optim/肝吸虫优化图/Optim241014(cases).csv')
C$object_value = - C$object_value

C$object_value[C$object_value == -500] <- 1
C$object_value[C$object_value == -1000] <- 2
C$object_value[C$object_value == -1500] <- 3
C$object_value[C$object_value == -2000] <- 4
C$object_value[C$object_value == -2500] <- 5

#########################12
C1_1 <- subset(C,(C$interv_measure==12)&(C$year==1))
C1_3 <- subset(C,(C$interv_measure==12)&(C$year==3))
C1_5 <- subset(C,(C$interv_measure==12)&(C$year==5))
C1 <- rbind(C1_1,C1_3,C1_5)
C1$interv_measure[C1$interv_measure==12] <- "Fish vaccination(Efficacy=0.99)+Chemotherapy(Efficacy=0.92)"
C1$year[C1$year==1] <- "One year's intervention"
C1$year[C1$year==3] <- "Three years' intervention"
C1$year[C1$year==5] <- "Five years' intervention"

opt_param_ranges= c(0,1) #优化参数范围
low_color = c("#80CDC1")
high_color = c("#01665E")

C1=C1 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C1$year <- factor(C1$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C1$object_value = - C1$object_value

C1a <- ggplot(C1, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C1$interv_measure) +
  scale_fill_gradient(low = low_color, high = high_color, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges ) 

#########################13
C2_1 <- subset(C,(C$interv_measure==13)&(C$year==1))
C2_3 <- subset(C,(C$interv_measure==13)&(C$year==3))
C2_5 <- subset(C,(C$interv_measure==13)&(C$year==5))
C2 <- rbind(C2_1,C2_3,C2_5)
C2$interv_measure[C2$interv_measure==13] <- "Fish vaccination(Efficacy=0.99)+IEC(Efficacy=0.5408)"
C2$year[C2$year==1] <- "One year's intervention"
C2$year[C2$year==3] <- "Three years' intervention"
C2$year[C2$year==5] <- "Five years' intervention"

opt_param_ranges_1= c(0,1) #优化参数范围
low_color_1 = c("#80CDC1")
high_color_1 = c("#004529")

C2=C2 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C2$year <- factor(C2$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C2$object_value = - C2$object_value

C2a<- ggplot(C2, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C2$interv_measure) +
  scale_fill_gradient(low = low_color_1, high = high_color_1, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_1 ) 

#########################14
C3_1 <- subset(C,(C$interv_measure==14)&(C$year==1))
C3_3 <- subset(C,(C$interv_measure==14)&(C$year==3))
C3_5 <- subset(C,(C$interv_measure==14)&(C$year==5))
C3 <- rbind(C3_1,C3_3,C3_5)
C3$interv_measure[C3$interv_measure==14] <- "Fish vaccination(Efficacy=0.99)+Sanitation toilets(Efficacy=1)"
C3$year[C3$year==1] <- "One year's intervention"
C3$year[C3$year==3] <- "Three years' intervention"
C3$year[C3$year==5] <- "Five years' intervention"

opt_param_ranges_2= c(0,1) #优化参数范围
low_color_2 = c("#80CDC1")
high_color_2 = c("#004529")

C3=C3 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C3$year <- factor(C3$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C3$object_value = - C3$object_value

C3a <- ggplot(C3, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C3$interv_measure) +
  scale_fill_gradient(low = low_color_2, high = high_color_2, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_2 ) 


#########################23
C4_1 <- subset(C,(C$interv_measure==23)&(C$year==1))
C4_3 <- subset(C,(C$interv_measure==23)&(C$year==3))
C4_5 <- subset(C,(C$interv_measure==23)&(C$year==5))
C4 <- rbind(C4_1,C4_3,C4_5)
C4$interv_measure[C4$interv_measure==23] <- "Chemotherapy(Efficacy=0.92)+IEC(Efficacy=0.5408)"
C4$year[C4$year==1] <- "One year's intervention"
C4$year[C4$year==3] <- "Three years' intervention"
C4$year[C4$year==5] <- "Five years' intervention"

opt_param_ranges_3= c(0,1) #优化参数范围
low_color_3 = c("#9E9AC8")
high_color_3 = c("#3F007D")

C4=C4 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C4$year <- factor(C4$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C4$object_value = - C4$object_value

C4a <- ggplot(C4, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C4$interv_measure) +
  scale_fill_gradient(low = low_color_3, high = high_color_3, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_3 ) 

#########################24
C5_1 <- subset(C,(C$interv_measure==24)&(C$year==1))
C5_3 <- subset(C,(C$interv_measure==24)&(C$year==3))
C5_5 <- subset(C,(C$interv_measure==24)&(C$year==5))
C5 <- rbind(C5_1,C5_3,C5_5)
C5$interv_measure[C5$interv_measure==24] <- "Chemotherapy(Efficacy=0.92)+Sanitation toilets(Efficacy=1)"
C5$year[C5$year==1] <- "One year's intervention"
C5$year[C5$year==3] <- "Three years' intervention"
C5$year[C5$year==5] <- "Five years' intervention"

opt_param_ranges_4= c(0,1) #优化参数范围
low_color_4 = c("#9E9AC8")
high_color_4 = c("#3F007D")

C5=C5 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C5$year <- factor(C5$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C5$object_value = - C5$object_value

C5a <- ggplot(C5, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C5$interv_measure) +
  scale_fill_gradient(low = low_color_4, high = high_color_4, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_4 ) 

#########################34
C6_1 <- subset(C,(C$interv_measure==34)&(C$year==1))
C6_3 <- subset(C,(C$interv_measure==34)&(C$year==3))
C6_5 <- subset(C,(C$interv_measure==34)&(C$year==5))
C6 <- rbind(C6_1,C6_3,C6_5)
C6$interv_measure[C6$interv_measure==34] <- "IEC(Efficacy=0.5408)+Sanitation toilets(Efficacy=1)"
C6$year[C6$year==1] <- "One year's intervention"
C6$year[C6$year==3] <- "Three years' intervention"
C6$year[C6$year==5] <- "Five years' intervention"

opt_param_ranges_5= c(0,1) #优化参数范围
low_color_5 = c("#9E9AC8")
high_color_5 = c("#3F007D")

C6=C6 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C6$year <- factor(C6$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C6$object_value = - C6$object_value

C6a <- ggplot(C6, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C6$interv_measure) +
  scale_fill_gradient(low = low_color_5, high = high_color_5, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_5 ) 

#########################123
C7_1 <- subset(C,(C$interv_measure==123)&(C$year==1))
C7_3 <- subset(C,(C$interv_measure==123)&(C$year==3))
C7_5 <- subset(C,(C$interv_measure==123)&(C$year==5))
C7 <- rbind(C7_1,C7_3,C7_5)
C7$interv_measure[C7$interv_measure==123] <- "Fish vaccination(Efficacy=0.99)+Chemotherapy(Efficacy=0.92)+IEC(Efficacy=0.5408)"
C7$year[C7$year==1] <- "One year's intervention"
C7$year[C7$year==3] <- "Three years' intervention"
C7$year[C7$year==5] <- "Five years' intervention"

opt_param_ranges_6= c(0,1) #优化参数范围
low_color_6 = c("#C6DBEF")
high_color_6 = c("#4292C6")

C7=C7 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C7$year <- factor(C7$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C7$object_value = - C7$object_value

C7a <- ggplot(C7, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C7$interv_measure) +
  scale_fill_gradient(low = low_color_6, high = high_color_6, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_6 ) 

#########################124
C8_1 <- subset(C,(C$interv_measure==124)&(C$year==1))
C8_3 <- subset(C,(C$interv_measure==124)&(C$year==3))
C8_5 <- subset(C,(C$interv_measure==124)&(C$year==5))
C8 <- rbind(C8_1,C8_3,C8_5)
C8$interv_measure[C8$interv_measure==124] <- "Fish vaccination(Efficacy=0.99)+Chemotherapy(Efficacy=0.92)+Sanitation toilets(Efficacy=1)"
C8$year[C8$year==1] <- "One year's intervention"
C8$year[C8$year==3] <- "Three years' intervention"
C8$year[C8$year==5] <- "Five years' intervention"

opt_param_ranges_7= c(0,1) #优化参数范围
low_color_7 = c("#C6DBEF")
high_color_7 = c("#4292C6")

C8=C8 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C8$year <- factor(C8$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C8$object_value = - C8$object_value

C8a <- ggplot(C8, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C8$interv_measure) +
  scale_fill_gradient(low = low_color_7, high = high_color_7, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_7) 

#########################234
C9_1 <- subset(C,(C$interv_measure==234)&(C$year==1))
C9_3 <- subset(C,(C$interv_measure==234)&(C$year==3))
C9_5 <- subset(C,(C$interv_measure==234)&(C$year==5))
C9 <- rbind(C9_1,C9_3,C9_5)
C9$interv_measure[C9$interv_measure==234] <- "Chemotherapy(Efficacy=0.92)+IEC(Efficacy=0.5408)+Sanitation toilets(Efficacy=1)"
C9$year[C9$year==1] <- "One year's intervention"
C9$year[C9$year==3] <- "Three years' intervention"
C9$year[C9$year==5] <- "Five years' intervention"

opt_param_ranges_8= c(0,1) #优化参数范围
low_color_8 = c("#C6DBEF")
high_color_8 = c("#4292C6")

C9=C9 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C9$year <- factor(C9$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C9$object_value = - C9$object_value

C9a <- ggplot(C9, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C9$interv_measure) +
  scale_fill_gradient(low = low_color_8, high = high_color_8, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_8) 

#########################1234
C10_1 <- subset(C,(C$interv_measure==1234)&(C$year==1))
C10_3 <- subset(C,(C$interv_measure==1234)&(C$year==3))
C10_5 <- subset(C,(C$interv_measure==1234)&(C$year==5))
C10 <- rbind(C10_1,C10_3,C10_5)
C10$interv_measure[C10$interv_measure==1234] <- "Fish vaccination(Efficacy=0.99)+Chemotherapy(Efficacy=0.92)+IEC(Efficacy=0.5408)+Sanitation toilets(Efficacy=1)"
C10$year[C10$year==1] <- "One year's intervention"
C10$year[C10$year==3] <- "Three years' intervention"
C10$year[C10$year==5] <- "Five years' intervention"

opt_param_ranges_9= c(0,1) #优化参数范围
low_color_9 = c("#C6DBEF")
high_color_9 = c("#4292C6")

C10=C10 %>% dplyr::mutate(object_value=ifelse(object_value == -1,0,object_value))
C10$year <- factor(C10$year,levels = c("One year's intervention","Three years' intervention","Five years' intervention"))
C10$object_value = - C10$object_value

C10a <- ggplot(C10, aes(scene, object_value, fill= min_coverage)) + 
  geom_tile(width=1) +
  theme_bw(base_size=11.5) + 
  facet_wrap(~year,nrow=1,scales = 'free_x') +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = 'white'),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x=element_text(vjust=1,size=9),
        legend.title=element_text(size=10)) + #标题的位置
  theme(strip.background = element_rect( fill="white")) +
  scale_x_continuous(breaks=c(1,2,3,4,5,6),labels=c('scene1','scene2','scene3','scene4','scene5','scene6')) +
  scale_y_continuous(breaks=c(-5,-4,-3,-2,-1),labels=c('2500','2000','1500','1000','500')) +
  labs(x="Transmission level", y="Target Health Goal \n(1/60000)",subtitle = C10$interv_measure) +
  scale_fill_gradient(low = low_color_9, high = high_color_9, na.value = "white",
                      name="Minimum \nCoverage",limits = opt_param_ranges_9) 


C11a/C12a/C13a/C14a/C1a/C2a/C3a/C4a/C5a/C6a/C7a/C8a/C9a/C10a

