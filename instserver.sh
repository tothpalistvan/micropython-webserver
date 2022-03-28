for x in $(ls webserver); 
do 
	echo $x;
	ampy --port /dev/ttyUSB0 put 'webserver/'$x $x
done
