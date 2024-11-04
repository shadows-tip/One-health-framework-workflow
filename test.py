from ModelPackage.SimulationModel import Model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# model = Model(t=150, ratio=0.4)
# model.set_param(intervene_meas=13, intervene_param=[0.923350617195189, 0.8, 0.923350617195189, 0.5408], intervene_time=100)
# out = np.sum(model.get_result(label=['Ih1', 'Ih2', 'Ih3', 'Ih4'], given_times=[99*365, 100*365, 102*365, 104*365]), axis=0)
# print(out)

data = pd.read_csv("./DataFolder/ResultFile/CostBenefit.csv")
df = data[data['intervene_measure'] == 4]["value"].values
plt.plot(df)
plt.show()