ampy --port /dev/ttyUSB0 put pysite/_superpyhtml_.py _superpyhtml_.py
ampy --port /dev/ttyUSB0 mkdir 'html'
for x in $(ls pysite/html); 
do 
	echo $x;
	ampy --port /dev/ttyUSB0 put 'pysite/html/'$x 'html/'$x
done
