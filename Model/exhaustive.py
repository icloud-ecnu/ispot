#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import copy
import datetime
import math

Job ={}

#return nodes whose indegree is 0
def indegree0(v,e):
	if v==[]:
		return None
	tmp = v[:]

	for i in e:
		if i[1] in tmp:
			tmp.remove(i[1])

	if tmp==[]:
		return -1

	for t in tmp:
		i=0
		for i in range(len(e)):
			for m in e[i]:
				if t==m:
					e[i]='del'

	if e:
		eset=set(e)
		eset.remove('del')
		e[:]=list(eset)
	if v:
		for t in tmp:
			v.remove(t)
	return tmp

def processinput(Stage,Size,v1,e1):

	first=indegree0(v1,e1)
	max_ratio=0 #the largest partition number of upstream RDD
	for i in first:
		input_size=input('input the data size of stage %d\n'%i)
		size=Stage.get(i).get('Read')
		input_ratio=input_size*1.0/size
		if input_ratio>max_ratio:
			max_ratio=input_ratio
		if Stage[i].has_key('Write'):
			Stage[i].pop('Write')
		Stage[i]['Read']=input_size
		Stage[i]['Write']=Stage[i]['Read']*Stage[i]['Rpi']

	for stage in Stage:

		if stage==0:

			Stage[stage]['CheckSize']=int(Size[5])*max_ratio*2
		elif stage==1:
			Stage[stage]['CheckSize']=int(Size[8])*max_ratio*2
		elif stage==24:
			Stage[stage]['CheckSize']=int(Size[66])*max_ratio*2
		elif stage==25:
			Stage[stage]['CheckSize']=int(Size[51])*max_ratio*2
		elif stage==27:
			Stage[stage]['CheckSize']=int(Size[56])*max_ratio*2
		elif stage==28:
			Stage[stage]['CheckSize']=int(Size[61])*max_ratio*2
	for stage in Stage:
		if stage in first:
			continue
		else:
			stage_input=0
			if Stage[stage].has_key('Write'):
				Stage[stage].pop('Write')
			for j in Stage[stage]['ParentIDs']:
				stage_input=stage_input+Stage[j]['Write']
			Stage[stage]['Read']=stage_input
			if Stage[stage].has_key('Rpi'):
				Stage[stage]['Write']=Stage[stage]['Read']*Stage[stage]['Rpi']



def topSort(v3,e3,Stage,core,B_d,B_n,n_sport,assigned_rpi,assigned_stagetime_ratio,Trep,MTTF):
#def topSort(v,e,Stage,core,B_d,B_n,n_sport):
	
	v1=copy.deepcopy(v3)
	e1=copy.deepcopy(e3)
	first=indegree0(v1,e1)
	BlockTime=0
	CheckpointTime=0
	RestorationTime=0
	MaxStageTime=0
	Upper=0
	Lower=0
	S=len(v3)
	while True:
		nodes=indegree0(v3,e3)
		if nodes==None:
			break
		if nodes==-1:
			print('there is a circle')
			return None

		StageTime=0
		ProcessTime=0 
		ShuffleTime=0
		SerialTime=0  
		GCTime=0
		p_i=0  #number of partitions in the same parallelism
		a_i=0 
		if len(nodes)>1:#parallelism
			p_i=len(nodes)
			a_i=core*n_sport*1.0
			for stage in nodes:
				ProcessTime=0
				ShuffleTime=0
				SerialTime=0
				GCTime=0

				ProcessTime=Stage[stage]['Read']*1.0/(Stage[stage]['Process Rate'])

				if Stage[stage].has_key('Serialization'):
					SerialTime=SerialTime+Stage[stage]['Serialization']
				if Stage[stage].has_key('Deserialization'):
					SerialTime=SerialTime+Stage[stage]['Deserialization']
				if Stage[stage].has_key('GCTime'):
					GCTime=GCTime+Stage[stage]['GCTime']
				ShuffleMaxRead=0
				if stage in first:#no ShuffleRead        
					ShuffleRemoteRead=Stage[stage]['Read']*1.0/B_n                                          #shuffletime
					ShuffleWrite=Stage[stage]['Write']*1.0/B_d#no read
					ShuffleTime=(ShuffleRemoteRead+ShuffleWrite)*1000/(n_sport*core) 
				else:
					ShuffleLocalRead=Stage[stage]['Read']*1.0/(B_d*n_sport)
					ShuffleRemoteRead=Stage[stage]['Read']*(n_sport-1)*1.0/(B_n*n_sport)
					if ShuffleRemoteRead>ShuffleLocalRead:
						ShuffleMaxRead=ShuffleRemoteRead
					else:
						ShuffleMaxRead=ShuffleLocalRead
					ShuffleWrite=Stage[stage]['Write']*1.0/B_d
					
					ShuffleTime=ShuffleWrite+ShuffleMaxRead
					ShuffleTime=ShuffleTime*1000/(n_sport*core) 

				StageTime=ProcessTime/a_i+SerialTime+ShuffleTime+GCTime
				Stage[stage]['StageTime']=StageTime
				
				if MaxStageTime<StageTime:
					MaxStageTime=StageTime

				if Stage[stage]['Rpi']>=assigned_rpi or Stage[stage]['Stage Ratio']>=assigned_stagetime_ratio:
					if B_n<B_d:
						tmp=B_n
					else:
						tmp=B_d
					Stage[stage]['Checkpoint']=(Stage[stage]['CheckSize']*1.0/tmp)*1000/(n_sport*core)
					CheckpointTime=CheckpointTime+Stage[stage]['Checkpoint']
					
				if Stage[stage].has_key('Checkpoint'):
					Stage[stage]['Restoration']=Stage[stage]['Checkpoint']
					
				elif stage == 24 or stage == 25 or stage ==27:
					Stage[stage]['Restoration']=StageTime	
					
				else:
					maxRestoration=0
					for parentstage in Stage[stage]['ParentIDs']:
						if maxRestoration<Stage[parentstage]['Restoration']:
							maxRestoration=Stage[parentstage]['Restoration']
					Stage[stage]['Restoration']=maxRestoration+StageTime
				RestorationTime=RestorationTime+Stage[stage]['Restoration']
				Upper=Upper+StageTime
		  	BlockTime=BlockTime+MaxStageTime	  	

		else:
		  	stage=nodes[0]
		  	a_i=core*n_sport

		  	ProcessTime=0
			ShuffleTime=0
			SerialTime=0
			GCTime=0
		  	
		  	ProcessTime=Stage[stage]['Read']*1.0/(Stage[stage]['Process Rate'])

			if Stage[stage].has_key('Serialization'):
				SerialTime=SerialTime+Stage[stage]['Serialization']
			if Stage[stage].has_key('Deserialization'):
				SerialTime=SerialTime+Stage[stage]['Deserialization']
			if Stage[stage].has_key('GCTime'):
				GCTime=GCTime+Stage[stage]['GCTime']
			if stage==0:
				ShuffleLocalRead=0
				ShuffleRemoteRead=Stage[stage]['Read']*1.0/B_n
			else:
				ShuffleLocalRead=Stage[stage]['Read']*1.0/(B_d*n_sport)
				ShuffleRemoteRead=Stage[stage]['Read']*(n_sport-1)*1.0/(B_n*n_sport)
			if ShuffleRemoteRead>ShuffleLocalRead:
				ShuffleMaxRead=ShuffleRemoteRead
			else:
				ShuffleMaxRead=ShuffleLocalRead
			ShuffleWrite=0
			if  Stage[stage].has_key('Write'):
				ShuffleWrite=Stage[stage]['Write']*1.0/B_d

			ShuffleTime=ShuffleWrite+ShuffleMaxRead
			ShuffleTime=ShuffleTime*1000/(n_sport*core)
			StageTime=ProcessTime/a_i+SerialTime+ShuffleTime+GCTime
			
			if (Stage[stage].has_key('Rpi') and Stage[stage]['Rpi']>=assigned_rpi)or Stage[stage]['Stage Ratio']>=assigned_stagetime_ratio:
				if B_n<B_d:
					tmp=B_n
				else:
					tmp=B_d
				Stage[stage]['Checkpoint']=(Stage[stage]['CheckSize']*1.0/tmp)*1000/(n_sport*core)
				CheckpointTime=CheckpointTime+Stage[stage]['Checkpoint']
					
			if Stage[stage].has_key('Checkpoint'):
					Stage[stage]['Restoration']=Stage[stage]['Checkpoint']
			else:
				maxRestoration=0
				for parentstage in Stage[stage]['ParentIDs']:
					if maxRestoration<Stage[parentstage]['Restoration']:
						maxRestoration=Stage[parentstage]['Restoration']
				Stage[stage]['Restoration']=maxRestoration+StageTime
			RestorationTime=RestorationTime+Stage[stage]['Restoration']
		
			if MaxStageTime<StageTime:
				MaxStageTime=StageTime
			BlockTime=BlockTime+StageTime
			Upper=Upper+StageTime
	

	Tupper=Upper+CheckpointTime+math.ceil(Upper/MTTF)*(Trep+RestorationTime*1.0/S)
	Tj=BlockTime+CheckpointTime+math.ceil(BlockTime/MTTF)*(Trep+RestorationTime*1.0/S)
	#print BlockTime,CheckpointTime,math.ceil(BlockTime/MTTF),Trep+RestorationTime*1.0/S
	Tlower=MaxStageTime+CheckpointTime+math.ceil(MaxStageTime/MTTF)*(Trep+RestorationTime/S)
	#print ('check',CheckpointTime)
	#print ('restore',RestorationTime/S)
	#print Tupper,Tj,Tlower
	return Tj
	#return Upper,BlockTime,MaxStageTime

RDD=[5,8,66,51,56,61]
Size={5:int(0),8:int(0),66:int(0),51:int(0),56:int(0),61:int(0)}

def CheckRDDSize(file):
	i=0
	str3=open(file).read()
	length=len(str3)
	while i<length:
		i=str3.find('"SparkListenerTaskEnd",',i)
		if i==-1:
			break
		j=i
		stack=['{']
		while j<length:
			if str3[j]=='{':
				stack.append('{')
			elif str3[j]=='}':
				stack.pop()
			j=j+1
			if not stack:
				break
		if i<length and j<length:
			obj=json.loads('{"Event": '+str3[i:j])
		if obj.has_key('Task Metrics'):
			RDDobj=obj['Task Metrics']['Updated Blocks']	
			for item in RDDobj:
				RDDnumber=item['Block ID']
				if RDDnumber[0:4]=='rdd_':
					size=int(item['Status']['Disk Size'])
					#print size
					if RDDnumber[4:6]=='5_':
						Size[5]+=size
					elif RDDnumber[4:6]=='8_':
						Size[8]+=size
					elif RDDnumber[4:6]=='66':
						Size[66]+=size
					elif RDDnumber[4:6]=='51':
						Size[51]+=size
					elif RDDnumber[4:6]=='56':
						Size[56]+=size
					elif RDDnumber[4:6]=='61':
						Size[61]+=size
		i=i+1
	return Size



def extract(str2,file):
	#n_sport=input('the number of VMs in the Cluster\n')
	core=input('the number of cores in a VM\n')
	B_d=input('the disk bandwidth of VM\n')
	B_n=input('the network bandwidth of VM\n')
	Trep=input('Replacement Time\n')
	MTTF=input('Mean Time to Failure\n')
	begin = datetime.datetime.now()
	length=len(str2)
	Size={}
	Size=CheckRDDSize(file)
	i=0
	count=0
	#extract the stage IDs of each job
	while i<length: 
		i=str2.find('"SparkListenerJobStart",',i)
		JobInfo={}
		if i==-1:
			break
		j=i
		stack=['{']
		while j<length:
			if str2[j]=='{':
				stack.append('{')
			elif str2[j]=='}':
				stack.pop()
			j=j+1
			if not stack:
				break
		if i<length and j<length:
			obj=json.loads('{"Event": '+str2[i:j])
			#print 'here'
			#print obj
			JobInfo['Submission']=obj['Submission Time']
			JobInfo['Stages']=obj['Stage IDs']
			Job[obj['Job ID']]=JobInfo
			count=count+1
		i=i+1
	i=0
	while i<length: 
		i=str2.find('"SparkListenerJobEnd",',i)
		#print i
		if i==-1:
			break
		j=i
		stack=['{']
		while j<length:
			if str2[j]=='{':
				stack.append('{')
			elif str2[j]=='}':
				stack.pop()
			j=j+1
			if not stack:
				break
		if i<length and j<length:
			obj=json.loads('{"Event": '+str2[i:j])
			#print 'here'
			#print obj
			Job[obj['Job ID']]['Completion']=obj['Completion Time']
			Job[obj['Job ID']]['Time']=Job[obj['Job ID']]['Completion']-Job[obj['Job ID']]['Submission']
			count=count+1
		i=i+1

	k=0 #job id
	while k<5:

		Stage={}
		v=[]
		e=[]
		i=0
		#if k==0 or k==4:
		if k==0:	
			while i<length:
				i=str2.find('"SparkListenerStageCompleted",', i)
				if i==-1:
					break;
				j=i
				stack=['{']
				while j<length:
					if str2[j]=='{':
						stack.append('{')
					elif str2[j]=='}':
						stack.pop()
					j=j+1
					if not stack:
						break

				if i<length and j<length:
					obj=json.loads('{"Event": '+str2[i:j])
					if(obj['Stage Info']['Stage ID']in Job[k]['Stages']):
						

						StageInfo={}
						
						StageInfo['Read']=0
						StageInfo['Remote']=0
						StageInfo['Local']=0
						StageInfo['Write']=0
						StageInfo['ResultSize']=0
						StageInfo['GCTime']=0
						

						StageInfo['TaskNumber']=obj['Stage Info']['Number of Tasks']
						StageInfo['ParentIDs']=obj['Stage Info']['Parent IDs']
						StageInfo['StageComp']=obj['Stage Info']['Completion Time']-obj['Stage Info']['Submission Time']
						StageInfo['Stage Ratio']=StageInfo['StageComp']*1.0/Job[k]['Time']
						acc=obj['Stage Info']['Accumulables']

						v.append(obj['Stage Info']['Stage ID'])
						for a in obj['Stage Info']['Parent IDs']:
							if a in v:
								e.append((a,obj['Stage Info']['Stage ID']))
						for item in acc:
							if item['Name']=='internal.metrics.input.bytesRead':
								StageInfo['Read']+=item['Value']
							elif item['Name'] == 'internal.metrics.shuffle.read.remoteBytesRead':
								StageInfo['Read']+=item['Value']
								StageInfo['Remote']=item['Value']
							elif item['Name'] == 'internal.metrics.shuffle.read.localBytesRead':
								StageInfo['Read']+=item['Value']
								StageInfo['Local']=item['Value']
							elif item['Name'] == 'internal.metrics.shuffle.write.bytesWritten':
								StageInfo['Write']=item['Value']
							elif item['Name'] == 'internal.metrics.resultSerializationTime':
								StageInfo['Serialization']=item['Value']
							elif item['Name'] == 'internal.metrics.executorDeserializeTime': 
								StageInfo['Deserialization']=item['Value']
							elif item['Name'] == 'internal.metrics.jvmGCTime':
								StageInfo['GCTime']=item['Value']
							elif item['Name'] == 'internal.metrics.executorRunTime':
								StageInfo['RunTime']=item['Value']

						LocalTime=0
						RemoteTime=0
						WriteTime=0
						if obj['Stage Info']['Stage ID']==24 or obj['Stage Info']['Stage ID']==25 or obj['Stage Info']['Stage ID']==27 or obj['Stage Info']['Stage ID']==0:
							LocalTime=0
							RemoteTime=StageInfo['Read']*1.0/B_n
						else: 
							LocalTime=StageInfo['Read']*1.0/B_d
							#RemoteTime=StageInfo['Read']*(n_sport-1)*1.0/(B_n*n_sport)
						WriteTime=StageInfo['Write']*1.0/B_d
						Shuffle=(LocalTime+RemoteTime+WriteTime)*1000/core
						StageInfo['Process Rate']=(StageInfo['Read']*1.0)/(StageInfo['RunTime']-Shuffle)

						if StageInfo['Write']!=0 and StageInfo['Read']!=0:
							StageInfo['Rpi']=StageInfo['Write']*1.0/StageInfo['Read']

						
						if StageInfo.has_key('Local'):
							StageInfo.pop('Local')
						if StageInfo.has_key('Remote'):
							StageInfo.pop('Remote')
						

						Stage[obj['Stage Info']['Stage ID']]=StageInfo

				i=i+1
			if k == 4:
				if Stage[25]['StageComp']<Stage[27]['StageComp']:
					Stage[27]['Stage Ratio']=(Stage[27]['StageComp']-Stage[25]['StageComp'])/Job[k]['Time']
				else:
					Stage[27]['Stage Ratio']=(Stage[25]['StageComp']-Stage[27]['StageComp'])/Job[k]['Time']

			
			v1=copy.deepcopy(v)
			e1=copy.deepcopy(e)
			processinput(Stage,Size,v1,e1)
			print Stage

			
			assigned_rpi=input('the process ratio\n')
			assigned_stagetime_ratio=input('the stage time ratio\n')
			for n_sport in range(2,11):
				v3=copy.deepcopy(v)
				e3=copy.deepcopy(e)
				res=topSort(v3,e3,Stage,core,B_d,B_n,n_sport,assigned_rpi,assigned_stagetime_ratio,Trep,MTTF)

			#res=topSort(v,e,Stage,core,B_d,B_n,n_sport)
				if k==0:
					#with open(file[:22]+'prediction_'+file[-9:-7]+'_0.txt','a+') as f:
					with open(file[:29]+'prediction_'+file[23:28]+'_0.txt','a+') as f:
					#with open(file[:21]+'prediction_'+file[-20:-18]+'_0.txt','a+') as f:
						f.write(str(res))
						f.write('\n')
				elif k==4:
					with open(file[:29]+'prediction_'+file[23:28]+'_4.txt','a+') as f:
					#with open(file[:22]+'prediction_'+file[-9:-7]+'_4.txt','a+') as f:
						f.write(str(res))
						f.write('\n')	
			end = datetime.datetime.now()
			print end-begin	
		k=k+1
		

if __name__=='__main__':
	args=sys.argv
	str1=open(args[1]).read()
	file1=args[1]

	#file=file1[:22]+'checkpoint_'+file1[-9:]
	file=file1[:29]+'check-'+file1[-30:]
	#file=file1[:21]+'check-'+file1[-20:]
	
	extract(str1,file)