Exar USB Serial Driver
======================
Version 1A, 1/9/2015

This driver will work with any USB UART function in these Exar devices:
	XR21V1410/1412/1414
	XR21B1411
	XR21B1420/1422/1424
	XR22801/802/804

The source code has been tested on various Linux kernels from 3.6.x to 5.10.x.  
This may also work with newer kernels as well.  


Installation
------------

* Compile and install the common usb serial driver module

	# make
	# make install

NOTE: to ensure that the conflicting CDC-ACM module is not loaded the 'make install' adds the CDC-ACM blacklist file under /etc/modprobe.d/

* Plug the device into the USB host.  You should see up to four devices created, typically /dev/ttyXRUSB[0-3].

	# ls -la /dev/ttyXR*


Tips for Debugging
------------------

* Check that the USB UART is detected by the system

	# lsusb

* Check that the CDC-ACM driver was not installed for the Exar USB UART

	# ls /dev/tty*

* Remove the current driver by running

	# make cleanall


Technical Support
-----------------
Send any technical questions/issues to uarttechsupport@exar.com. 

