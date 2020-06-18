# Aim
This algorithm stitches two images and displays this stitched image on a xy axes plot

# Motivation
This algorithm was developed for [MATE ROV International Competition 2016/17](https://materovcompetition.org/).The mission was to survey a specified area underwater and compute the distance of some specified cargo containers from a hazardous object. To achieve this, firstly, two images were captured to be able to cover the whole survey area. This algorithm was then used to stitch the two captured images to display the survey area in one image. This stitched image was then displayed on a graph. Since the length of the 'hazardous object' was given, it was used to calculate the scaling factor. Using the stitched image and coordinate geometry, the distance of cargo containers from the hazardous object was calculated. The actual distance between them was then calculated using the earlier calculated scaling factor.

# Structure of Folder
1. Main Algorithm: 'main.py' which further executes the helper class 'ImageStitching.py'
2. 'Image_Left_1.jpg': Image capturing more towards the left of the objects
3. 'Image_Right_1.jpg': Image capturing more towards the right of the objects

# Setup/ Installation
1. Software: Python3
2. [Scale-Invariant Feature Transform(SIFT)](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html#feature-homography) was used for image stitching. This is a patented algorithm, hence not available in each open-cv version. Therefore, install the following open cv versions to use this software for free
```
pip3 install opencv-python==3.3.0.10 
pip3 install opencv-contrib-python==3.3.0.10 
```
3. Install 'pylab' library if not present
4. Clone the images provided and execute the 'main.py'


# Results
## Below two images underwent the stitching process

IMAGES
IMAGES

## Shows the common features identified in the above images using SIFT Algorithm 
IMAGE

## Shows the final stitched image displayed on a graph to calculate the distance between the two objects. A reference distance was provided to calculate the scaling factor.

IMAGE

Multiple experiments were conducted by modifying the orientation and distances between these objects. On average an error of 0.05% was achieved between the algorithm computed and actual distance of the object. This shows a high accuracy of this algorithm.