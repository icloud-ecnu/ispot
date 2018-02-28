#!/bin/bash
echo "Please input the cluster size:"
#read size
size=$(awk 'NR=='1' {print $1}' spot.txt)
echo $size
echo "Please input the instance type:"
ec2type=$(awk 'NR=='2' {print $1}' spot.txt)
echo $ec2type
echo "Please input your spot price:"
price=$(awk 'NR=='2' {print $2}' spot.txt)
echo "Please input the avalible zones:"
zones=($(awk 'NR==3 {print}' spot.txt))
echo "We will request ${size} ${ec2type} spot instances to create the Spark cluster in ${zones[*]}!"
echo "Please input the ImageId which the new instance depend on:"
ami=$(awk 'NR=='4' {print $1}' spot.txt)
echo $ami
sed -i '/ImageId/d' /home/ubuntu/ispot/specification.json
sed -i "1a\"ImageId\": \"$ami\"," /home/ubuntu/ispot/specification.json
sed -i '/InstanceType/d' /home/ubuntu/ispot/specification.json
line=`sed -n "/\"SecurityGroupIds/=" /home/ubuntu/ispot/specification.json`
sed  -i "${line}a\"InstanceType\": \"$ec2type\"," /home/ubuntu/ispot/specification.json
for (( i=1; i<=$size; i++))
do
        echo "Request for one spot instance in the us-east-1${zones[$i-1]} as node$i!" 
        line2=`sed -n "/\"Placement/=" /home/ubuntu/ispot/specification.json`
        sed -i "${line2}a\"AvailabilityZone\": \"us-east-1${zones[$i-1]}\"" /home/ubuntu/ispot/specification.json
        sed -n "`expr ${line2} - 1`p" /home/ubuntu/ispot/specification.json
        sed -n "${line2}p" /home/ubuntu/ispot/specification.json
        sed -n "`expr ${line2} + 1`p" /home/ubuntu/ispot/specification.json
        aws ec2 request-spot-instances --spot-price "${price}" --instance-count 1 --type "one-time" --launch-specification file:///home/ubuntu/ispot/specification.json
        sed -i '/AvailabilityZone/d' /home/ubuntu/ispot/specification.json
done
