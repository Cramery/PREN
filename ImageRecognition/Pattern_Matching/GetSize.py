import cv2

filename = 'pictures_real/templates/3.jpg'
oriimg = cv2.imread(filename)
img = cv2.resize(oriimg, (15,30))
cv2.imwrite('pictures_real/templates/3.jpg', img)