import numpy as np
import pandas as pd
import joblib
import matplotlib
from plotnine import *
from matplotlib import pyplot as plt
from ModelPackage.SimulationModel import Model

Nh = 5.81e4

# Ih values in the stationary state in 6 scenarios
Ih_list = [1904, 4095, 7405, 8876, 13915, 19085]
mu_h = 1.49e-5
mu_d = 2.10e-7
gamma1 = 0.137 / 365

# Calculate the cost of scenario 2, intervention for 3 years
def calcu_cost(measure, measure_param, scene=0, time=50):
    cost = 0
    measure = str(measure)
    # intervention 1： cost = total number of fish (1.17e7) * coverage * Vaccine costs（0.2/fish） * years
    if measure == '1':
        cost = 1.17e7 * measure_param[0] * 0.2 * time
    # intervention 2：cost = total number of infected people * coverage * Cost of chemotherapy per person (681.58) * years
    elif measure == '2':
        cost = Ih_list[scene] * measure_param[0] * 681.58 * time
    # intervention 3：cost = total number of people * coverage * cost of IEC per person (8.23) * years
    elif measure == '3':
        cost = Nh * measure_param[0] * 8.23 * time
    # intervention 4：cost = total number of sanitation toilets (1.349e7) * coverage * [The unit price of the toilet demolition and construction cost (719.94+3324.58=4043.98)+Toilet maintenance costs per unit (652.65) * years]
    elif measure == '4':
        cost = 1.349e7 * measure_param[0] * 4043.98
        # cost = 1.349e7 * measure_param[0] * (4043.98 + 652.65 * time)
    return cost


def calcu_rate(measure, measure_param):
    cost = calcu_cost(measure, measure_param)
    # out = np.squeeze(model.predict(measure_param))
    model = Model(t=150, ratio=0.34)
    model.set_param(intervene_meas=measure, intervene_time=100, intervene_param=measure_param)
    out = np.sum(model.get_result(label=['Ih1', 'Ih2', 'Ih3', 'Ih4'], given_times=[99*365, 102*365]), axis=0)
    # print(out):YLD + YLL (GBD2021 DW = 0.114339967；Life expectancy in 2015: 76.34-The mean age of death in patients with cholangiocarcinoma: 62.6)
    diff = (out[0] - out[1]) * (1 / (mu_h + mu_d + gamma1)) * 0.114339967 + (out[0] - out[1]) * 2.10e-7 * (76.34 - 62.6)

    # print(diff, cost)
    return cost / diff

plt.figure(figsize=(8, 5))
config = {
    "font.family": "serif",
    "font.serif": ["Arial"],
    "font.size": 14,
    "axes.unicode_minus": False  # 处理负号，即-号
}
matplotlib.rcParams.update(config)
Meas = [1, 2, 3, 4]
titles = ["Fish vaccination", "Chemotherapy", "IEC", "Sanitation toilets"]
cov = np.linspace(0.01, 1, 100)
eff = [0.99, 0.92, 0.5408, 1]
recorder = []
linestyles = ['-', '-.', ':', '--']
for i in range(len(Meas)):
    param = list(map(lambda x: [x, eff[i]], cov))
    # path = "./DataFolder/ModelFile/Scene2/m" + str(Meas[i]) + "_GPmodel.pkl"
    # gpr = joblib.load(path)
    recorder_item = []
    for j in param:
        recorder_item.append(calcu_rate(Meas[i], j))
        recorder.append(calcu_rate(Meas[i], j))
    plt.plot(cov, recorder_item, label=titles[i], color='black', linestyle=linestyles[i])
    # print(cov[np.argmax(np.array(recorder_item))], recorder_item[np.argmax(np.array(recorder_item))])

    # recorder.append(recorder_item)
# print(recorder)
data = {
    "intervene_measure": np.concatenate((np.ones((len(cov),)), np.full((len(cov),), 2), np.full((len(cov),), 3), np.full((len(cov),), 4)), axis=0),
    "cov": np.concatenate((cov.reshape(-1), cov.reshape(-1), cov.reshape(-1), cov.reshape(-1)), axis=0),
    "value": recorder
}
print(data)
data = pd.DataFrame(data)
# plot_curve(data)
data.to_csv("./DataFolder/ResultFile/ICER.csv", index=False)
plt.xlabel("Coverage")
plt.ylabel("Incremental cost-effectiveness ratio (ICER)")
plt.xlim(0, 1)

plt.legend()
plt.savefig("./DataFolder/FigureFile/Cost.png")
plt.show()
