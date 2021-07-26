from easydict import EasyDict as edict

config = edict()
config.dataset = "emore"
config.embedding_size = 512
config.sample_rate = 1
config.fp16 = False
config.momentum = 0.9
config.weight_decay = 5e-4
config.weight_decay_last = 5e-3

config.batch_size = 128
config.lr = 0.1  # batch size is 512
config.output = "output/emore_random_resnet2"
config.global_step=295672
config.s=64.0
config.m=0.5

#net paramerters
config.net_name="mixfacenet"

config.net_size="s"
config.scale=1.0
config.gdw_size=1024
config.shuffle=True
if (config.net_size=="s"):
    config.gdw_size = 512

if config.dataset == "emore":
    config.rec = "/data/fboutros/faces_emore"
    config.num_classes = 85742
    config.num_image = 5822653
    config.num_epoch =  26
    config.warmup_epoch = -1
    config.val_targets = ["lfw", "cfp_fp", "agedb_30" ]
    def lr_step_func(epoch):
        return ((epoch + 1) / (4 + 1)) ** 2 if epoch < -1 else 0.1 ** len(
            [m for m in [ 8, 14,20,25] if m - 1 <= epoch])  # [m for m in [8, 14,20,25] if m - 1 <= epoch])
    config.lr_func = lr_step_func

elif config.dataset == "ms1m-retinaface-t2":
    config.rec = "/train_tmp/ms1m-retinaface-t2"
    config.num_classes = 91180
    config.num_epoch = 25
    config.warmup_epoch = -1
    config.val_targets = ["lfw", "cfp_fp", "agedb_30"]

    def lr_step_func(epoch):
        return ((epoch + 1) / (4 + 1)) ** 2 if epoch < -1 else 0.1 ** len(
            [m for m in [11, 17, 22] if m - 1 <= epoch])
    config.lr_func = lr_step_func




