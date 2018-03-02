#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import math
import os
import sys

instance_type=['d2','g2','m4','r3']
#instance_type=['m4','r3','d2']
#instance_type=['type1','type2']
spot_price=[0.0,0.0,0.0,0.0]
#spot_price=[0.04,0.025]
#time=[0.0,0.0]
availablility_zone=['a','a','a','a']
zones_d2=['a','b','c','d','e','f']
zones_g2=['d','e']
zones_m4=['e','f']
zones_r3=['a','c','d']
instance_number=[0,0,0,0]
times=[1,1,1,1]
def predict_price(spot_type):
	cmd1="python extract_price.py"
	os.system("%s %s"%(cmd1,spot_type))
	cmd2="./run2.sh"
	os.system("%s %s"%(cmd2,spot_type))

def provision():
	
	jobnumber=input('the total number of jobs\n')
	for num in range(jobnumber):
		t=0
		job=input('the number of job\n')
		performance_goal=input('performance goal\n')
		instance_number=[0,0,0,0]

		
		#instance number
		
		for ins_type in instance_type:
			#print ins_type
			times=[1,1,1,1]
			n=0
			#with open('eventlog/AL/AL_75G/'+ins_type+'/Flint_prediction_'+ins_type+'_'+str(job)+'.txt','r')as f:
			#with open('eventlog/Sort/'+ins_type+'/Sort_prediction_'+str(job)+'_sample1.3.txt','r') as f:
			#with open('eventlog/AL/AL_75G/GCE/'+ins_type+'/prediction_'+ins_type+'_'+str(job)+'.txt','r')as f:
			with open('eventlog/PageRank/'+ins_type+'/prediction_'+ins_type+'_'+str(job)+'.txt','r') as f:
				for line in f.readlines():
					#	Zprint line
					if float(performance_goal)>=float(line):
						#time[t]=math.ceil(float(line)/60000)
						times[t]=math.ceil(float(line)/3600000)
						instance_number[t]=n+2
						break
					n+=1
			f.close()	
			t+=1
		

		#predict price
		
		for ins_type in instance_type:
			predict_price(ins_type)
		
		#calculate the minimum price
		
		
		t=-1
		for ins_type in instance_type:
			#min_price=9999
			t+=1
			
			if t==0:
				zones=zones_d2
			elif t==1:
				zones=zones_g2
			elif t==2:
				zones=zones_m4
			elif t==3:
				zones=zones_r3
			'''
			if t==0:
				zones=zones_m4
			elif t==1:
				zones=zones_r3
			elif t==2:
				zones=zones_d2
			'''
			price = 0
			for j in zones:
				with open('eventlog/AL/AL_75G/'+ins_type+'/2-'+j+'-pred.csv')as f:
				#with open('eventlog/Sort/'+ins_type+'/2-'+j+'-pred.csv')as f:
					for line in f.readlines():
						price=price+float(line)
			avg_price=price/len(zones)
			
			spot_price[t]=avg_price
		

		#provision plan
		
		t=-1
		min_overhead=99999
		for ins_type in instance_type:
			t+=1
			monetary_overhead=float(instance_number[t])*float(spot_price[t])*times[t]
			print monetary_overhead
			if monetary_overhead==0:
				continue
			if min_overhead>monetary_overhead:
				min_overhead=monetary_overhead
				final=ins_type
				T=t
		


		print instance_number
		#print times
		#print spot_price
		#print availablility_zone
		print final,instance_number[T],min_overhead
		
provision()