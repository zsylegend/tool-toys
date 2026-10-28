import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from main import Net
import PIL.Image as Image
import torchvision.transforms as transforms
net=torch.load("./model.pth",weights_only=False)

img1=Image.open("./img1.png")
img2=Image.open("./img2.png")
img3=Image.open("./img3.png")
img=[img1,img2,img3]
transform=transforms.Compose([transforms.Resize((28,28)),transforms.Grayscale(1),transforms.ToTensor()])
timg1=transform(img1)
timg2=transform(img2)
timg3=transform(img3)
timg1=torch.reshape(timg1,(1,1,28,28))
timg2=torch.reshape(timg2,(1,1,28,28))
timg3=torch.reshape(timg3,(1,1,28,28))
timg1=timg1.cuda()
timg2=timg2.cuda()
timg3=timg3.cuda()

net.eval()

output1=net.forward(timg1.cuda())
output2=net.forward(timg2.cuda())
output3=net.forward(timg3.cuda())

predict1=torch.argmax(output1)
predict2=torch.argmax(output2)
predict3=torch.argmax(output3)
prediction=[predict1,predict2,predict3]
for n in range(0,3):
    plt.figure(n)
    plt.imshow(img[n])
    plt.title("prediction: " + str(int(prediction[n])))
plt.show()
print('预测img1:',str(int(predict1)),'预测img2:',str(int(predict2)),'预测img3:',str(int(predict3)))
