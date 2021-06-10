from  PIL import Image
import os

def transparent_back(img):
    img = img.convert('RGBA')
    L, H = img.size
    color_0 = img.getpixel((2,2))
    for h in range(H):
        for l in range(L):
            dot = (l,h)
            color_1 = img.getpixel(dot)
            if color_1 ==color_0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot,(0,0,0,0))
    return img
 
'''
img=Image.open('1.png')
img=transparent_back(img)
img.save('round2.png')
'''
l=[]
for a,b,c in os.walk('.'):
	#print(a,b,c)
	if b==[]:		
		l+=[os.path.join(a,i) for i in c if os.path.splitext(i)[-1]=='.png']
#print(l)
num=len(l)
print(num)
n=0
for i in l:
	n+=1
	print('正在进行',i,n,'共',num)
	img=Image.open(i)
	img=transparent_back(img)
	img.save(i)
	









