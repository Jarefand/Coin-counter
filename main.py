import cv2

import numpy as np

#wczytywanie obrazu
img = cv2.imread("zdj1.jpg")
#zmniejszenie zdjecia
img = cv2.pyrDown(img)
img = cv2.pyrDown(img)



cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


pimg = cv2.GaussianBlur(cimg,(5,5),0)


circles = cv2.HoughCircles(pimg,cv2.HOUGH_GRADIENT,1,35,param1=280,param2=50,minRadius=0,maxRadius=0)

font = cv2.FONT_HERSHEY_SIMPLEX
color = (255,0,0)
fontScale = 1


img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

circles = np.uint16(np.around(circles))

br = []
sr = []
re = []


for i in circles[0,:]:
    mask = np.full((img.shape[0], img.shape[1]), 0, np.uint8)
    cv2.circle(mask, (i[0], i[1]), i[2], (255, 255, 255), -1)
    metric = list(cv2.mean(img_hsv, mask))

    if metric[1] > 52:
        br.append([i[0],i[1],i[2], 0])
    elif metric[1] < 20:
        sr.append([i[0], i[1], i[2], 0])
    else:
        re.append([i[0], i[1], i[2], 0])


brazowe = np.array(br)
srebrne = np.array(sr)
reszta = np.array(re)

bmin = min(brazowe[:,2])


for i in range(len(reszta[:,2])):
    if reszta[i,2] > (0.95*bmin*1.387) and reszta[i,2] < (1.05*bmin*1.387):
        reszta[i,3]= 200
    elif reszta[i,2] > (0.95*bmin*1.548) and reszta[i,2] < (1.05*bmin*1.548):
        reszta[i,3] = 500

for i in range(len(brazowe[:,2])):
    if brazowe[i,2] > (0.95*bmin) and brazowe[i,2] < (1.05*bmin):
        brazowe[i,3]= 1
    elif brazowe[i,2] > (0.95*bmin*1.129) and brazowe[i,2] < (1.05*bmin*1.129):
        brazowe[i, 3] = 2
    elif brazowe[i,2] > (0.95*bmin*1.258) and brazowe[i,2] < (1.05*bmin*1.258):
        brazowe[i, 3] = 5

for i in range(len(srebrne[:,2])):
    if srebrne[i,2] > (0.95*bmin*1.065) and srebrne[i,2] < (1.05*bmin*1.065):
        srebrne[i,3]= 10
    elif srebrne[i,2] > (0.95*bmin*1.194) and srebrne[i,2] < (1.05*bmin*1.194):
        srebrne[i, 3] = 20
    elif srebrne[i,2] > (0.95*bmin*1.323) and srebrne[i,2] < (1.05*bmin*1.323):
        srebrne[i, 3] = 50
    elif srebrne[i,2] > (0.95*bmin*1.484) and srebrne[i,2] < (1.05*bmin*1.484):
        srebrne[i, 3] = 100

monety = brazowe
monety = np.append(monety,srebrne, axis = 0)
monety = np.append(monety,reszta, axis = 0)



for i in monety:
    # rysowenie obrysow
    cv2.circle(img,(i[0],i[1]),i[2],(0,0,255),2)
    # rysowanie wartosci
    cimg = cv2.putText(img,str(i[3]/100),(i[0]-25,i[1]),font,fontScale,color,2, cv2.LINE_AA)

suma=0
for i in monety[:,3]:
    suma=i+suma

print("Suma monet ze zdjęcia wynosi: ",suma/100,"zł")





cv2.imshow("monetkif",img)
cv2.waitKey(0)
cv2.destroyAllWindows()