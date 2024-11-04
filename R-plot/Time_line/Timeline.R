#导入数据集
library(readxl)
library(ggplot2)
A1 <- read.csv('timeline_data.csv') # 19346:38690:single
P <- read.csv('timeline_data_co.csv') # combined

A1$Interventions[A1$Interventions == 2] <- 0
A11 <- A1[c(19346:38690),]
A12 <- rbind(A11,P)


A12$Interventions[A12$Interventions == 0] <- "Chemotherapy"
A12$Interventions[A12$Interventions == 2] <- "No Intervention"
A12$Interventions[A12$Interventions == 12] <- "Fish vaccination"
A12$Interventions[A12$Interventions == 23] <- "IEC"
A12$Interventions[A12$Interventions == 24] <- "Sanitation toilets"


A12$Interventions <- factor(A12$Interventions,levels=c('Chemotherapy','No Intervention','Fish vaccination','IEC','Sanitation toilets'))

timeline_plot_A <- ggplot(A12, aes(day/30, y=med_Ih, ymin=min_Ih, ymax=max_Ih, fill=Interventions)) + 
  geom_line(aes(linetype = Interventions)) + 
  geom_ribbon(alpha=0.5) + 
  scale_x_continuous(breaks=c(0,36,72,120,180,240,300,360,420,480,540,600)) +
  scale_fill_manual(values=c("No Intervention" = "#E31A1C","Fish vaccination" = "#80CDC1","Chemotherapy" = "#004529","IEC" = "#4292C6","Sanitation toilets" = "#E76BF3")) +  
  theme_bw() +  
  theme(legend.title = element_text(size =13),
               legend.text = element_text(size = 12),
               #legend.position = c(0.85, 0.83),
               panel.grid=element_blank(),
               panel.border = element_rect(size = 1),
               axis.text.x=element_text(vjust=1,size=13,color='black'),
               axis.text.y=element_text(vjust=1,size=13,color='black'),
               axis.title.x=element_text(size=16,color='black'),
               axis.title.y=element_text(size=16,color='black'))  + #去掉画布的网格线
  labs(x="Months", y="Number of infected people \n(1/20,000)", fill="Interventions", linetype='Interventions') 
timeline_plot_A 