import os
import time
import numpy as np
import pandas as pd
import torch
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
import xgboost
from sklearn.svm import SVR
from NeuralNetwork.DNNtrain import DNN
from Utils import get_dataset, save
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import KFold


def xgboost_training():
    print("Xgboost training ...")
    start = time.time()
    xgb = xgboost.XGBRegressor(learning_rate=0.1)
    xgb.fit(x_train, y_train)
    y_hat = xgb.predict(x_test)
    joblib.dump(xgb, "./DataFolder/ModelAnalysis2/ModelFile/xgb.pkl")
    save(y_hat, "./DataFolder/ModelAnalysis2/ResultFile/xgb_predict.csv")
    indicator = calcu_indicator(y_hat)
    print("xgboost RMSE:", indicator[0], "MAE:", indicator[1], "time:", time.time()-start, "r2:", indicator[2])
    return indicator


def random_forest_training():
    print("Random_Forest training ...")
    start = time.time()
    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(x_train, y_train)
    y_hat = rf.predict(x_test)
    joblib.dump(rf, "./DataFolder/ModelAnalysis2/ModelFile/rf.pkl")
    save(y_hat, "./DataFolder/ModelAnalysis2/ResultFile/rf_predict.csv")
    indicator = calcu_indicator(y_hat)
    print("random_forest RMSE:", indicator[0], "MAE:", indicator[1], "time:", time.time()-start, "r2:", indicator[2])
    return indicator


def svr_training():
    print("SVR training ...")
    start = time.time()
    y_hat = np.zeros_like(y_test)
    for i in range(y_train.shape[1]):
        svr_item = SVR(C=100)
        svr_item.fit(x_train, y_train[:, i])
        joblib.dump(svr_item, "./DataFolder/ModelAnalysis2/ModelFile/svr" + str(i) + ".pkl")
        y_hat[:, i] = svr_item.predict(x_test)
    save(y_hat, "./DataFolder/ModelAnalysis2/ResultFile/svr_predict.csv")
    indicator = calcu_indicator(y_hat)
    print("svr RMSE:", indicator[0], "MAE:", indicator[1], "time:", time.time()-start, "r2:", indicator[2])
    return indicator


def gp_training():
    print("GP training ...")
    start = time.time()
    kernel = RBF(1.0) + WhiteKernel()
    gpr = GaussianProcessRegressor(kernel, normalize_y=True)  # n_restarts_optimizer=5,
    gpr.fit(x_train, y_train)
    y_hat = gpr.predict(x_test)
    joblib.dump(gpr, "./DataFolder/ModelAnalysis2/ModelFile/gpr.pkl")
    save(y_hat, "./DataFolder/ModelAnalysis2/ResultFile/gpr_predict.csv")
    indicator = calcu_indicator(y_hat)
    print("GP RMSE:", indicator[0], "MAE:", indicator[1], "time:", time.time()-start, "r2:", indicator[2])
    return indicator


def dnn_training(num):
    print("DNN training ...")
    start = time.time()
    dnn = DNN(num)
    dnn.fit(x_train, y_train)
    y_hat = dnn.predict(x_test, y_test)
    torch.save(dnn.model.state_dict(), "./DataFolder/ModelAnalysis2/ModelFile/dnn.pkl")
    save(y_hat, "./DataFolder/ModelAnalysis2/ResultFile/dnn_predict.csv")
    indicator = calcu_indicator(y_hat)
    print("DNN RMSE:", indicator[0], "MAE:", indicator[1], "time:", time.time()-start, "r2:", indicator[2])
    return indicator


def cv_training(train_x, train_y, func):
    # training sets
    kf = KFold(n_splits=5, shuffle=True)
    cv_record = []
    for i, index in enumerate(kf.split(train_x)):
        train_index, test_index = index
        x_train_cv, x_test_cv = train_x[train_index], train_x[test_index]
        y_train_cv, y_test_cv = train_y[train_index], train_y[test_index]
        # GP training
        gpr = func(x_train_cv, y_train_cv)
        cv_y_hat = gpr.predict(x_test)
        cv_score = gpr.score(x_test, y_test)
        cv_mae = mean_absolute_error(y_test, cv_y_hat)
        cv_record.append([i, cv_score, cv_mae])
    return np.array(cv_record)


def diso(model_metrics):
    metrics_res = model_metrics.copy()
    # normalization, MAE, RMSE, r2
    for i in range(metrics_res.shape[1] - 1):
        p = max((np.max(metrics_res[:, i]) - np.min(metrics_res[:, i])), abs(np.max(metrics_res[:, i])),
                abs(np.min(metrics_res[:, i])))
        metrics_res[:, i] = (metrics_res[:, i] / p) ** 2
    metrics_res[:, -1] = (metrics_res[:, -1] - 1) ** 2
    return np.sqrt(np.sum(metrics_res, axis=1))


def calcu_indicator(y_hat):
    RMSE = np.sqrt(mean_squared_error(y_test, y_hat))
    MAE = mean_absolute_error(y_test, y_hat)
    r2 = r2_score(y_test[:, 1:], y_hat[:, 1:])
    return np.array([RMSE, MAE, r2]).reshape(-1)


def model_testing(measure):
    model_indicator = np.zeros((5, 3))
    model_indicator[0] = xgboost_training()
    model_indicator[1] = random_forest_training()
    model_indicator[2] = svr_training()
    model_indicator[3] = gp_training()
    model_indicator[4] = dnn_training(num=len(str(measure)))

    metrics_diso = diso(model_indicator)
    model_indicator = np.concatenate(
        (model_indicator, metrics_diso.reshape(-1, 1), np.full((len(model_indicator), 1), measure)), axis=1)

    model_indicator = pd.DataFrame(model_indicator, index=["xgboost", "random_forest", "svr", "gp", "DNN"],
                                   columns=["RMSE", "MAE", "r2", "diso", "meas"])
    print(model_indicator)
    model_indicator.to_csv("./DataFolder/ModelAnalysis2/ResultFile/model_indicator_meas" + str(measure) + ".csv")


Measures = [34]
for meas in Measures:
    train_path = "./DataFolder/DatasetFile2/Scene1/meas" + str(meas) + "_Scene1_train_set.csv"
    test_path = "./DataFolder/DatasetFile2/Scene1/meas" + str(meas) + "_Scene1_test_set.csv"
    x_train, y_train, x_test, y_test = get_dataset(train_path, test_path, meas_num=len(str(meas)))

    model_testing(meas)
    # dnn_training(len(str(meas)))
