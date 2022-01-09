# 2021년도 CNU 창의SW축전 창의작품경진대회

## 팀명 : Brightling
## Project : 야간 CCTV 영상화질 개선 및 객체 탐지

### 1.  배경 및 목적

-  통합관제센터의 관제 인력 부족
-  통합관제센터의 저화질 CCTV의 경우 어두운 환경에서 객체 식별에 어려움이 있음.
-  기존의 저화질 CCTV를 단기간에 모두 교체하기에는 예산 문제가 있음

#### 인터뷰 요청_문제 인식 및 정의
<img width="685" alt="인터뷰요청" src="https://user-images.githubusercontent.com/49335804/148665514-73bd59f9-b52e-4425-a70c-f1baf51c9b2b.png">

#### 인터뷰 결과_문제점 파악
<img width="704" alt="인터뷰 결과" src="https://user-images.githubusercontent.com/49335804/148665518-db013394-fd7a-4ec3-a9a6-f7e930f2a356.png">


### 2. 개발환경 및 개발언어

### Training 환경
- OS : Ubuntu 20.04 LTS
- GPU : 8 x NVIDIA Tesla P100 PCIe 16GB
- CUDA Toolkit : Driver 460.32, CUDA 11.2
- 사용 언어 : Python 3.7 이상

### 구동 환경
- OS : Windows 10 Pro Build 19043.1165
- CPU: i7-11700K
- RAM: 32GB DDR4
- GPU: GeForce RTX 3080

### 3. 시스템 구성 및 아키텍처

- 저조도 모델 : EnlightenGan(17 Jun 2019  ·  Yifan Jiang, Xinyu Gong, Ding Liu, Yu Cheng, Chen Fang, Xiaohui Shen, Jianchao Yang, Pan Zhou, Zhangyang Wang )
- https://arxiv.org/pdf/1906.06972v2.pdf
- https://github.com/arsenyinfo/EnlightenGAN-inference

- 객체 탐지 모델 : Yolov5
- https://github.com/ultralytics/yolov5

### 4. 모델 학습 결과
epoch 50
![training_results1](https://user-images.githubusercontent.com/41338783/132691322-6089e5c8-5598-42ad-ab41-bfa400894b2b.png)

epoch 200
![training_results2](https://user-images.githubusercontent.com/41338783/141113925-9b06f9fd-69d3-421f-9ba0-6bb735e4b7c9.png)

### 5. 프로젝트 주요기능

<img width="649" alt="시스템 서비스" src="https://user-images.githubusercontent.com/49335804/148665531-ada32eb7-7852-4162-a938-110fc2caa35b.png">

- 저조도 개선 : 저조도 영상을 입력으로 받아 밝기 개선
- 객체 탐지 : 저조도 영상을 입력으로 받아 저조도 환경에서도 객체에 대한 Bounding Box 출력
- 로그 기록 : 객체 탐지된 영상에 대해서 탐지된 객체의 로그 기록 저장

### 6. 기대 효과
#### 야간식별 문제 해결
<img width="715" alt="야간식별문제해결" src="https://user-images.githubusercontent.com/49335804/148665536-8821bd16-0d8f-4523-81a4-3357ed46207c.png">

#### 인력부족 문제 해결
<img width="560" alt="인력부족문제해결" src="https://user-images.githubusercontent.com/49335804/148665550-86df0397-7700-422e-90a9-f8084d7ad075.png">

### 7. 기능 및 UI 개선
<img width="743" alt="기능및 UI 개선" src="https://user-images.githubusercontent.com/49335804/148665555-60e358c5-7c44-44d8-bef0-3c0cba7e79b6.png">

### 8. 시연 영상
링크 : https://youtu.be/52OB8Pl12Ws
