PORT=$1
if [ 6 -gt ${#PORT} ] || [ ${PORT::5} != '/dev/' ]
then
  PORT='/dev/ttyUSB0';
fi

for FILE in $(ls webserver); 
do 
	echo $FILE;
	ampy --port $PORT put 'webserver/'$FILE $FILE
done
