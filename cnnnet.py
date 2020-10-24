import torch
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# 批处理数
BATCHSIZE = 512
# 训练总批次
EPOCHS = 20
# 是否使用GPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


transform = transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ])
train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data/MNIST', train=True, download=True, transform=transform),
    batch_size=BATCHSIZE, shuffle=True
)
test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data/MNIST', train=False, download=True, transform=transform),
    batch_size=BATCHSIZE, shuffle=True
)


class ConvNet(nn.Module):
    def __init__(self):
        super().__init__()
        # batch*1*28*28（每次会送入batch个样本，输入通道数1（黑白图像），图像分辨率是28x28）
        # 下面的卷积层Conv2d的第一个参数指输入通道数，第二个参数指输出通道数，第三个参数指卷积核的大小
        self.conv1 = nn.Conv2d(1, 10, 5)  # 输入通道数1，输出通道数10，核的大小5
        self.conv2 = nn.Conv2d(10, 20, 3)  # 输入通道数10，输出通道数20，核的大小3
        # 下面的全连接层Linear的第一个参数指输入通道数，第二个参数指输出通道数
        self.fc1 = nn.Linear(20*10*10, 500)  # 输入通道数是2000，输出通道数是500
        self.fc2 = nn.Linear(500, 10)  # 输入通道数是500，输出通道数是10，即10分类

    # 定义向前操作方法，即整个模型流程
    def forward(self, x):
        in_size = x.size(0)  # 在本例中in_size=512，也就是BATCH_SIZE的值。输入的x可以看成是512*1*28*28的张量。
        out = self.conv1(x)  # batch*1*28*28 -> batch*10*24*24（28x28的图像经过一次核为5x5的卷积，输出变为24x24）
        out = F.relu(out)  # batch*10*24*24（激活函数ReLU不改变形状））
        out = F.max_pool2d(out, 2, 2)  # batch*10*24*24 -> batch*10*12*12（2*2的池化层会减半）
        out = self.conv2(out)  # batch*10*12*12 -> batch*20*10*10（再卷积一次，核的大小是3）
        out = F.relu(out)  # batch*20*10*10
        out = out.view(in_size, -1)  # batch*20*10*10 -> batch*2000（out的第二维是-1，说明是自动推算，本例中第二维是20*10*10）
        out = self.fc1(out)  # batch*2000 -> batch*500
        out = F.relu(out)  # batch*500
        out = self.fc2(out)  # batch*500 -> batch*10
        out = F.log_softmax(out, dim=1)  # 计算log(softmax(x))
        return out


model = ConvNet().to(DEVICE)
# 定义一个Adam算法的优化器
optimizer = optim.Adam(model.parameters())


def train(model, device, train_loader, optimizer, epoch):
    # Module类的train方法·将模块设置为训练模式。
    model.train()
    # 调用enumerate遍历train_loader中每个数据，获取对应的批处理索引，数据和目标，即index，x和y
    for batch_idx, (data, target) in enumerate(train_loader):
        # 将对应的数据加载到GPU
        data, target = data.to(device), target.to(device)
        # 将优化器的梯度清零
        optimizer.zero_grad()
        # 将数据传入模型
        output = model(data)
        # 以负对数似然损失函数作为损失函数
        loss = F.nll_loss(output, target)
        # 对损失1函数反馈
        loss.backward()
        # 更新网络参数
        optimizer.step()
        # 每一30个数据打印
        if(batch_idx+1) % 30 == 0:
            print('训练批次为：{} [{}/{} ({:.0f}%)]\t损失值为：{:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))


def test(model, device, test_loader):
    # 将模块设置为评估模式，即测试模式
    model.eval()
    test_loss = 0
    correct = 0
    # 让下面的Tensor反向传播不会求导，因为test模式下没必要去反馈，所以也不会更新参数
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            # reduction指定要应用于输出的缩减，为和的模式
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # 将一批的损失相加
            pred = output.max(1, keepdim=True)[1]  # 找到概率最大的下标
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    print('\n测试集：平均损失为：{:.4f}，精确度为：{}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


if __name__ == '__main__':
    # 循环训练与测试
    for epoch in range(1, EPOCHS + 1):
        train(model, DEVICE, train_loader, optimizer, epoch)
        test(model, DEVICE, test_loader)
