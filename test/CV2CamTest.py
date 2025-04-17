import cv2

capture = cv2.VideoCapture(0)

while True:
    success, image = capture.read()

    if(success):
        imageCanny = cv2.Canny(image, 30, 60)
        anotherEffect = cv2.Canny(image, 100, 200)
        
        cv2.imshow('Cam Test', imageCanny)
        # cv2.imshow('Cam Test', anotherEffect)

    if(cv2.waitKey(1) == ord('q')):
        break


capture.release()
cv2.destroyAllWindows()
