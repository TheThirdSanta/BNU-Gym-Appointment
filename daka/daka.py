#代码中所有路径都需要修改成你自己的路径
#我开的网页浏览器是edge，如果要用谷歌或者火狐请自行下载对应的插件，安装过程自行百度
#在此感谢黄梓峻同学为验证码识别做出的卓越贡献
#感谢段欣然同学为网页操作部分做出的卓越贡献
# -*- coding: utf-8 -*-
import os
from PIL import Image
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
driver = webdriver.Edge(executable_path = "C:\CONDA\msedgedriver.exe")
#窗口最大化方便后面的验证码图片生成
driver.maximize_window()
driver.get("http://172.16.213.7/gymbook/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id=2&viewType=m")
driver.implicitly_wait(1)
#""内输入数字京师学号和密码
name = driver.find_element_by_id("un").send_keys("202011081027")

password = driver.find_element_by_id('pd').send_keys("jerry777")


element = driver.find_element_by_id('index_login_btn')
element.click()
#弹窗等待同意按钮元素出现，可以修改一下加一个判定
#sleep(1)
ele = driver.find_element_by_xpath('//*[@id="attentionModal"]/div[3]/button')
ele.click()

yu= driver.find_element_by_xpath('//*[@id="tabs"]/ul/li[3]/a')
yu.click()

#跳转至羽毛球预约界面
first = driver.find_element_by_xpath('//*[@id="box-0"]/div/div/div[5]/a[4]')
first.click()
driver.switch_to_frame('overlayView')

#预约的下午两点到三点小综合1和2的场，时间可以自己改，如果找不到那就是已经被人抢了
driver.find_element_by_xpath('//*[@id="resourceTd_50407"]').click()
driver.find_element_by_xpath('/html/body/table/tbody/tr[8]/td[10]').click()
driver.find_element_by_xpath('//*[@id="resourceTd_50405"]').click()
driver.find_element_by_xpath('//*[@id="resourceTd_50455"]').click()

#sleep(1)
driver.switch_to.default_content()
#点击预约按钮
yuyue = driver.find_element_by_xpath('//*[@id="box-0"]/div/div/div[6]/span/a/span')
yuyue.click()
#sleep(1)
#生成验证码图片
img = driver.find_element_by_xpath('//*[@id="kaptchaImage"]')
driver.save_screenshot("C:/Users/78793/Desktop/1.jpg")
location = img.location
size = img.size
rangle = (int(location['x']*1.25), int(location['y']*1.25), (int(location['x'] + size['width'])*1.25),
          (int(location['y'] + size['height']))*1.25)
i = Image.open("C:/Users/78793/Desktop/1.jpg")
frame4 = i.crop(rangle)
frame4.save("C:/Users/78793/Desktop/save.png")
#最终结果为result，若为-1则表示识别失败，需要换一个验证码
#验证码识别过程
global red
def sign(x):
    if x<0:
        return -1
    elif x==0:
        return 0
    else:
        return 1
    
def get(x,y):
    color=img.getpixel((x,y))
    if color[-1]==color[0] and color[-1]==color[1]:
        return(color[-1])
    elif color[1]==255:
        return -2
    elif color[0]==255:
        return -1
    else:
        print('color error')

def mod(x,y,c):
    if c==-1:
        img.putpixel((x,y),(255,0,0))
        return
    if c==-2:
        img.putpixel((x,y),(0,255,0))
        return
    img.putpixel((x,y),(c,c,c))

def isnarrow(x,y):
    if x==0 or x==199 or y==0 or y==49:
        return 0
    if get(x,y+1)>80 and get(x,y-1)>80:
        return 1
    if get(x+1,y)>80 and get(x-1,y)>80:
        return 1
    return 0

def length(x,y):
    lenth=[];plus=0;red_flag=0
    if x>45:
        red_flag=1
    for k in range(-30,30):
        t=k/20;p=0;n=0
        while get(x+p,int(y+t*p))<80:
            if red_flag==0:
                for rp in red:
                    goal=int((x+p-rp[0])**2+(y+t*p-rp[1])**2)
                    if goal<4:
                        activate=((x-rp[0])**2+(y+t*p-rp[1])**2)**(1/2)
                        plus+=int(200/(activate+1)**(1/2))
                        if plus>52:
                            red_flag=1
                        
            p+=1
            if x+p==199 or int(y+t*p)==50  or x+p==0 or int(y+t*p)==0:
                break
        while get(x-n,int(y-t*n))<80:
            if red_flag==0:
                for rp in red:
                    goal=int((x-n-rp[0])**2+(y-t*n-rp[1])**2)
                    if goal<4:
                        activate=((x-rp[0])**2+(y-rp[1])**2)**(1/2)
                        plus+=int(200/(activate+1)**(1/2))
                        if plus>52:
                            red_flag=1
                    
            n+=1
            if x-n==199 or int(y-t*n)==50  or x-n==0 or int(y-t*n)==0:
                break
        lenth.append([(p+n)*((1+t**2)**(1/2)),t])
    lenth=max(lenth,key=lambda e:e[0])
    return (lenth[0]+plus,lenth[1])
        
def main():
    global img,red,wait_lst,testglass,already_lst
    red=[];wait_lst=[];testglass=[];already_lst=[]
    img=Image.open("C:/Users/78793/Desktop/save.png")
    img= img.convert('RGB')
    for x in range(200):
        for y in range(50):
            if x==0 or x==199 or y==0 or y==49:
                mod(x,y,255);continue
            color=get(x,y)
            if color>160:
                mod(x,y,255)
                
    for y in range(50):
        for x in range(20):
            color=get(x,y)
            if color<50:
                if get(x-1,y)>0 and get(x,y-1)>0:
                    red.append((x,y))
    testglass=[]                
    for x in range(200):
        for y in range(50):
            if get(x,y)==0 and isnarrow(x,y):
                wait_lst.append([x,y]);testglass.append((x,y))
    distance_list=[]
    for xt in range(200):
        for yt in range(50):
            if get(xt,yt)<60:
                distance=0
                lenth,k=length(xt,yt)
                if lenth>35:
                    if lenth>50:
                        wait_lst.append([xt,yt])
                    for gp1 in testglass:
                        distance+=(abs(k*(gp1[0]-xt)+yt-gp1[1])/((1+k**2)**(1/2)))**(1/10)
                    distance_list.append([distance,xt,yt])
    distance_list.sort()
    k=int(len(distance_list)*0.5)
    for num in range(k):
        wait_lst.append([distance_list[num][1],distance_list[num][2]])
        
    for wp in wait_lst:
        white=0;flag=0
        if wp[0]>=197 or wp[0]<=2 or wp[1]<=2 or wp[1]>=47:
            flag=1
        else:
            for right in [-3,-2,-1,1,2,3]:
                for down in [-3,-2,-1,1,2,3]:
                    white+=get(wp[0]+right,wp[1]+down)/(right**2+down**2)**(2)
        if white>50 or flag==1:
            already_lst.append([wp[0],wp[1]])
        if white>150:
            try:
                for r2 in [-1,0,1]:
                    for d2 in [-1,0,1]:
                        already_lst.append([wp[0]+r2,wp[1]+d2])
            except:
                pass
    for ap in already_lst:       
        mod(ap[0],ap[1],255)
    img.save("C:/Users/78793/Desktop/save1.png")
        
    
    import ddddocr
    ocr = ddddocr.DdddOcr()
    with open("C:/Users/78793/Desktop/save1.png",'rb') as f:
        img_bytes = f.read()
    return (ocr.classification(img_bytes))

        
        
    
if __name__=='__main__':
    try:
        res=main()
        res=res[:-1]
        str1='';symbol='0';str2=''
        if not res[-1].isdigit():
            if res[-1]=='F' or res[-1]=='上':
                res=res[:-1]+'1'
            else:
                res=res[:-1]
        if res[0]=='H' or res[0]=='h':
            res='1+'+res[1:]
        if res[1]=='H' or res[1]=='h':
            res=res[0]+'1+'+res[2:]
        flag=0
        pl=len(res)
        for indx in range(pl):
            if res[indx]=='+':
                flag=1
                res0=int(res[:indx])+int(res[indx+1:])
                if pl==3 and (('4' in res )or ('7' in res)):
                    res0+=10
                res=res0
                break
        if flag==0:
            if len(res)==3:
                res=int(res[:2])-int(res[2])
            elif len(res)==4:
                res0=int(res[:2])-int(res[2:])
                if res0<0:
                    res0=int(res[:2])+int(res[3])
                res=res0
                    
            elif len(res)==5:
                res=int(res[:2])-int(res[3:])
            elif len(res)==2:
                res=int(res[0])-int(res[1])+10
        if str(res).isdigit():       
            result=res
        else:
            result=-1
    except:
        result=-1
 #打印结果   
    print(result)

#验证码填写并点击确认
driver.find_element_by_xpath('//*[@id="checkcodeuser"]').send_keys(result)
#sleep(1)

driver.find_element_by_xpath('//*[@id="contactCompanion"]/div[3]/a[1]').click()
sleep(20)