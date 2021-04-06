Using C++ SDK on Raspberry Pi OS
===

https://datasheets.raspberrypi.org/pico/getting-started-with-pico.pdf

Tested using *Raspberry Pi Model 4 B*

Get SDK and examples
--------------------

```shell
mkdir -p ~/projects
cd ~/projects/

wget https://raw.githubusercontent.com/raspberrypi/pico-setup/master/pico_setup.sh
chmod +x pico_setup.sh

# this will create a pico sub-directory
./pico_setup.sh

# same, but will build picoprobe version of OpenOCD
INCLUDE_PICOPROBE=1 ./pico_setup.sh
```

- Installs toolchain and dependencies
- Clones the repos for  SDK (`pico-sdk`), examples (`pico-examples`), and `pico-extras`/`pico-playground`
- Builds a couple of targets in `pico-examples`
- Clones repos for `picoprobe` and builds
- Clones repos for `picotool` and builds+installs
- Clones `openocd` repo and builds+installs
- Installs Visual Studio Code
- Configures serial port UART on host Pi


Blink an LED
------------

```
cd ~/projects/pico/pico-examples
mkdir build
cd build

echo $PICO_SDK_PATH
#export PICO_SDK_PATH=../../pico-sdk

cmake \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..

# cmake --build . --target blink --parallel 7
cd blink
make -j5
# will produce `blink.elf` and `blink.uf2`

#
cd ~/projects/pico/pico-examples/blink/
# edit blink.c

#
cd ~/projects/pico/pico-examples/build/blink
make -j5


```

Picotool
--------

from "Appendix B: Using Picotool"

```
cd ~/projects/pico/picotool/build
./picotool help
```

setup script does a `make install` for `picotool` which means it is available in your shell.

```shell
# Show Details from a connected Pico in BOOTSEL mode
sudo picotool info -a
```

can be used to inspect and manage local files

```shell
cd ~/projects/pico/pico-examples/build/hello_world/serial/
picotool info -a     hello_serial.uf2
picotool info --pins hello_serial.elf
```

can load a program

```shell
cd ~/projects/pico/pico-examples/build/blink/

# works, if attached Pico is in BOOTSEL mode
sudo picotool info -a

# load and e(x)ecute a program
sudo picotool load -x blink.uf2
```

reboot

```shell
sudo picotool info -a

# Reboot back into the (a)pplication
sudo picotool reboot -a
```

minicom
-------

setup script will install `minicom`

```shell
minicom -b 115200 -o -D /dev/ttyACM0
```

-	To exit minicom, use <kbd>Ctrl-a</kbd> followed by <kbd>x</kbd>.

Automatic project creation
--------------------------

```shell
cd ~/projects/pico
git clone https://github.com/raspberrypi/pico-project-generator.git
cd pico-project-generator
./pico_project.py --gui
```

```shell
cd ~/projects/pico/pico-first-projects/projects
~/projects/pico/pico-project-generator/pico_project.py \
  --feature spi --feature i2c --project vscode test
cd test/build
cmake -DCMAKE_BUILD_TYPE=Debug \
      -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
      ..
```


Install OpenOCD (for `picoprobe`\)
----------------------------------


```shell
cd ~/projects/pico
mv openocd openocd.raspi
git clone https://github.com/raspberrypi/openocd.git --branch picoprobe --depth=1 --no-single-branch openocd.picoprobe
cd openocd.picoprobe

./bootstrap
./configure --enable-ftdi --enable-sysfsgpio --enable-bcm2835gpio --enable-picoprobe
make -j4

src/openocd
```


### Use Two Pico-s, one as OpenOCD probe for other


1. Flash `picoprobe.uf2` onto "probe" Pico
1. Wire the "probe" to the "target" as in *Appendix A*.

#### Picoprobe Wiring

![Picoprobe wiring](picoprobe/picoprobe-wiring-with-serial-1.png)


### Using gdb and OpenOCD

- For Picoprobe's UART: `sudo minicom -D /dev/ttyACM0 -b 115200`
- For OpenOCD `sudo src/openocd -f interface/picoprobe.cfg -f target/rp2040.cfg -s tcl`
       - didn't work from Pi without `sudo`

In one terminal window

```shell
cd ~/projects/pico/openocd.picoprobe
sudo src/openocd -f interface/picoprobe.cfg -f target/rp2040.cfg -s tcl
```

In another terminal window

```shell
minicom -D /dev/ttyACM0 -b 115200
```


In a third  terminal window


```shell
cd ~/projects/pico/pico-examples/build/hello_world/serial
gdb-multiarch hello_serial.elf
```

connect GDB to OpenOCD

```console
(gdb) target remote localhost:3333
Remote debugging using localhost:3333
0x10000ce0 in alarm_pool_add_alarm_at (pool=0xffffffff, time=...,
    callback=0xd0000000, user_data=0x10000337 <__do_global_dtors_aux+42>,
    fire_if_past=100)
    at /home/pi/projects/pico/pico-sdk/src/common/pico_time/time.c:219
219	        pheap_node_id_t id = add_alarm_under_lock(pool, time, callback, user_data, 0, false, &missed);
(gdb) load
Loading section .boot2, size 0x100 lma 0x10000000
Loading section .text, size 0x41b8 lma 0x10000100
Loading section .rodata, size 0xe54 lma 0x100042b8
Loading section .binary_info, size 0x28 lma 0x1000510c
Loading section .data, size 0x1e0 lma 0x10005134
Start address 0x100001e8, load size 21268
Transfer rate: 6 KB/sec, 3544 bytes/write.
(gdb) monitor reset init
target halted due to debug-request, current mode: Thread
xPSR: 0xf1000000 pc: 0x000000ee msp: 0x20041f00
target halted due to debug-request, current mode: Thread
xPSR: 0xf1000000 pc: 0x000000ee msp: 0x20041f00
(gdb) continue
Continuing.
(gdb) <Ctrl-C>
(gdb) monitor reset init
(gdb) b main
(gdb) continue
Continuing.
target halted due to debug-request, current mode: Thread
xPSR: 0x01000000 pc: 0x00000178 msp: 0x20041f00

Thread 1 hit Breakpoint 1, main ()
    at /home/pi/projects/pico/pico-examples/hello_world/serial/hello_serial.c:11
11	    stdio_init_all();
(gdb) continue
(gdb) quit
```
