PORT=$1
if [ 6 -gt ${#PORT} ] || [ ${PORT::5} != '/dev/' ]
then
  PORT='/dev/ttyUSB0';
fi

ampy --port $PORT put pysite/_superpyhtml_.py _superpyhtml_.py
ampy --port $PORT mkdir 'html'
for FILE in $(ls pysite/html); 
do 
	echo $FILE;
	ampy --port $PORT put 'pysite/html/'$FILE 'html/'$FILE
done
