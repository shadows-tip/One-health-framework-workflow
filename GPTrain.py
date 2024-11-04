import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from Utils import get_dataset, save
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, r2_score


def gp_training(train_x, train_y):
    kernel = RBF(1.0) + WhiteKernel()
    gpr = GaussianProcessRegressor(kernel, n_restarts_optimizer=10, normalize_y=True)
    gpr.fit(train_x, train_y)
    return gpr


def cv_training(train_x, train_y, scene, meas):
    # 根据折数拆分训练集
    kf = KFold(n_splits=5, shuffle=True)

    cv_record = []
    for i, index in enumerate(kf.split(train_x)):
        train_index, test_index = index
        x_train, x_test = train_x[train_index], train_x[test_index]
        y_train, y_test = train_y[train_index], train_y[test_index]
        # 执行GP训练
        gpr = gp_training(x_train, y_train)
        cv_y_hat = gpr.predict(x_test)
        cv_score = gpr.score(x_test, y_test)
        cv_time_score = []
        for j in range(y_test.shape[1]):
            cv_time_score.append(r2_score(y_test[:, j].reshape(-1), cv_y_hat[:, j].reshape(-1)))
        cv_mae = mean_absolute_error(y_test, cv_y_hat)
        cv_record.append([i, cv_score, cv_mae]+cv_time_score)
    return np.array(cv_record)


def train_gp(train_x, train_y, test_x, test_y, scene, meas):
    gpr = gp_training(train_x, train_y)
    y_hat, std = gpr.predict(test_x, return_std=True)
    score = gpr.score(test_x, test_y)
    mae = mean_absolute_error(test_y, y_hat)
    print("{:s}, intervene_measures{:s} GP train....".format(scene, meas))
    print("GP predict score:", score)
    print("GP predict MAE:", mae)
    time_score = []
    for i in range(test_y.shape[1]):
        r2 = r2_score(test_y[:, i].reshape(-1), y_hat[:, i].reshape(-1))
        time_score.append(r2)
    # joblib.dump() function
    joblib.dump(gpr, './DataFolder/ModelFile2/' + scene + '/m' + str(meas) + '_GPmodel.pkl')
    save(y_hat, "./DataFolder/ResultFile2/" + scene + "/m" + str(meas) + "_GP_predict.csv")
    save(std, "./DataFolder/ResultFile2/" + scene + "/m" + str(meas) + "_GP_predict_std.csv")
    # set GP training ID as -1
    train_record = [-1, score, mae] + time_score
    return np.array(train_record).reshape(1, -1)


def parallel_module(parallel_item, cv_train=True):
    scene, meas = parallel_item

    # print("begin ....")
    train_path = './DataFolder/DatasetFile2/' + scene + '/meas' + str(meas) + '_' + scene + '_train_set.csv'
    test_path = './DataFolder/DatasetFile2/' + scene + '/meas' + str(meas) + '_' + scene + '_test_set.csv'
    train_x, train_y, test_x, test_y = get_dataset(train_path, test_path, len(meas))
    train_record = train_gp(train_x, train_y, test_x, test_y, scene, meas)
    # cross-validation
    if cv_train:
        cv_record = cv_training(train_x, train_y, scene, meas)
        train_record = np.concatenate((cv_record, train_record), axis=0)
        for i in range(len(cv_record)):
            print("{:s}, Meas{:s}, Cross validation[{:d}] score:{:f} MAE:{:f}".format(scene, meas, int(cv_record[i, 0]), cv_record[i, 1], cv_record[i, 2]))
    save(train_record, './DataFolder/ResultFile2/' + scene + '/m' + str(meas) + '_GP_cv_res.csv', ['ID', 'score', 'mae', '0th', '1th', '3th', '5th'])


if __name__ == '__main__':
    Scenes_names = ['Scene1', 'Scene2', 'Scene3', 'Scene4', 'Scene5', 'Scene6']
    Measures = ['1', '2', '3', '4', '12', '13', '14', '23', '24', '34', '123', '124', '134', '234', '1234']

    Parallel_tuple = [(Scene, Meas) for Scene in Scenes_names for Meas in Measures]
    task = [joblib.delayed(parallel_module)(item) for item in Parallel_tuple]
    worker = joblib.Parallel(n_jobs=-1, backend='multiprocessing')
    worker(task)
