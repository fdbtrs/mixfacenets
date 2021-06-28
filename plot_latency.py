import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
fontP = FontProperties()
db="IJB-C"
if (db=="agedb"):
    agedb = [98.100,97.32,97.6,96.4,94.4,97.05,96.983,96.633,97.05,95.85,95.617,96.07,93.22]
    accuracies=agedb
    flops = [1000,577.5,900,1100,900,626.1,626.1,451.7,451.7,161.9,161.9,439.8,66.9]
    nets=["VarGFaceNet", "ShuffleFaceNet 1.5", "MobileFaceNet", "MobileFaceNetV1", "ProxylessFaceNAS", "MixFaceNet-M(ours)","ShuffleMixFaceNet-M(ours)","MixFaceNet-S(ours)","ShuffleMixFaceNet-S(ours)","MixFaceNet-XS(ours)","ShuffleMixFaceNet-XS(ours)","MobileFaceNets","ShuffleFaceNet 0.5"]
    marker=['o', '.', 'H', 'x', '+', 'v', 'v', 'v', 'v', 'v', 'v','1','2','3']
    save_path = "./agedb.png"
    plt.figure()
    fig, ax = plt.subplots()
    plt.plot(accuracies, flops, 'o')
    plt.ylabel("Accuracy (%) ",fontsize=16)
    plt.xlabel("MFLOPs",fontsize=16)
    plt.ylim([93.15, 98.5])
    plt.xlim([50, 1200])
elif(db=="lfw"):
    accuracies = [99.683,99.67,99.7,99.4,99.2,99.683,99.6,99.65,99.583,99.6,99.533,99.55,99.23,99.3]
    flops = [1000,577.5,900,1100,900,626.1,626.1,451.7,451.7,161.9,161.9,439.8,66.9,1000]
    nets=["VarGFaceNet", "ShuffleFaceNet 1.5", "MobileFaceNet", "MobileFaceNetV1", "ProxylessFaceNAS", "MixFaceNet-M(ours)","ShuffleMixFaceNet-M(ours)","MixFaceNet-S(ours)","ShuffleMixFaceNet-S(ours)","MixFaceNet-XS(ours)","ShuffleMixFaceNet-XS(ours)","MobileFaceNets","ShuffleFaceNet 0.5","AirFace"]
    marker=['o', '.', 'H', 'x', '+', 'v', 'v', 'v', 'v', 'v', 'v','1','2','3']
    save_path = "./lfw.png"
    plt.figure()
    fig, ax = plt.subplots()
    plt.plot(accuracies, flops, 'o')
    plt.ylabel("Accuracy (%) ",fontsize=16)
    plt.xlabel("MFLOPs",fontsize=16)
    plt.ylim([99.15, 99.81])
    plt.xlim([50, 1200])
elif(db=="megaface"):
    accuracies = [93.9,93.0,95.2,91.3,82.8,94.26,94.24,92.23,93.60,89.40,89.24,90.16,96.52]
    flops = [1000,577.5,900,1100,900,626.1,626.1,451.7,451.7,161.9,161.9,439.8,1000]
    nets=["VarGFaceNet", "ShuffleFaceNet 1.5", "MobileFaceNet", "MobileFaceNetV1", "ProxylessFaceNAS", "MixFaceNet-M(ours)","ShuffleMixFaceNet-M(ours)","MixFaceNet-S(ours)","ShuffleMixFaceNet-S(ours)","MixFaceNet-XS(ours)","ShuffleMixFaceNet-XS(ours)","MobileFaceNets","AirFace"]
    marker=['o', '.', 'H', 'x', '+', 'v', 'v', 'v', 'v', 'v', 'v','1','3']
    save_path = "./megaface.png"
    plt.figure()
    fig, ax = plt.subplots()
    plt.plot(accuracies, flops, 'o')
    plt.ylabel("TAR at FAR1e–6 ",fontsize=16)
    plt.xlabel("MFLOPs",fontsize=16)
    plt.ylim([82.1, 96.7])
    plt.xlim([50, 1200])
elif(db=="megafacer"):
    accuracies = [95.6,94.6,96.8,93.0 ,84.8 ,95.83 ,95.22  ,93.79, 95.19, 91.04, 91.03, 92.59, 97.93]
    flops = [1000,577.5,900,1100,900,626.1,626.1,451.7,451.7,161.9,161.9,439.8,1000]
    nets=["VarGFaceNet", "ShuffleFaceNet 1.5", "MobileFaceNet", "MobileFaceNetV1", "ProxylessFaceNAS", "MixFaceNet-M(ours)","ShuffleMixFaceNet-M(ours)","MixFaceNet-S(ours)","ShuffleMixFaceNet-S(ours)","MixFaceNet-XS(ours)","ShuffleMixFaceNet-XS(ours)","MobileFaceNets","AirFace"]
    marker=['o', '.', 'H', 'x', '+', 'v', 'v', 'v', 'v', 'v', 'v','1','3']
    save_path = "./megafacer.png"
    plt.figure()
    fig, ax = plt.subplots()
    plt.plot(accuracies, flops, 'o')
    plt.ylabel("TAR at FAR1e–6 ",fontsize=16)
    plt.xlabel("MFLOPs",fontsize=16)
    plt.ylim([84.1, 98.1])
    plt.xlim([50, 1200])

elif(db=="IJB-B"):
    accuracies = [92.9,92.3,92.8,92.0,87.1,91.55,91.47,90.17,90.94,88.48,87.86]

    flops = [1000,577.5,900,1100,900,626.1,626.1,451.7,451.7,161.9,161.9]
    nets=["VarGFaceNet", "ShuffleFaceNet 1.5", "MobileFaceNet", "MobileFaceNetV1", "ProxylessFaceNAS", "MixFaceNet-M(ours)","ShuffleMixFaceNet-M(ours)","MixFaceNet-S(ours)","ShuffleMixFaceNet-S(ours)","MixFaceNet-XS(ours)","ShuffleMixFaceNet-XS(ours)"]
    marker=['o', '.', 'H', 'x', '+', 'v', 'v', 'v', 'v', 'v', 'v','1','3']
    save_path = "./ijbb.png"
    plt.figure()
    fig, ax = plt.subplots()
    plt.plot(accuracies, flops, 'o')
    plt.ylabel("TAR at FAR1e–4 ",fontsize=16)
    plt.xlabel("MFLOPs",fontsize=16)
    plt.ylim([87, 93])
    plt.xlim([50, 1200])
elif(db=="IJB-C"):
    accuracies = [94.7,94.3,94.7,93.9,89.7,93.42,93.5,92.30,93.08,90.73,90.43]

    flops = [1000,577.5,900,1100,900,626.1,626.1,451.7,451.7,161.9,161.9]
    nets=["VarGFaceNet", "ShuffleFaceNet 1.5", "MobileFaceNet", "MobileFaceNetV1", "ProxylessFaceNAS", "MixFaceNet-M(ours)","ShuffleMixFaceNet-M(ours)","MixFaceNet-S(ours)","ShuffleMixFaceNet-S(ours)","MixFaceNet-XS(ours)","ShuffleMixFaceNet-XS(ours)"]
    marker=['o', '.', 'H', 'x', '+', 'v', 'v', 'v', 'v', 'v', 'v','1','3']
    save_path = "./ijbc.png"
    plt.figure()
    fig, ax = plt.subplots()
    plt.plot(accuracies, flops, 'o')
    plt.ylabel("TAR at FAR1e–4 ",fontsize=16)
    plt.xlabel("MFLOPs",fontsize=16)
    plt.ylim([88, 95])
    plt.xlim([50, 1200])
p=[]
for i in range(len(accuracies)):
    if "ours" in nets[i]:
        plt.plot(flops[i], accuracies[i], marker[i],markersize=12,markeredgecolor='red',label=nets[i])
    else:
        plt.plot(flops[i], accuracies[i], marker[i],markersize=12,label=nets[i])

plt.grid()

plt.legend(numpoints=1, loc='lower right',fontsize=8,ncol=2)
plt.savefig(save_path, format='png', dpi=600)
plt.close()
