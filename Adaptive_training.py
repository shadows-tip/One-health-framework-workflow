import numpy as np
import pandas as pd
import joblib
from DataGenerator2 import parallel_module
from joblib import Parallel, delayed
from Utils import lhs_sampling, get_data_column, save, get_dataset
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error
# from Plot import plot_scatter_boxplot
from sklearn.metrics import r2_score

if __name__ == '__main__':

    T = 120  # time span
    Intervene_time = 100  # intervene time (year)
    Scenes = {'Scene1': [0.6683, 0.1792, 0.1025, 0.05]}
    Measures = [12, 13, 14, 23, 24, 123, 124, 234, 1234]  # intervention measures
    for Scene_key in Scenes:
        for measure in Measures:

            Intervene_measure = measure  # intervention measures
            Scene = Scenes[Scene_key]
            Parallel_tuple = [(Scene_key, Scene, Measure) for Scene_key, Scene in Scenes.items() for Measure in
                              Measures]
            Task = [delayed(parallel_module)(T, Intervene_time, parallel_item, True) for parallel_item in Parallel_tuple]
            Worker = Parallel(n_jobs=30, backend='multiprocessing')
            Worker(Task)
            print("Finish Dataset prepared!")

            model_path = './DataFolder/ModelFile/' + Scene_key + '/m' + str(measure) + '_GPmodel.pkl'
            train_path = './DataFolder/DatasetFile/' + Scene_key + '/meas' + str(
                measure) + '_' + Scene_key + '_adaptive_train_set.csv'
            test_path = './DataFolder/DatasetFile/' + Scene_key + '/meas' + str(
                measure) + '_' + Scene_key + '_test_set.csv'
            train_x, train_y, test_x, test_y = get_dataset(train_path, test_path, len(str(measure)))

            gpr = joblib.load(model_path)
            y_hat, std = gpr.predict(test_x, return_std=True)
            score = gpr.score(test_x, test_y)
            mae = mean_absolute_error(test_y, y_hat)
            print("{:s}, intervene_measures{:d} GP train....".format(Scene_key, measure))
            print("GP predict score:", score)
            print("GP predict MAE:", mae)

            gpr.fit(train_x, train_y)
            # gpr = joblib.load("./DataFolder/Adaptive_training/Model/Scene2/m123_GPmodel.pkl")
            y_hat, std = gpr.predict(test_x, return_std=True)
            score = gpr.score(test_x, test_y)
            mae = mean_absolute_error(test_y, y_hat)
            print("{:s}, intervene_measures{:d} GP train....".format(Scene_key, measure))
            print("GP predict score:", score)
            print("GP predict MAE:", mae)

            # # joblib.dump()函数保存模型
            joblib.dump(gpr, './DataFolder/Adaptive_training/Model/' + Scene_key + '/m' + str(measure) + '_GPmodel.pkl')
            save(y_hat, "./DataFolder/Adaptive_training/Result/" + Scene_key + "/m" + str(measure) + "_GP_predict.csv")
            save(std,
                 "./DataFolder/Adaptive_training/Result/" + Scene_key + "/m" + str(measure) + "_GP_predict_std.csv")

            # m = str(measure)
            # true_data = test_y
            # pred_data = y_hat[:, [0, 2, 3]]
            # cv_score = pd.read_csv("DataFolder/ResultFile/Scene2/m" + m + "_GP_cv_res.csv").values[:, 1]
            # time_score = []
            # true_data = true_data[:, [0, 2, 3]]
            # for i in range(3):
            #     r2 = r2_score(true_data[:, i].reshape(-1), pred_data[:, i].reshape(-1))
            #     time_score.append(r2)
            #
            # plot_scatter_boxplot(true_data, pred_data, cv_score, time_score, m)
