import math

import torch
from torch import nn
from math import pi

import numpy as np

class CosFace(nn.Module):
    def __init__(self, s=64.0, m=0.40):
        super(CosFace, self).__init__()
        self.s = s
        self.m = m

    def forward(self, cosine, label):
        index = torch.where(label != -1)[0]
        m_hot = torch.zeros(index.size()[0], cosine.size()[1], device=cosine.device)
        m_hot.scatter_(1, label[index, None], self.m)
        cosine[index] -= m_hot
        ret = cosine * self.s
        return ret

class Softmax(nn.Module):
    def __init__(self, s=64.0, m=0.40):
        super(Softmax, self).__init__()
        self.s = s
        self.m = m
    def forward(self, cosine, label):
        ret = cosine * self.s
        return ret
class ArcFace(nn.Module):
    def __init__(self, s=64.0, m=0.5):
        super(ArcFace, self).__init__()
        self.s = s
        self.m = m

    def forward(self, cosine: torch.Tensor, label):
        index = torch.where(label != -1)[0]
        m_hot = torch.zeros(index.size()[0], cosine.size()[1], device=cosine.device)
        m_hot.scatter_(1, label[index, None], self.m)
        cosine.acos_()
        cosine[index] += m_hot
        cosine.cos_().mul_(self.s)
        return cosine


class CombineLoss(nn.Module):
    def __init__(self, s=64.0, m=1.0):  #m2 Arcface, m3CosineFace
        super(CombineLoss, self).__init__()
        self.s = s

        self.m1 = m
        self.m2 = 0.3
        self.m3 = 0.2
    def forward(self, cosine: torch.Tensor, label):
        index = torch.where(label != -1)[0]
        m_hot = torch.zeros(index.size()[0], cosine.size()[1], device=cosine.device)
        m_hot.scatter_(1, label[index, None], self.m2)
        m_hot3 = torch.zeros(index.size()[0], cosine.size()[1], device=cosine.device)
        m_hot3.scatter_(1, label[index, None], self.m3)
        cosine.acos_()
        cosine[index] += m_hot
        cosine.cos_()
        cosine[index] -= m_hot3
        cosine.mul_(self.s)
        return cosine

