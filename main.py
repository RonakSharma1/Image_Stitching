from ImageStitching import Stitcher
import cv2
import pylab as plt

imageA = cv2.imread("Image_Left_1.jpg")
imageB = cv2.imread("Image_Right_1.jpg")

#-----Image Dimensions-------#
width=400
height=800
dsizeImageA = (width, height)
dsizeImageB = (width, height)
#---------------------------#

# Resize image
imageA = cv2.resize(imageA, dsizeImageA)
imageB = cv2.resize(imageB, dsizeImageB)

# Stitch the images together to create a panorama
stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

# Save images
cv2.imwrite("Processed Image.png",result)
cv2.imwrite("Keypoint Matches.png",vis)

#---- Shows the stiched image on a graph for measuring distances--------#
plt.grid(True)
plt.imshow(result)
plt.show()
#---------------------------#
cv2.waitKey(0)


