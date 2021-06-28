import argparse
import logging
import os

import cv2
import numpy as np
import sys
import mxnet as mx
import datetime
from skimage import transform as trans
import sklearn
from sklearn import preprocessing
import torch
from torchvision import transforms

import backbones.mixnetm as mx
from  sklearn.metrics.pairwise import cosine_similarity

from utils.utils_callbacks import CallBackVerification
from utils.utils_logging import init_logging

sys.path.append('/root/xy/work_dir/xyface/')
from torch.nn.parallel import DistributedDataParallel
from config import config as cfg



if __name__ == "__main__":

    backbone = mx.mixnet_s(embedding_size=cfg.embedding_size, width_scale=cfg.scale, gdw_size=cfg.gdw_size).to("cpu")
    backbone.load_state_dict(torch.load(os.path.join('147836backbone.pth'),map_location=torch.device('cpu')))
    model = torch.nn.DataParallel(backbone)
    print(model)
    exit()
    log_root = logging.getLogger()

    init_logging(log_root, 0, cfg.output,logfile="test.log")
    callback_verification = CallBackVerification(11372, 0, cfg.val_targets, cfg.rec)
    output_folder='/home/fboutros/arcface_torch/output/emore_combine_mixcon_s_0.5' #emore_cosface_mixcon_s_1.0_gdw_1024 net_size_scale_gdw
    weights=os.listdir(output_folder)

    for w in weights:
        if "backbone" in w:

         if (cfg.net_size == "s"):
             backbone = mx.mixnet_s(embedding_size=cfg.embedding_size, width_scale=cfg.scale, gdw_size=cfg.gdw_size).to( "cuda:0")
         else:
            backbone = mx.mixnet_m(embedding_size=cfg.embedding_size, width_scale=cfg.scale, gdw_size=cfg.gdw_size).to( "cuda:0")

         backbone.load_state_dict(torch.load(os.path.join(output_folder,w)))
         model = torch.nn.DataParallel(backbone)
         callback_verification(int(w.split("backbone")[0]),model)

