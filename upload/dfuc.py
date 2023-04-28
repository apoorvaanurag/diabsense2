import torch
import torchvision
from torch.utils.data.dataloader import DataLoader
from torchvision import datasets, models, transforms
from PIL import Image
from vit_pytorch import SimpleViT

base_vit = SimpleViT(
    image_size = 224,
    patch_size = 16,
    num_classes = 2,
    dim = 1024,
    depth = 6,
    heads = 14,
    mlp_dim = 2048
)

torch.manual_seed(42)
torch.cuda.manual_seed(42)

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
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

# Test Section
def dfuc(img_name):
    # concatenate img_name to the path
    img_path = img_name

    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        RemoveAlphaChannel(),
    ])

    dataset = ImageDataset(img_path, transform=transform)
    test_dl = DataLoader(dataset, batch_size=1, shuffle=False, pin_memory=True)

    # Store predicted values
    # 0 - both
    # 1 - infection
    # 2 - ischaemia
    # 3 - none
    predicted_vals = [0] * 4

    # MODEL 1
    # model = torch.jit.load('model1.pt') # Load
    model = torch.jit.load("upload/model1.pt", map_location=torch.device('cpu')) # Load
    model = model.to(device)
    was_training = model.training
    model.eval()

    with torch.no_grad():
        for i, (inputs) in enumerate(test_dl):
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            sm = torch.nn.Softmax(dim=1)
            probabilities = sm(outputs)

            for j in range(inputs.size()[0]):
                none = probabilities[j][0].item()

        model.train(mode=was_training)

    # MODEL 2
    model = base_vit
    model.load_state_dict(torch.load('upload/model2.pt', map_location=torch.device('cpu')))
    model = model.to(device)
    was_training = model.training
    model.eval()

    # Find a good threshold
    threshold = 20
    # Convert the threshold to a percentage because the probabilities are between 0 and 1
    threshold = threshold * 0.01

    with torch.no_grad():
        for i, (inputs) in enumerate(test_dl):
            inputs = inputs.to(device)
            # labels = labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            sm = torch.nn.Softmax(dim=1)
            probabilities = sm(outputs)

            for j in range(inputs.size()[0]):
                # Remaining Probability
                rp = 1 - none
                both_prob = 0
                infection_prob = probabilities[j][0].item()
                ischaemia_prob = probabilities[j][1].item()
                # If the probabilities are close, then we can assume that the image is both
                # Probability of both can be calculated by taking the average of the two probabilities
                # and the probabilities of infection and ischaemia can be halved
                if abs(infection_prob - ischaemia_prob) <= threshold and False:
                    both_prob = (infection_prob + ischaemia_prob) / 2
                    # Double down on the image being of type 'both'
                    # both_prob = 1
                    infection_prob = infection_prob / 2
                    ischaemia_prob = ischaemia_prob / 2
                both_prob = both_prob * rp
                both = both_prob
                corrected_probability = infection_prob * rp
                infection = corrected_probability
                corrected_probability = ischaemia_prob * rp
                ischaemia = corrected_probability

        model.train(mode=was_training)

    predicted_vals[0] = both
    predicted_vals[1] = infection
    predicted_vals[2] = ischaemia
    predicted_vals[3] = none

    print(predicted_vals)

    return predicted_vals

