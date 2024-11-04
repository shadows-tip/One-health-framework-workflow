#导入数据集
library(readxl)
library(ggplot2)
library(dplyr)

A <- read.csv('D:/Picture/Cost-Effectiveness/肝吸虫病/ICER.csv')

colnames(A)[1] <- "Interventions"
A$Interventions[A$Interventions == 1] <- "Fish vaccination"
A$Interventions[A$Interventions == 2] <- "Chemotherapy"
A$Interventions[A$Interventions == 3] <- "IEC"
A$Interventions[A$Interventions == 4] <- "Sanitation toilets"

A$Interventions <- factor(A$Interventions,levels=c("Fish vaccination","Chemotherapy","IEC","Sanitation toilets")) 
A_Normalization <- A %>%
  group_by(Interventions) %>%
  mutate(ICER = (value - min(value)) / (max(value) - min(value)))
# Custom linetypes
linetype_values <- c("solid", "dashed", "dotted", "dotdash")  



P1 <- ggplot(A_Normalization, aes(x=cov, y=ICER)) + #*1e-08
  geom_line(aes(linetype = Interventions),size=0.8) +
  theme_bw() +
  scale_x_continuous(breaks=c(0,0.2,0.4,0.6,0.8,1)) +
  # scale_y_continuous(breaks=c(-1,0,1,2,3,4,5,6,7,8,9,10)) +   #labels = function(x) format(x, scientific=FALSE)
  theme(panel.grid=element_blank(),
        legend.position = c(0.78, 0.78),
        legend.title = element_text(size =16),
        legend.text = element_text(size =12),
        axis.text.x=element_text(vjust=1,size=13,color='black'),
        axis.text.y=element_text(vjust=1,size=13,color='black'),
        axis.title.x=element_text(size=16,color='black'),
        axis.title.y=element_text(size=16,color='black'),
        #plot.subtitle = element_text(size = 11),
        panel.border = element_rect(size = 1)) +
  labs(x="Coverage", y="Incremental cost-effectiveness ratio") + #,subtitle = "e+08"   
  scale_linetype_manual(values = linetype_values)
P1
ggsave(plot=plot, filename='./DataFolder/FigureFile/benefit_cost.png',
       dpi=500, width=5, height=5)


#x <- 3e-6
#print(x*1e6)

P1 <- ggplot(A, aes(x=cov, y=value*1e-06)) +
  geom_line(aes(linetype = Interventions),size=0.8) +
  theme_bw() +
  scale_x_continuous(breaks=c(0,0.2,0.4,0.6,0.8,1)) +
  #scale_y_continuous(breaks=c(0,0.5,1,1.5,2,2.5)) +   #labels = function(x) format(x, scientific=FALSE)
  theme(panel.grid=element_blank(),
        legend.position = c(0.78, 0.78),
        legend.title = element_text(size =12),
        legend.text = element_text(size =9),
        axis.text.x=element_text(vjust=1,size=15,color='black'),
        axis.text.y=element_text(vjust=1,size=15,color='black'),
        axis.title.x=element_text(size=17,color='black'),
        axis.title.y=element_text(size=17,color='black'),
        plot.subtitle = element_text(size = 12),
        panel.border = element_rect(size = 1)) +
  labs(x="Coverage", y="Effectiveness/cost \n(DALY/$)",subtitle = "e-06")
