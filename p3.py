from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import cv2

np.random.seed(1)
n = 10
l = 256
im = np.zeros((l, l))
points = l*np.random.random((2, n**2))
im[(points[0]).astype(np.int), (points[1]).astype(np.int)] = 1
im = ndimage.gaussian_filter(im, sigma=l/(4.*n))
mask = im > im.mean()

label_im, nb_labels = ndimage.label(mask)
print(nb_labels)
plt.figure(figsize=(9,3))

plt.subplot(131)
plt.imshow(im)
plt.axis('off')
plt.subplot(132)
plt.imshow(mask, cmap=plt.cm.gray)
plt.axis('off')
print(np.shape(label_im))

frame_anterior = cv2.cvtColor(label_im, cv2.COLOR_BGR2GRAY)
print(np.shape(label_im))
mask = frame_anterior
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
mayor_contorno = max(contours, key = cv2.contourArea)
momentos = cv2.moments(mayor_contorno)
cx = float(momentos['m10']/momentos['m00'])
cy = float(momentos['m01']/momentos['m00'])

punto_elegido = np.array([[[cx,cy]]],np.float32)
print(punto_elegido)

plt.show()