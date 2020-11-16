# ResNet64 based Face Recognition

## Contents

1. [Environment](#Environment)
2. [Preparation](#Preparation)
3. [Train/Eval](#Train/Eval)
4. [Performance](#Performance)
5. [Model information](#Model information)

## Environment

#### Compatibility 

The test code is tested with Python 2.7. You can install the dependencies of opencv-python and protobuf by:
```shell
pip install opencv-python protobuf
```

#### Installation

1. Download and unzip Xilinx custom distribution of Caffe.

2. Build the code. Please follow [Caffe instruction](http://caffe.berkeleyvision.org/installation.html) to install all necessary packages and build it.
  ```shell
  # Modify Makefile.config according to your Caffe installation and then build Caffe.
  make -j8
  make pycaffe
  ```
  
Note: If you are in the released Docker env, there is no need to build Caffe.

## Preparation

1. Dataset description.
   Face recognition training and test datasets are private.

2. Dataset pre-processing.
   Please ensure that the dataset for face recognition has been pre-processed by face detection and face alignment.
   You could also try to run the following commands to generate aligned faces for training and test datasets.
   ```shell
   cd code/get_aligned_face/
   python get_aligned_face.py
   ```

3. Dataset directory structure:
   ```
    + data
        + dataset_name
            + images
                + ID_number0_C.jpg (ID photo)
                + ID_number1_C.jpg
                + ID_number0_A.jpg (snapshot photo)
                + ID_number1_A.jpg
            + ID_list.txt
            + snapshot_list.txt
   ```

## Train/Eval

1. Train your model. Training is not currently supported.
  
2. Evaluate the caffemodel.
```shell
# Test the float model.
python code/test/test_resnet64.py \
--model $/path/to/float/model \
--prototxt $/path/to/float/prototxt \
--caffe_path $/path/to/caffe \
--feat_name BatchNorm_61 \
--batch_size 128 \
--gpu 0

# Test the quantized model.
python code/test/test_resnet64.py \
--model $/path/to/quantized/model \
--prototxt $/path/to/quantized/prototxt \
--caffe_path $/path/to/caffe \
--feat_name BatchNorm_61_fixed \
--batch_size 128 \
--gpu 0
```

## Performance

The performance is tested on the private dataset.

* float model

FPR | TPR | Thr
-- | -- | --
1e-07  |  96.8  |  0.477
1e-06  |  98.3  |  0.425
1e-05  |  99.1  |  0.383
1e-04  |  99.4  |  0.330

* quantized model

FPR | TPR | Thr
-- | -- | --
1e-07  |  97.0 |   0.464
1e-06  |  98.2 |   0.434
1e-05  |  98.7 |   0.391
1e-04  |  99.3 |   0.338


  
## Model information

#### Data preprocess information

1. data channel order: RGB(0~255)
2. input image size: height=112, width=96
3. mean_value: 127.5, 127.5, 127.5
4. scale: 0.0078125
5. output feature size: 512D


#### Quantize the network with calibration mode

1. Replace the original network file data layer with the "ImageData" data layer
2. Modify the "ImageData" layer parameters according to the data preprocess information
3. Provide a "quant.txt" file, including image path and label information, but the label can randomly give some values
4. Give examples of data layer and "quant.txt":

```shell
layer {
  name: "data"
  type: "ImageData"
  top: "data"
  top: "label"
  include {
    phase: TRAIN
  }
  image_data_param {
    source: "quant.txt"
    batch_size: 128
    new_width: 96
    new_height: 112
  }
  transform_param {
    mirror: false
    mean_value: 127.5
    mean_value: 127.5
    mean_value: 127.5
    scale: 0.0078125
  }
}
```

```
# quant.txt: image path label
images/000001.jpg 1
images/000002.jpg 2
images/000003.jpg 3
...
```


