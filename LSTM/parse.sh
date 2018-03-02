#!/bin/bash

for i in {d2.2xlarge,g2.2xlarge,m3.medium,m4.xlarge,r3.large}
do 
	ec2-describe-spot-price-history -H --region us-east-1 --instance-type $i --start-time 2017-10-30T12:00:00 --end-time 2017-11-30T12:00:00 --product-description "Linux/UNIX" --aws-access-key AKIAIHSNUA7UOTL5S2EA --aws-secret-key 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 >> /Users/zhenghaoyue/Desktop/LSTM/price/price-$i.txt
done

for i in {d2.2xlarge,g2.2xlarge,m3.medium,m4.xlarge,r3.large}
#for i in {g2.2xlarge}
do 
	python parseprice.py $i
done

#periodically
'''
yesterday=$(date -v-1d +%F)
today=$(date +%F)
start="${yesterday}T12:00:00"
end="${today}T12:00:00"
echo $start
echo $end

for i in {d2.2xlarge,g2.2xlarge,m3.medium,m4.xlarge,r3.large}
do 
	ec2-describe-spot-price-history -H --region us-east-1 --instance-type $i --start-time $start --end-time $end --product-description "Linux/UNIX" --aws-access-key AKIAIHSNUA7UOTL5S2EA --aws-secret-key 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 >> /Users/zhenghaoyue/Desktop/LSTM/price/price-$i.txt
done


for i in {d2.2xlarge,g2.2xlarge,m3.medium,m4.xlarge,r3.large}
do 
	python parseprice.py $i
done
'''