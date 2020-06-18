import numpy as np
import cv2
sift = cv2.xfeatures2d.SIFT_create() # Calling the SIFT algorithm

#IMAGES ALREADY NEED TO A COMBINED FORM OF THE TWO IMAGES
class Stitcher:
#    def __init__(self):
#        self.isv3 = imutils.is_cv3()
          #Checks which CV version being used as large differencesthe different versions
                              
        # unpack the images, then detect keypoints and extract
	 # local invariant descriptors from them
      #images is list of (two) images that we are going to stitch together to form the panorama
      #reprojThresh  which is the maximum pixel “wiggle room” allowed by the RANSAC algorithm like deadband
    def stitch(self,images,ratio=0.75,reprojThresh=10,showMatches=False):
        (image_left,image_right)=images
        (X_left,Y_left)=self.detectAndDescribe(image_left)
        (X_right,Y_right)=self.detectAndDescribe(image_right)
        #The ordering to the images  list is important: we expect images to be supplied in left-to-right order.
        #Match features of the two images
        #OR GEBERATE A CRITICAL VALUE FOR M TO FIND THE BEST IMAGE QUALITY
        for i in range(10):
            M=self.matchKeypoints(X_left,X_right,Y_left,Y_right)
        if M is None:
            print("Not Enough matching points found")
       # MATCHES gives a list of keypoint not necessarily matched
       # STATUS a list of indexes to indicate which keypoints in matches  were successfully spatially verified using RANSAC.
        (matches, H, status) = M
    # Shape out of the output image is the sum of the lengths of both images and then using the height of the second image
        result = cv2.warpPerspective(image_left, H,(image_left.shape[1] + image_right.shape[1], image_left.shape[0]))
    # HERE image_left variable defines the right image 
        result[0:image_right.shape[0], 0:image_right.shape[1]] = image_right
    
# check to see if the keypoint matches should be visualiz
        if showMatches:
            vis = self.drawMatches(image_left, image_right, X_left, X_right, matches,status)
            return (result,vis)
        return result #This is waht the function returns
       
#     Method accepts an image, then detects keypoints and extracts local invariant descriptors
    def detectAndDescribe(self, image):
        # detect and extract features from the image
        descriptor = cv2.xfeatures2d.SIFT_create()
        (kps, features) = descriptor.detectAndCompute(image, None)
        # convert the keypoints from KeyPoint objects to NumPy  arrays
        kps = np.float32([kp.pt for kp in kps])
        return (kps, features)
    
    def matchKeypoints(self,X_left,X_right,Y_left,Y_right,ratio=0.75,reprojThresh=10):
        # compute the raw matches and initialize the list of actual# matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        #performs k-NN matching between the two feature vector sets using k=2 
        #(indicating the top two matches for each feature vector are returned)
        #The reason we want the top two matches rather than just the top one match is because 
        #we need to apply David Lowe’s ratio test for false-positive match pruning
        rawMatches = matcher.knnMatch(Y_left, Y_right, 2)
        matches=[]
    #loop over the matches
        for m in rawMatches:
        # ensure the distance is within a certain ratio of each# other
        #Lowe’s ratio test, which is used to determine high-quality feature matches. 
        #Typical values for Lowe’s ratio are normally in the range [0.7, 0.8].
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
    
    # Computing a homography between two sets of points requires at a bare minimum
    # an initial set of four matches. For a more reliable homography estimation, 
    # we should have substantially more than just four matched points
        if len(matches)>4:
        # construct the two sets of points
            ptsA = np.float32([X_left[i] for (_, i) in matches])
            ptsB = np.float32([X_right[i] for (i, _) in matches])
        
        # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,reprojThresh)
        # return the matches along with the homograpy matrix and status of each matched point
            return (matches, H, status)
    #Used to visualize keypoint correspondences between two images:
    def drawMatches(self, image_left, image_right, X_left, X_right, matches, status):
        # initialize the output visualization image
        (hA, wA) = image_left.shape[:2]
        (hB, wB) = image_right.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = image_left
        vis[0:hB, wA:] = image_right

        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            if s == 1:
                ptA = (int(X_left[queryIdx][0]), int(X_left[queryIdx][1]))
                ptB = (int(X_right[trainIdx][0]) + wA, int(X_right[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
        return vis