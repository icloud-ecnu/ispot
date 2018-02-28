echo "Mount the EBS......"
sudo mkfs -t ext4 /dev/xvdf
sudo mkdir /mnt/disk1
sudo mount /dev/xvdf /mnt/disk1
sudo sh -c "cat ~/ispot/mountpoint >> /etc/fstab"
sudo mount -a
sudo mkdir /mnt/disk1/hadoop/
sudo chmod -R 777 /mnt/disk1/hadoop/
sudo mkdir /mnt/disk1/tmp/
sudo mkdir /mnt/disk1/tmp/spark/
sudo chmod 777 /mnt/disk1/tmp/spark/
echo "Mount EBS successful!"

