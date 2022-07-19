from car import Car
from arducam_camera import MyCamera
import cv2
from pose_evaluation_utils import *

device = 0
width  = 640
height = 480

# need to calibration

# width = 1241.0
# height = 376.0
# fx, fy, cx, cy = [718.8560, 718.8560, 607.1928, 185.2157]

# initial parameter

count = 0
out_pose_file = './' + 'MONO_traj_est.txt'

def camera():
    cam   = MyCamera(device, width, height)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('video/output.avi', fourcc, 20.0, (width, height))

    while cv2.waitKey(10) != ord('q'):
        frame = cam.get_frame()
        frame = cv2.resize(frame, (width, height))
        out.write(frame)
        mono_mapping(frame, count)
        cv2.imshow("Arducam", frame)
        count += 1

    cam.close_camera()
    out.release()
    cv2.destroyAllWindows()

def mono_mapping(frame, i):
    curr_img = frame

    if i == 0:
        curr_R = np.eye(3)
        curr_t = np.array([0, 0, 0])
    else:
        
        orb = cv2.ORB_create(nfeatures=6000)
        kp1, des1 = orb.detectAndCompute(prev_img, None)
        kp2, des2 = orb.detectAndCompute(curr_img, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        img_matching = cv2.drawMatches(prev_img, kp1, curr_img, kp2, matches[0:100], None)
        cv2.imshow('feature matching', img_matching)
        pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
        pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])
        E, mask = cv2.findEssentialMat(pts1, pts2, focal=fx, pp=(cx, cy), method=cv2.RANSAC, prob=0.999, threshold=1)
        pts1 = pts1[mask.ravel() == 1]
        pts2 = pts2[mask.ravel() == 1]
        _, R, t, mask = cv2.recoverPose(E, pts1, pts2, focal=fx, pp=(cx, cy))
        R = R.transpose()
        t = -np.matmul(R, t)

        if i == 1:
            curr_R = R
            curr_t = t
        else:
            curr_R = np.matmul(prev_R, R)
            curr_t = np.matmul(prev_R, t) + prev_t

        # draw the current image with keypoints
        curr_img_kp = cv2.drawKeypoints(curr_img, kp2, None, color=(0, 255, 0), flags=0)
        cv2.imshow('keypoints from current image', curr_img_kp)
    prev_img = curr_img
    [tx, ty, tz] = [curr_t[0], curr_t[1], curr_t[2]]
    qw, qx, qy, qz = rot2quat(curr_R)
    with open(out_pose_file, 'a') as f:
        f.write('%f %f %f %f %f %f %f %f\n' % (0.0, tx, ty, tz, qx, qy, qz, qw))

    prev_R = curr_R
    prev_t = curr_t

    # draw estimated trajectory (blue) and gt trajectory (red)
    offset_draw = (1000)
    cv2.circle(1000, (int(curr_t[0])+offset_draw, int(curr_t[2])+offset_draw), 1, (255,0,0), 2)
    cv2.imshow('Trajectory', 1000)
    cv2.waitKey(1)
    cv2.imwrite('trajMap_MonoRight02.png', 1000)

def jetcar():
    mycar = Car()
    if cv2.waitKey(10) == ord('w'):
        mycar.carforward()
    elif cv2.waitKey(10) == ord('s'):
        mycar.carbackward()
    elif cv2.waitKey(10) == ord('a'):
        mycar.carleft()
    elif cv2.waitKey(10) == ord('d'):
        mycar.carright()
    elif cv2.waitKey(10) == ord('h'):
        mycar.stop()

if __name__ == "__main__":
    camera()
    jetcar()