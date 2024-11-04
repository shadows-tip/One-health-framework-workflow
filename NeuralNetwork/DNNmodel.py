from torch import nn


class DNNmodel(nn.Module):
    def __init__(self, num):
        super(DNNmodel, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(1, 256, kernel_size=1),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True)
        )
        self.fc1 = nn.Sequential(
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True)
        )
        self.fc2 = nn.Sequential(
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True)
        )
        self.fc3 = nn.Sequential(
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(inplace=True)
        )
        self.fc4 = nn.Sequential(
            nn.Linear(32, 16),
            nn.BatchNorm1d(16),
            nn.ReLU(inplace=True)
        )
        self.final = nn.Sequential(
            nn.Linear(16, 4),
        )

    def forward(self, x):
        out = self.conv(x)
        out = out.view(x.size(0), -1)
        out = self.fc1(out)
        out = self.fc2(out)
        out = self.fc3(out)
        out = self.fc4(out)
        out = self.final(out)

        return out
