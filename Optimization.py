import numpy as np
import pandas as pd
import joblib
from scipy.optimize import minimize
from Utils import save
import warnings

# warnings.filterwarnings("ignore")
record = []


def func(cov, *args):
    gpr, meas, object_value, year = args
    output = gpr.predict([cov], return_std=False)
    diff = output[0, year] - object_value
    global record
    record.append(-1 if diff < 0 else 1)
    return np.abs(diff)


def optim(*args):
    # gpr, eff, object_value, year
    best_x, best_res = np.nan, 1
    for j in range(120):  # 80
        x0 = np.random.uniform(0, 1)
        result = minimize(func, x0, method='SLSQP', bounds=[[0, 1]], args=args)
        if result.fun < best_res:
            best_res = result.fun
            best_x = result.x[0]
        # print("第{:d}次优化, 优化状态:{:s}, 最优值:{:f}, 最优解:{:f}".format(j, str(res.success), result.x[0], result.fun))
    global record
    if record.count(-1) > record.count(1) and np.isnan(best_x):
        best_x = 0
    print("the optimization value of this time is:{:f}".format(best_x))
    record.clear()
    return best_x


def optim_running(meas, scene, objects: list, year: int):
    gpr_path = './DataFolder/ModelFile2/Scene' + str(scene) + '/m' + str(meas) + '_GPmodel.pkl'
    gpr_model = joblib.load(gpr_path)
    out = []
    time_list = {"1": 1, "2": 3, "3": 5}
    for i, object_value in enumerate(objects):
        print("meas{:d}, scene{:d}, object:{:.2f}, year:{:d}".format(meas, scene, object_value, time_list[str(year)]))
        optim_res = optim(gpr_model, meas, object_value, year)
        out.append([meas, scene, object_value, optim_res, time_list[str(year)]])
    return out


Scenes = [i for i in range(1, 7)]
times = [1, 2, 3]  # the first, third, and fifth year
Meas = [1, 2, 3, 4, 12, 13, 14, 23, 24, 34, 123, 124, 134, 234, 1234]

# set health goals
Objects = [500, 1000, 1500, 2000, 2500]
Out = []
# four cycles
for item, M in enumerate(Meas):
    for t, time in enumerate(times):
        for s, Scene in enumerate(Scenes):
            res = optim_running(M, Scene, Objects, time)
            Out.extend(res)

save(Out, './DataFolder/ResultFile2/Optim241014_1234(cases).csv',
     columns=['interv_measure', 'scene', 'object_value', 'min_coverage', 'year'])
