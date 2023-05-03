import torch
import torchvision
from torch.utils.data.dataloader import DataLoader
from torchvision import datasets, models, transforms
from PIL import Image

torch.manual_seed(42)
torch.cuda.manual_seed(42)

device = torch.device("cpu")

class ImageDataset(torch.utils.data.Dataset):
    def __init__(self, img_path, transform=None):
        self.img_path = img_path
        self.transform = transform

    def __getitem__(self, index):
        img = Image.open(self.img_path)
        if self.transform:
            img = self.transform(img)
        return img

    def __len__(self):
        return 1

# Needed for PNG images
class RemoveAlphaChannel(object):
    def __call__(self, img):
        return img[:3, :, :]

def footValid(img_name):
    # concatenate img_name to the path
    img_path = img_name
    # img_path = 'C:/Users/apoor/Desktop/dfu.jpg'

    transform = transforms.Compose([
        transforms.Resize((32,32)),
        transforms.ToTensor(),
        RemoveAlphaChannel(),
    ])

    dataset = ImageDataset(img_path, transform=transform)
    print(dataset[0].shape)
    test_dl = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=1, pin_memory=True)

    # MODEL 1
    model = torch.jit.load("upload/validate.pt", map_location=torch.device('cpu')) # Load
    model = model.to(device)
    was_training = model.training
    model.eval()

    with torch.no_grad():
        other = []
        dfu = []
        for i, (inputs) in enumerate(test_dl):
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            sm = torch.nn.Softmax(dim=1)
            probabilities = sm(outputs)

            for j in range(inputs.size()[0]):
                other.append(probabilities[j][0].item())
                dfu.append(probabilities[j][1].item())

        model.train(mode=was_training)

    print(f'other: {other[0]}')
    print(f'dfu: {dfu[0]}')

    return dfu[0] > 0.40
