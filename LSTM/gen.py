import sys
import os
import matplotlib.pyplot as plt
import numpy as np
path = sys.argv[1]
cnt = 0

#parameter 1:spot type
#parameter 2:predict price interval
#1
in_files = ['result-useast1a.txt','result-useast1b.txt','result-useast1c.txt','result-useast1d.txt','result-useast1e.txt','result-useast1f.txt']
train_files = ['1a-train.txt','1b-train.txt','1c-train.txt','1d-train.txt','1e-train.txt','1f-train.txt']
test_files = ['1a-test.txt','1b-test.txt','1c-test.txt','1d-test.txt','1e-test.txt','1f-test.txt']
#2
#in_files = ['result-price-d2.2xlarge-f.txt']
#train_files = ['1f-train.txt']
#test_files = ['1f-test.txt']

#in_files = ['result-price-r3.large-f.txt']
#train_files = ['1f-train.txt']
#test_files = ['1f-test.txt']

#n_train = 20000

for i in range(len(in_files)):
    if os.path.exists(os.path.join(path,in_files[i])):
        '''
        with open(os.path.join(path,in_files[i]),'a') as fin:
            for k in range(int(offset)+1):
                fin.writelines('0\n')
            fin.close()
        '''
        with open(os.path.join(path,in_files[i])) as fin:
            with open(os.path.join(path, train_files[i]), 'w') as fout1:
                with open(os.path.join(path, test_files[i]), 'w') as fout2:
                    lines=fin.readlines()
                    length=len(lines)
                    n_train=length-20-1
                    #print length
                    #print n_train

                    cnt = 0
                    for line in lines:
                        #print 'here'
                        if n_train==0:
                            continue
                        if cnt <= n_train:
                            fout1.writelines(line)
                        else:
                            fout2.writelines(line)
                        cnt += 1
                        
