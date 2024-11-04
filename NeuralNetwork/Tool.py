import numpy as np
import torch
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import os

os.getcwd()

scaler1 = MinMaxScaler()
scaler2 = MinMaxScaler()


def data_normalized(data_x, data_y):
    global scaler1
    scaler1.fit(data_x)
    global scaler2
    scaler2.fit(data_y)


def data_processing(data_x, data_y, data_type='train'):
    data_x = scaler1.transform(data_x)
    data_y = scaler2.transform(data_y)
    data_x = data_x.reshape(len(data_x), 1, -1)
    if data_type == 'test':
        data_loader = torch.tensor(data_x, dtype=torch.float32), torch.tensor(data_y, dtype=torch.float32)
    else:
        data_loader = DataLoader(
            TensorDataset(torch.tensor(data_x, dtype=torch.float32), torch.tensor(data_y, dtype=torch.float32)),
            batch_size=64, shuffle=True)
    return data_loader


def calc_error(y_hat, y_true):
    y_hat = scaler2.inverse_transform(y_hat)
    y_true = scaler2.inverse_transform(y_true)

    y_hat_tensor = torch.tensor(y_hat, dtype=torch.float32)
    y_true_tensor = torch.tensor(y_true, dtype=torch.float32)

    criterion = torch.nn.MSELoss()
    # print('MSELoss', criterion(y_hat_tensor, y_true_tensor))
    mse = mean_squared_error(y_true, y_hat)
    mae = mean_absolute_error(y_true, y_hat)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_hat)
    indicator = [mse, rmse, mae, r2]

    return y_hat
