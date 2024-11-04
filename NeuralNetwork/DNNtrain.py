import torch
import time
from NeuralNetwork.Earlystopping import EarlyStopping
from torch.optim import lr_scheduler
from NeuralNetwork.DNNmodel import DNNmodel
from NeuralNetwork.Tool import calc_error, data_processing, data_normalized
from sklearn.model_selection import train_test_split
import os

os.getcwd()


class DNN:
    def __init__(self, num):
        self.criterion = torch.nn.MSELoss()
        self.early_stopping = EarlyStopping(patience=12, verbose=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.criterion.to(self.device)

        self.lr = 0.05
        self.epochs = 100
        self.model = DNNmodel(num)
        self.model.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        self.scheduler = lr_scheduler.ReduceLROnPlateau(self.optimizer, factor=0.3, patience=3, verbose=False)
        # self.scheduler = lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=150, eta_min=0)

    def fit(self, train_x, train_y):

        data_normalized(train_x, train_y)
        train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size=0.2, random_state=10)
        train_loader = data_processing(train_x, train_y, data_type='train')
        val_loader = data_processing(val_x, val_y, data_type='val')

        train_loss_record = []
        val_loss_record = []

        for epoch in range(self.epochs):
            epoch_start = time.time()

            # print("Epoch {}/{}:".format(epoch + 1, self.epochs))
            self.model.train()
            train_loss = self.train(train_loader)
            val_loss = self.evaluate(val_loader)
            train_loss_record.append(train_loss)
            val_loss_record.append(val_loss)

            self.scheduler.step(val_loss)  # 学习率衰减
            self.early_stopping(val_loss, self.model)  # 早停

            if self.early_stopping.early_stop:
                # print("Early stopping")
                break
            # print(">train loss:{:f}, val loss:{:f}, epoch time:{:f}".format(train_loss, val_loss,
            #                                                                 time.time() - epoch_start))
        self.model.load_state_dict(torch.load('checkpoint.pkl'))

    def train(self, train_loader):
        train_loss = 0.0
        for i, data in enumerate(train_loader):
            inputs, labels = data
            inputs, labels = inputs.to(self.device), labels.to(self.device)
            # 前向传播
            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)
            # 反向传播
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            train_loss += loss.item()
            if (i + 1) % 100 == 0:
                print("Step[{}/{}] train Loss:{:f} Lr:{:f}".format(i + 1, len(train_loader), train_loss / (i + 1),
                                                                   self.optimizer.param_groups[0]["lr"]))
        return train_loss / len(train_loader)

    def evaluate(self, val_loader):
        self.model.eval()
        with torch.no_grad():
            val_loss = 0.0
            for i, data in enumerate(val_loader):
                inputs, labels = data
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                val_loss += loss.item()
            return val_loss / len(val_loader)

    def predict(self, test_x, test_y):
        test_tensor = data_processing(test_x, test_y, data_type='test')
        self.model.eval()
        with torch.no_grad():
            test_x, test_y = test_tensor
            inputs, labels = test_x.to(self.device), test_y.to(self.device)
            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)

            outputs = outputs.cpu().clone().detach().numpy()
            y_hat = calc_error(outputs, labels)

            # loss / len(outputs)
            return y_hat
