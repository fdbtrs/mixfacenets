# MixFaceNets



## This is the official repository of the paper: MixFaceNets: Extremely Efficient Face Recognition Networks.
(MixFaceNets)[https://ieeexplore.ieee.org/abstract/document/9484374]




| Model  | MFLOPs |Params (M)|LFW %| AgeDB-30 % |IJB-B ( TAR at FAR1e–6) | IJB-C ( TAR at FAR1e–6)| Pretrained model|
| ------------- | ------------- |------------- |------------- |------------- |------------- |------------- |------------- |
| MixFaceNet-M         | 626.1     | 3.95          | 99.68     | 97.05         | 91.55 | 93.42 | |
| ShuffleMixFaceNet-M   | 626.1     | 3.95         | 99.60      | 96.98        | 91.47 | 93.5  | |
| MixFaceNet-S         | 451.7     | 3.07         | 99.60    | 96.63         |90.17 | 92.30 | 
|ShuffleMixFaceNet-S   | 451.7     | 3.07         | 99.58     | 97.05        |90.94 | 93.08  | (pretrained-mode)[pretrained_model/ShuffleMixFaceNet-S]|
|MixFaceNet-XS        | 161.9     | 1.04          |99.60     | 95.85         | 88.48 | 90.73 | |
|ShuffleMixFaceNet-XS  | 161.9     | 1.04         | 99.53     | 95.62         |87.86 | 90.43 | |


If you find MixFaceNets useful in your research, please consider to cite the following related paper:


## Citation
```
@INPROCEEDINGS{9484374,
  author={Boutros, Fadi and Damer, Naser and Fang, Meiling and Kirchbuchner, Florian and Kuijper, Arjan},
  booktitle={2021 IEEE International Joint Conference on Biometrics (IJCB)}, 
  title={MixFaceNets: Extremely Efficient Face Recognition Networks}, 
  year={2021},
  volume={},
  number={},
  pages={1-8},
  doi={10.1109/IJCB52358.2021.9484374}}


```
The model is trained with ArcFace loss using Partial-FC algorithms.
If you train the MixfaceNets with ArcFace and  Partial-FC, please follow distribution licenses. 


## Citation
```
@inproceedings{deng2019arcface,
  title={Arcface: Additive angular margin loss for deep face recognition},
  author={Deng, Jiankang and Guo, Jia and Xue, Niannan and Zafeiriou, Stefanos},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
  pages={4690--4699},
  year={2019}
}
@inproceedings{an2020partical_fc,
  title={Partial FC: Training 10 Million Identities on a Single Machine},
  author={An, Xiang and Zhu, Xuhan and Xiao, Yang and Wu, Lan and Zhang, Ming and Gao, Yuan and Qin, Bin and
  Zhang, Debing and Fu Ying},
  booktitle={Arxiv 2010.05222},
  year={2020}
}
```
