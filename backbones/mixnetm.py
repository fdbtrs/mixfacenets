

__all__ = ['MixNet', 'mixnet_s', 'mixnet_m', 'mixnet_l']


import torch.nn.init as init

import math
import torch
import torch.nn as nn

from backbones.activation import get_activation_layer, HSwish, Swish
from backbones.common import dwconv3x3_block, SEBlock
from backbones.utils import conv1x1, round_channels, _calc_width, ConvBlock, conv3x3_block, dwconv_block, conv1x1_block, \
    DwsConvBlock, channel_shuffle2, count_model_flops








class MixConv(nn.Module):
    """
    Mixed convolution layer from 'MixConv: Mixed Depthwise Convolutional Kernels,' https://arxiv.org/abs/1907.09595.

    Parameters:
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    kernel_size : int or tuple/list of int, or tuple/list of tuple/list of 2 int
        Convolution window size.
    stride : int or tuple/list of 2 int
        Strides of the convolution.
    padding : int or tuple/list of int, or tuple/list of tuple/list of 2 int
        Padding value for convolution layer.
    dilation : int or tuple/list of 2 int, default 1
        Dilation value for convolution layer.
    groups : int, default 1
        Number of groups.
    bias : bool, default False
        Whether the layer uses a bias vector.
    axis : int, default 1
        The axis on which to concatenate the outputs.
    """
    def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size,
                 stride,
                 padding,
                 dilation=1,
                 groups=1,
                 bias=False,
                 axis=1):
        super(MixConv, self).__init__()
        kernel_size = kernel_size if isinstance(kernel_size, list) else [kernel_size]
        padding = padding if isinstance(padding, list) else [padding]
        kernel_count = len(kernel_size)
        self.splitted_in_channels = self.split_channels(in_channels, kernel_count)
        splitted_out_channels = self.split_channels(out_channels, kernel_count)

        for i, kernel_size_i in enumerate(kernel_size):
            in_channels_i = self.splitted_in_channels[i]
            out_channels_i = splitted_out_channels[i]
            padding_i = padding[i]
            self.add_module(
                name=str(i),
                module=nn.Conv2d(
                    in_channels=in_channels_i,
                    out_channels=out_channels_i,
                    kernel_size=kernel_size_i,
                    stride=stride,
                    padding=padding_i,
                    dilation=dilation,
                    groups=(out_channels_i if out_channels == groups else groups),
                    bias=bias))
        self.axis = axis

    def forward(self, x):
        xx = torch.split(x, self.splitted_in_channels, dim=self.axis)
        out = [conv_i(x_i) for x_i, conv_i in zip(xx, self._modules.values())]
        x = torch.cat(tuple(out), dim=self.axis)
        return x

    @staticmethod
    def split_channels(channels, kernel_count):
        splitted_channels = [channels // kernel_count] * kernel_count
        splitted_channels[0] += channels - sum(splitted_channels)
        return splitted_channels


class MixConvBlock(nn.Module):
    """
    Mixed convolution block with Batch normalization and activation.

    Parameters:
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    kernel_size : int or tuple/list of int, or tuple/list of tuple/list of 2 int
        Convolution window size.
    stride : int or tuple/list of 2 int
        Strides of the convolution.
    padding : int or tuple/list of int, or tuple/list of tuple/list of 2 int
        Padding value for convolution layer.
    dilation : int or tuple/list of 2 int, default 1
        Dilation value for convolution layer.
    groups : int, default 1
        Number of groups.
    bias : bool, default False
        Whether the layer uses a bias vector.
    use_bn : bool, default True
        Whether to use BatchNorm layer.
    bn_eps : float, default 1e-5
        Small float added to variance in Batch norm.
    activation : function or str or None, default nn.ReLU(inplace=True)
        Activation function or name of activation function.
    activate : bool, default True
        Whether activate the convolution block.
    """
    def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size,
                 stride,
                 padding,
                 dilation=1,
                 groups=1,
                 bias=False,
                 use_bn=True,
                 bn_eps=1e-5,
                 activation=(lambda: nn.ReLU(inplace=True))):
        super(MixConvBlock, self).__init__()
        self.activate = (activation is not None)
        self.use_bn = use_bn

        self.conv = MixConv(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            dilation=dilation,
            groups=groups,
            bias=bias)
        if self.use_bn:
            self.bn = nn.BatchNorm2d(
                num_features=out_channels,
                eps=bn_eps)
        if self.activate:
            self.activ = get_activation_layer(activation,out_channels)

    def forward(self, x):
        x = self.conv(x)
        if self.use_bn:
            x = self.bn(x)
        if self.activate:
            x = self.activ(x)

        return x


def mixconv1x1_block(in_channels,
                     out_channels,
                     kernel_count,
                     stride=1,
                     groups=1,
                     bias=False,
                     use_bn=True,
                     bn_eps=1e-5,
                     activation=(lambda: nn.ReLU(inplace=True))):
    """
    1x1 version of the mixed convolution block.

    Parameters:
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    kernel_count : int
        Kernel count.
    stride : int or tuple/list of 2 int, default 1
        Strides of the convolution.
    groups : int, default 1
        Number of groups.
    bias : bool, default False
        Whether the layer uses a bias vector.
    use_bn : bool, default True
        Whether to use BatchNorm layer.
    bn_eps : float, default 1e-5
        Small float added to variance in Batch norm.
    activation : function or str, or None, default nn.ReLU(inplace=True)
        Activation function or name of activation function.
    """
    return MixConvBlock(
        in_channels=in_channels,
        out_channels=out_channels,
        kernel_size=([1] * kernel_count),
        stride=stride,
        padding=([0] * kernel_count),
        groups=groups,
        bias=bias,
        use_bn=use_bn,
        bn_eps=bn_eps,
        activation=activation)


class MixUnit(nn.Module):
    """
    MixNet unit.

    Parameters:
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    exp_channels : int
        Number of middle (expanded) channels.
    stride : int or tuple/list of 2 int
        Strides of the second convolution layer.
    exp_kernel_count : int
        Expansion convolution kernel count for each unit.
    conv1_kernel_count : int
        Conv1 kernel count for each unit.
    conv2_kernel_count : int
        Conv2 kernel count for each unit.
    exp_factor : int
        Expansion factor for each unit.
    se_factor : int
        SE reduction factor for each unit.
    activation : str
        Activation function or name of activation function.
    """
    def __init__(self,
                 in_channels,
                 out_channels,
                 stride,
                 exp_kernel_count,
                 conv1_kernel_count,
                 conv2_kernel_count,
                 exp_factor,
                 se_factor,
                 activation, shuffle=True):
        super(MixUnit, self).__init__()
        assert (exp_factor >= 1)
        assert (se_factor >= 0)
        self.shuffle=shuffle
        self.residual = (in_channels == out_channels) and (stride == 1)
        self.use_se = se_factor > 0
        mid_channels = exp_factor * in_channels
        self.use_exp_conv = exp_factor > 1
        self.conv1_kernel_count=conv1_kernel_count
        if self.use_exp_conv:
            if exp_kernel_count == 1:
                self.exp_conv = conv1x1_block(
                    in_channels=in_channels,
                    out_channels=mid_channels,
                    activation=activation)
            else:
                self.exp_conv = mixconv1x1_block(
                    in_channels=in_channels,
                    out_channels=mid_channels,
                    kernel_count=exp_kernel_count,
                    activation=activation)
        if conv1_kernel_count == 1:
            self.conv1 = dwconv3x3_block(
                in_channels=mid_channels,
                out_channels=mid_channels,
                stride=stride,
                activation=activation)
        else:
            self.conv1 = MixConvBlock(
                in_channels=mid_channels,
                out_channels=mid_channels,
                kernel_size=[3 + 2 * i for i in range(conv1_kernel_count)],
                stride=stride,
                padding=[1 + i for i in range(conv1_kernel_count)],
                groups=mid_channels,
                activation=activation)
        if self.use_se:
            self.se = SEBlock(
                channels=mid_channels,
                reduction=(exp_factor * se_factor),
                round_mid=False,
                mid_activation=activation)
        if conv2_kernel_count == 1:
            self.conv2 = conv1x1_block(
                in_channels=mid_channels,
                out_channels=out_channels,
                activation=None)
        else:
            self.conv2 = mixconv1x1_block(
                in_channels=mid_channels,
                out_channels=out_channels,
                kernel_count=conv2_kernel_count,
                activation=None)

    def forward(self, x):
        if self.residual:
            identity = x
        if self.use_exp_conv:
            x = self.exp_conv(x)
        x = self.conv1(x)
        if self.use_se:
            x = self.se(x)
        x = self.conv2(x)
        if self.residual:
            x = x + identity
        if (self.shuffle):
         x=channel_shuffle2(x,2)

        return x


class MixInitBlock(nn.Module):
    """
    MixNet specific initial block.

    Parameters:
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    """
    def __init__(self,
                 in_channels,
                 out_channels,activation,stride=1, shuffle=True):
        super(MixInitBlock, self).__init__()
        self.conv1 = conv3x3_block(
            in_channels=in_channels,
            out_channels=out_channels,
            stride=stride,activation=activation)
        self.conv2 = MixUnit(
            in_channels=out_channels,
            out_channels=out_channels,
            stride=1,
            exp_kernel_count=1,
            conv1_kernel_count=1,
            conv2_kernel_count=1,
            exp_factor=1,
            se_factor=0,
            activation=activation,shuffle=shuffle)

    def forward(self, x):
        x = self.conv1(x)

        x = self.conv2(x)

        return x


class MixNet(nn.Module):
    """
    MixNet model from 'MixConv: Mixed Depthwise Convolutional Kernels,' https://arxiv.org/abs/1907.09595.

    Parameters:
    ----------
    channels : list of list of int
        Number of output channels for each unit.
    init_block_channels : int
        Number of output channels for the initial unit.
    final_block_channels : int
        Number of output channels for the final block of the feature extractor.
    exp_kernel_counts : list of list of int
        Expansion convolution kernel count for each unit.
    conv1_kernel_counts : list of list of int
        Conv1 kernel count for each unit.
    conv2_kernel_counts : list of list of int
        Conv2 kernel count for each unit.
    exp_factors : list of list of int
        Expansion factor for each unit.
    se_factors : list of list of int
        SE reduction factor for each unit.
    in_channels : int, default 3
        Number of input channels.
    in_size : tuple of two ints, default (224, 224)
        Spatial size of the expected input image.
    num_classes : int, default 1000
        Number of classification classes.
    """
    def __init__(self,
                 channels,
                 init_block_channels,
                 final_block_channels,
                 exp_kernel_counts,
                 conv1_kernel_counts,
                 conv2_kernel_counts,
                 exp_factors,
                 se_factors,
                 in_channels=3,
                 in_size=(112, 112),
                 num_classes=1000,gdw_size=512,shuffle=True):
        super(MixNet, self).__init__()
        self.in_size = in_size
        self.num_classes = num_classes
        self.shuffle=shuffle
        self.features = nn.Sequential()
        self.features.add_module("init_block", MixInitBlock(
            in_channels=in_channels,
            out_channels=init_block_channels,activation="prelu",stride=2))
        in_channels = init_block_channels
        for i, channels_per_stage in enumerate(channels):
            stage = nn.Sequential()
            for j, out_channels in enumerate(channels_per_stage):  #                stride = 2 if ((j == 0) and (i != 3) and (i !=0)) or ((j == len(channels_per_stage) // 2) and (i == 3)) else 1
                stride = 2 if ((j == 0) and (i != 3) and (i !=0)) or ((j == len(channels_per_stage) // 2) and (i == 3)) else 1
                exp_kernel_count = exp_kernel_counts[i][j]
                conv1_kernel_count = conv1_kernel_counts[i][j]
                conv2_kernel_count = conv2_kernel_counts[i][j]
                exp_factor = exp_factors[i][j]
                se_factor = se_factors[i][j]
                activation = "prelu" if i == 0 else "swish"
                stage.add_module("unit{}".format(j + 1), MixUnit(
                    in_channels=in_channels,
                    out_channels=out_channels,
                    stride=stride,
                    exp_kernel_count=exp_kernel_count,
                    conv1_kernel_count=conv1_kernel_count,
                    conv2_kernel_count=conv2_kernel_count,
                    exp_factor=exp_factor,
                    se_factor=se_factor,
                    activation=activation,shuffle=self.shuffle))
                in_channels = out_channels
            self.features.add_module("stage{}".format(i + 1), stage)

        self.tail=conv1x1_block(
            in_channels=in_channels,
            out_channels=gdw_size,activation="prelu")
        self.feautre_layer=DwsConvBlock(in_channels=gdw_size,out_channels=final_block_channels,kernel_size=7,padding=0,stride=1,pw_activation=None,dw_activation=None,pw_use_bn=False)
        self.features_norm = nn.BatchNorm1d(final_block_channels , eps=1e-05)
        nn.init.constant_(self.features_norm.weight, 1.0)
        self.features_norm.weight.requires_grad = False
        self._init_params()

    def _init_params(self):
        for name, module in self.named_modules():
            if isinstance(module, nn.Conv2d):
                init.kaiming_uniform_(module.weight)
                if module.bias is not None:
                    init.constant_(module.bias, 0)
            elif isinstance(module, (nn.BatchNorm2d, nn.GroupNorm)):
                nn.init.constant_(module.weight, 1)
                nn.init.constant_(module.bias, 0)

    def forward(self, x):
        x = self.features(x)
        x=self.tail(x)
        x=self.feautre_layer(x)
        x = x.view(x.size(0), -1)
        x=self.features_norm(x)
        return x


def get_mixnet(version,
               width_scale, embedding_size=512,model_name="mixnet_s",gdw_size=512
              ,weight=None,shuffle=True,
               **kwargs):
    """
    Create MixNet model with specific parameters.

    Parameters:
    ----------
    version : str
        Version of MobileNetV3 ('s' or 'm').
    width_scale : float
        Scale factor for width of layers.
    model_name : str or None, default None
        Model name for loading pretrained model.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.torch/models'
        Location for keeping the model parameters.
    """

    if version == "s":
        init_block_channels = 16
        channels = [[24, 24], [40, 40, 40, 40], [80, 80, 80], [120, 120, 120, 200, 200, 200]]
        exp_kernel_counts = [[2, 2], [1, 2, 2, 2], [1, 1, 1], [2, 2, 2, 1, 1, 1]]
        conv1_kernel_counts = [[1, 1], [3, 2, 2, 2], [3, 2, 2], [3, 4, 4, 5, 4, 4]]
        conv2_kernel_counts = [[2, 2], [1, 2, 2, 2], [2, 2, 2], [2, 2, 2, 1, 2, 2]]
        exp_factors = [[6, 3], [6, 6, 6, 6], [6, 6, 6], [6, 3, 3, 6, 6, 6]]
        se_factors = [[0, 0], [2, 2, 2, 2], [4, 4, 4], [2, 2, 2, 2, 2, 2]]
    elif version == "m":
        init_block_channels = 24
        channels = [[32, 32], [40, 40, 40, 40], [80, 80, 80, 80], [120, 120, 120, 120, 200, 200, 200, 200]]
        exp_kernel_counts = [[2, 2], [1, 2, 2, 2], [1, 2, 2, 2], [1, 2, 2, 2, 1, 1, 1, 1]]
        conv1_kernel_counts = [[3, 1], [4, 2, 2, 2], [3, 4, 4, 4], [1, 4, 4, 4, 4, 4, 4, 4]]
        conv2_kernel_counts = [[2, 2], [1, 2, 2, 2], [1, 2, 2, 2], [1, 2, 2, 2, 1, 2, 2, 2]]
        exp_factors = [[6, 3], [6, 6, 6, 6], [6, 6, 6, 6], [6, 3, 3, 3, 6, 6, 6, 6]]
        se_factors = [[0, 0], [2, 2, 2, 2], [4, 4, 4, 4], [2, 2, 2, 2, 2, 2, 2, 2]]
    else:
        raise ValueError("Unsupported MixNet version {}".format(version))

    final_block_channels = embedding_size

    if width_scale != 1.0:
        channels = [[round_channels(cij * width_scale) for cij in ci] for ci in channels]
        init_block_channels = round_channels(init_block_channels * width_scale)

    net = MixNet(
        channels=channels,
        init_block_channels=init_block_channels,
        final_block_channels=final_block_channels,
        exp_kernel_counts=exp_kernel_counts,
        conv1_kernel_counts=conv1_kernel_counts,
        conv2_kernel_counts=conv2_kernel_counts,
        exp_factors=exp_factors,
        se_factors=se_factors,gdw_size=gdw_size,shuffle=shuffle,
        **kwargs)
    if (weight is not None):
        weight = torch.load(weight)
        net.load_state_dict(weight)


    return net


def mixnet_s(embedding_size=512,width_scale=0.5,gdw_size=512, weight=None,shuffle=True,**kwargs):
    """
    MixNet-S model from 'MixConv: Mixed Depthwise Convolutional Kernels,' https://arxiv.org/abs/1907.09595.

    Parameters:
    ----------
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.torch/models'
        Location for keeping the model parameters.
    """
    return get_mixnet(version="s", width_scale=width_scale,embedding_size=embedding_size,gdw_size=gdw_size, model_name="mixnet_s",shuffle=shuffle, **kwargs)


def mixnet_m(embedding_size=512,width_scale=0.5,gdw_size=512,shuffle=True,**kwargs):
    """
    MixNet-M model from 'MixConv: Mixed Depthwise Convolutional Kernels,' https://arxiv.org/abs/1907.09595.

    Parameters:
    ----------
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.torch/models'
        Location for keeping the model parameters.
    """
    return get_mixnet(version="m", width_scale=width_scale,embedding_size=embedding_size,gdw_size=gdw_size, model_name="mixnet_m",shuffle=shuffle, **kwargs)


def mixnet_l(embedding_size=512,width_scale=1.3,shuffle=True,**kwargs):
    """
    MixNet-L model from 'MixConv: Mixed Depthwise Convolutional Kernels,' https://arxiv.org/abs/1907.09595.

    Parameters:
    ----------
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.torch/models'
        Location for keeping the model parameters.
    """
    return get_mixnet(version="m", width_scale=width_scale,embedding_size=embedding_size, model_name="mixnet_l",shuffle=shuffle, **kwargs)




def _test():
    import torch

    pretrained = False

    models = [
        mixnet_s
    ]

    for model in models:

        net = model(embedding_size=512,width_scale=1.0,gdw_size=1024)
        print(net)
        weight_count = _calc_width(net)
        flops=count_model_flops(net)
        print("m={}, {}".format(model.__name__, weight_count))
        print("m={}, {}".format(model.__name__, flops))
        net.eval()

        x = torch.randn(1, 3, 112, 112)

        y = net(x)
        y.sum().backward()
        assert (tuple(y.size()) == (1, 512))


if __name__ == "__main__":
    _test()
