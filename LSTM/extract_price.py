# -*- coding:utf-8 -*-
import re
import time
import sys
import os
'''
Created on 2017年7月30日
'''
#http://bbs.csdn.net/topics/391978633
#array = [0,None]

in_files = ['useast1a.txt','useast1b.txt','useast1c.txt','useast1d.txt','useast1e.txt','useast1f.txt']
def extract_price():
    startTime = "2017-10-30 12:00:00"
    endTime = "2017-11-30 12:00:00"

    #转换成时间数组
    startTimeArray = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    startTimeInt = time.mktime(startTimeArray)

    #转换成时间数组
    endTimeArray = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")
    endTimeInt = time.mktime(endTimeArray)

    value = endTimeInt - startTimeInt
    #print(startTimeInt,endTimeInt)
    #print(value)

    #结果存储
    resultSum = int(value/(5*60) + 1) 
    #print(resultSum)

    #存储原始数据
    price = [[0, 0] for _ in range(sum)] 
    #存储处理的数据（将字符串处理成时间格式 "%Y-%m-%d %H:%M:%S"）
    price2 = [[0, 0] for _ in range(sum)]
    i = 0
    file = open(filename)
    for line in file:
        price[sum-i-1][0] = re.split('\t|\n',line)[0]
        price[sum-i-1][1] = re.split('\t|\n',line)[1]
    #    print(sum-i-1,price[sum-i-1][0],price[sum-i-1][1])
        i = i + 1
    #print(price)
    for j in range(0,i):
    #    print(price[j])
        price2[j][1] = price[j][1][0:19].replace('T',' ')
        price2[j][0] = price[j][0]
    #print(price2)
    #time1 = time.strftime('%Y-%m-%d %T',time.localtime(time.time()-24*60*60))
    #print(time1)
    #print(price2[0][1],"======")
    #print(price2[1][1],"======")
    #timeArray0 = time.strptime(price2[0][1], "%Y-%m-%d %H:%M:%S")
    #timeArray1 = time.strptime(price2[1][1], "%Y-%m-%d %H:%M:%S")
    #timeStamp0 = int(time.mktime(timeArray0))
    #timeStamp1 = int(time.mktime(timeArray1))
    #print(timeStamp0,timeStamp1)
    #time3 = timeStamp1 - timeStamp0
    #print(time3)
    #print(time.strftime('%Y-%m-%d %T',time.localtime(time.time()-24*60*60)) )

    #timestamp = 1462451334
    ##转换成localtime
    #time_local = time.localtime(timestamp)
    ##转换成新的时间格式(2016-05-05 20:28:54)
    #dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    #print(dt)



    result = [[0, 0] for _ in range(resultSum)] 

    k = 0
    #循环输入以5分钟为时间间隔的时间
    for i in range(0,resultSum):
        #转换成localtime
        
        startTime2 = time.localtime(startTimeInt)
        #转换成新的时间格式(2016-05-05 20:28:54)
        startTime3 = time.strftime("%Y-%m-%d %H:%M:%S",startTime2)
    #    print(startTime3)
        result[i][1] = startTime3
        
        for j in range(k,sum):
            timeArray0 = time.strptime(price2[j][1], "%Y-%m-%d %H:%M:%S")
            timeStamp0 = int(time.mktime(timeArray0))
            tmp = startTimeInt - timeStamp0
            if tmp >= 0:
                continue
            else:
                #print i
                result[i][0] = price2[j-1][0]
                #codelst = [result[i][0],'\t',result[i][1],'\n'] 
                codelst = [result[i][0],'\n'] 
                fileWrite.writelines(codelst)
                k = j - 1
                break
        startTimeInt = startTimeInt + 5*60
    #print(result)

if __name__=='__main__':
    args=sys.argv
    sum = 0
    #filename = args[1] # txt文件目录
    dir = args[1]
    for i in range(6):
        #print dir
        #print dir+'result-'+in_files[i]
        if os.path.exists(os.path.join('eventlog/AL/AL_75G/',dir,in_files[i])):
            sum=0
            filename=os.path.join('eventlog/AL/AL_75G/',dir,in_files[i])
            fileWrite=open('eventlog/AL/AL_75G/'+dir+'/result-'+in_files[i],'w+')
            for line in open(filename):
                sum =sum +1
            extract_price()
    #fileWrite = open('result-'+args[1],'w+')  
    #for line in open(filename):
        #sum = sum + 1
    #extract_price()


