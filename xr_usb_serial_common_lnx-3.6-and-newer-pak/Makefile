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

install: all
	sudo cp blacklist-cdc-acm.conf /etc/modprobe.d/
	@test -f /lib/modules/`uname -r`/kernel/drivers/tty/serial/xr_usb_serial_common.ko && echo "Reinstalling the existing driver in /lib/modules/`uname -r`/kernel/drivers/tty/serial/"
	sudo cp xr_usb_serial_common.ko /lib/modules/`uname -r`/kernel/drivers/tty/serial
	sudo depmod -ae
	sudo update-initramfs -u
