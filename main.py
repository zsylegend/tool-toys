import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
import matplotlib.pyplot as plt
device=torch.device("cuda" if torch.cuda.is_available() else "cpu")




class Net(torch.nn.Module):

    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=5, stride=1,padding=2),
            nn.Dropout(0.5),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=4),
            nn.Conv2d(32, 64, kernel_size=5, stride=1,padding=2),
            nn.Dropout(0.5),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Flatten(),
            nn.Linear(1600 , 1024),
            nn.ReLU(),
            nn.Linear(1024 , 512),
            nn.ReLU(),
            nn.Linear(512 , 64),
            nn.ReLU(),
            nn.Linear(64, 10),
            nn.LogSoftmax(dim=1),
        )

    def forward(self, x):
        return self.model(x)



def get_data_loader(is_train):
    to_tensor = transforms.Compose([transforms.ToTensor()])
    data_set = MNIST("", is_train, transform=to_tensor, download=True)
    return DataLoader(data_set, batch_size=15, shuffle=True,drop_last=True)


def evaluate(test_data, net):
    net.eval()
    n_correct = 0
    n_total = 0
    with torch.no_grad():
        for (x, y) in test_data:
            x=x.to(device)
            y=y.to(device)
            outputs = net.forward(x)
            for i, output in enumerate(outputs):
                if torch.argmax(output) == y[i]:
                    n_correct += 1
                n_total += 1
    net.train()
    return n_correct / n_total


def main():
    train_data = get_data_loader(is_train=True)
    test_data = get_data_loader(is_train=False)
    net = Net()
    net=net.to(device)

    print("initial accuracy:", evaluate(test_data, net))
    optimizer = torch.optim.Adam(net.parameters(), lr=0.001)
    for epoch in range(1):
        for (x, y) in train_data:
            x=x.to(device)
            y=y.to(device)
            net.zero_grad()
            output = net.forward(x)
            loss = torch.nn.functional.nll_loss(output, y)
            loss=loss.to(device)
            loss.backward()
            optimizer.step()
        print("epoch", epoch, "accuracy:", evaluate(test_data, net))
    torch.save(net, "./model1.pth")
    print("model saved")

    for (n, (x, _)) in enumerate(test_data):
        if n > 3:
            break
        input=x[0].to(device)
        predict = torch.argmax(net.forward(torch.reshape(input, (1,1,28,28))), dim=1)
        plt.figure(n)
        plt.imshow(x[0].view(28, 28))
        plt.title("prediction: " + str(int(predict)))
    plt.show()


if __name__ == "__main__":
    main()

