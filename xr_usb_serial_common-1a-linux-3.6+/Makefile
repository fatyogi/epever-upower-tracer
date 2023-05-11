obj-m := xr_usb_serial_common.o

KERNELDIR ?= /lib/modules/$(shell uname -r)/build
PWD       := $(shell pwd)

EXTRA_CFLAGS	:= -DDEBUG=0

all:
	$(MAKE) -C $(KERNELDIR) M=$(PWD)

modules_install:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) modules_install

clean:
	rm -rf *.o *~ core .depend .*.cmd *.ko *.mod.c .tmp_versions vtty

cleanall: clean
	@echo Removing Exar drivers from /lib/modules/`uname -r`/kernel/drivers/tty/serial
	sudo rm -f /lib/modules/`uname -r`/kernel/drivers/tty/serial/xr*

install: all
	sudo cp blacklist-cdc-acm.conf /etc/modprobe.d/
	sudo cp xr_usb_serial_common.ko /lib/modules/`uname -r`/kernel/drivers/tty/serial
	sudo depmod -ae
	sudo update-initramfs -u
