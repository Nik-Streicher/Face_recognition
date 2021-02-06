import os

from torch.utils.data import DataLoader
from torchvision import datasets
from tqdm import tqdm

from .User import User


class Loader:

    # initializes dataset path
    def __init__(self, dataset_path):

        self.workers = 0 if os.name == 'nt' else 4
        self.dataset = datasets.ImageFolder(dataset_path)

    # loads dataset and return as list of User()
    def load(self, mtcnn, resnet, users):

        def collate_fn(val):
            return val[0]

        self.dataset.idx_to_class = {i: c for c, i in self.dataset.class_to_idx.items()}
        loader = DataLoader(self.dataset, collate_fn=collate_fn, num_workers=self.workers)

        for x, y in tqdm(loader, desc="Loading dataset", position=0):
            x_aligned = mtcnn(x)

            # if a face is detected makes user embedding
            if x_aligned is not None:
                users.append(User(self.dataset.idx_to_class[y], resnet(x_aligned), "Allowed"))

        return users
