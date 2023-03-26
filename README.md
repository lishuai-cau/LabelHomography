# labelhomography

A tool that can visually mark the homography transformation relationship of images, released by Li Shuai, current tested on ubuntu and windows 



## Setup

Dependencies:

+ numpy == 1.22.3
+ opencv == 4.5.5.64

Installation:

+ `pip install numpy==1.22.3`
+ ` pip install opencv==4.5.5.64`

If your system is a version below ubuntu20.04,you can use pip3 instead of pip 

## Demo

Put your images in image folder ，label the left image and the right image respectively, and note that each group of points first labels the left image:

![1](https://github.com/lishuai-cau/LabelHomography/blob/master/Image/1.jpg)

Label result:

![2](https://github.com/lishuai-cau/LabelHomography/blob/master/Image/2.jpg)

You can adjust whether it is grayscale or color annotation by passing in different parameters

gray mode:

```python
read_path("./Image",mode='gray')
```

color mode:

```python
read_path("./Image",mode='color')
```

## Contact us

+ mail: lishuaicau@gmail.com
