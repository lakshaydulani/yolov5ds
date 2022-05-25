import torch
import torchvision.transforms as transforms
import numpy as np
import torch.nn as nn
import cv2
import logging
import glob
# from torchsummary import summary


from .model import Net

def _cosine_distance(a, b, data_is_normalized=False):
    if not data_is_normalized:
        a = np.asarray(a) / np.linalg.norm(a, axis=1, keepdims=True)
        b = np.asarray(b) / np.linalg.norm(b, axis=1, keepdims=True)
    return (1000 * (1. - np.dot(a, b.T)))

class Extractor(object):
    def __init__(self, model_path, use_cuda=True):
        self.net = Net(reid=True)
        self.device = "cuda" if torch.cuda.is_available() and use_cuda else "cpu"
        state_dict = torch.load(model_path, map_location=torch.device(self.device))[
            'net_dict']
        self.net.load_state_dict(state_dict)

        self.net.to(self.device)
        self.size = (64, 128)
        self.norm = transforms.Compose([
            transforms.ToTensor(),
            # transforms.Lambda(lambda x: x.repeat(3, 1, 1)),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])

    def _preprocess(self, im_crops):
        """
        TODO:
            1. to float with scale from 0 to 1
            2. resize to (64, 128) as Market1501 dataset did
            3. concatenate to a numpy array
            3. to torch Tensor
            4. normalize
        """
        def _resize(im, size):
            return cv2.resize(im.astype(np.float32)/255., size)

        im_batch = torch.cat([self.norm(_resize(im, self.size)).unsqueeze(
            0) for im in im_crops], dim=0).float()
        return im_batch

    def __call__(self, im_crops):
        im_batch = self._preprocess(im_crops)
        with torch.no_grad():
            im_batch = im_batch.to(self.device)
            features = self.net(im_batch)
        return features.cpu().numpy()


if __name__ == '__main__':

    extr = Extractor("./deep_sort_pytorch/deep_sort/deep/checkpoint/ckpt.t7")
    summary(extr.net,(3,128,64))
    
    # list = glob.glob("mars/*.jpg")
    # features_list = []

    # for i in list:
    #     im = cv2.imread(i)
    #     im_crops = [im]
    #     features = extr(im_crops)
    #     features_list.append(features)
    #     print(_cosine_distance(features, features_list[0]),"<< " + i)
