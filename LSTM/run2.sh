#! /bin/bash
declare -a DIRS
declare -a FILES
DIRS=$1
# dirs=(m3medium)
#FILES=(a b c d e f)

if [ $1 = d2 ]; then
    echo d2
    FILES=(a b c d e f)
fi
if [ $1 = g2 ]; then
    echo g2
    FILES=(d e)
fi
if [ $1 = m4 ]; then
    echo m4
    FILES=(e f)
fi
if [ $1 = r3 ]; then
    echo r3
    FILES=(a b c d)
fi
for dir in ${DIRS[*]}
do
    str1=eventlog/AL/AL_75G/
    str3=${str1}${dir}
    #echo $2
    python gen.py $str3 || exit
    #echo $str3
    for file in ${FILES[*]}
    do
        #echo $str3
        #echo $file
        if [ $dir = m3medium -a $file = e ]; then
            continue
        fi
        python train2.py $str3 $file || exit
    done
done
#echo ${FILES[*]}