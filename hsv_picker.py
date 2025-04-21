import cv2

# Load the image you uploaded
img_bgr = cv2.imread("debug_hsv.jpg")
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

def show_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = img_hsv[y, x]
        print(f"Clicked HSV: {pixel} at ({x},{y})")

cv2.imshow("Click the Ball", img_bgr)
cv2.setMouseCallback("Click the Ball", show_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
