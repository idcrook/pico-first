macOS SDK
=========

https://datasheets.raspberrypi.org/pico/getting-started-with-pico.pdf

Pre-requisites
--------------

1.	[The Missing Package Manager for macOS (or Linux) — Homebrew](https://brew.sh/)

Get SDK and examples
--------------------

```shell
mkdir -p ~/projects/pico
cd ~/projects/pico
git clone --recurse-submodules https://github.com/raspberrypi/pico-sdk.git
git clone https://github.com/raspberrypi/pico-examples.git
```

### Optional: Get pico-extras and pico-playground

```shell
cd ~/projects/pico
git clone https://github.com/raspberrypi/pico-extras.git
git clone https://github.com/raspberrypi/pico-playground.git
```

Install the toolchain
---------------------

```shell
brew install cmake
brew tap ArmMbed/homebrew-formulae
brew install arm-none-eabi-gcc
```

Download and install [Visual Studio Code](https://code.visualstudio.com/download)

Blink an LED
------------

```shell
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

Install OpenOCD (for `picoprobe`\)
----------------------------------

-	`--disable-presto --disable-openjtag` added to `configure` based on
	-	[Fails to compile on MacOS using the latest libftdi · Issue #7 · raspberrypi/openocd](https://github.com/raspberrypi/openocd/issues/7#issuecomment-766730331)

```shell
brew install open-ocd --only-dependencies
brew install automake
brew install autoconf libusb pkg-config libtool texinfo wget gcc

cd ~/projects/pico
git clone https://github.com/raspberrypi/openocd.git --branch picoprobe --depth=1 --no-single-branch
cd openocd


cd ~/projects/pico/openocd

export PATH="$(brew --prefix)/opt/texinfo/bin:$PATH"
./bootstrap
CAPSTONE_CFLAGS="-I$(brew --prefix)/include" \
  ./configure --prefix="$(brew --prefix)"  \
  --enable-picoprobe --disable-presto --disable-openjtag

make -j5

src/openocd
```

### picoprobe

```shell
cd ~/projects/pico
git clone https://github.com/raspberrypi/picoprobe.git
cd picoprobe
mkdir build
cd build
echo $PICO_SDK_PATH
cmake ..
make -j5
# produces picoprobe.elf/picoprobe.uf2
```

`picoprobe` installs onto Pico like any other application.

#### Picoprobe Wiring

![Picoprobe wiring](picoprobe/picoprobe-wiring-with-serial-1.png)

Image copied from: [How to debug a Raspberry Pi Pico with a Mac, SWD and… another Pico | smittytone messes with micros](https://blog.smittytone.net/2021/02/05/how-to-debug-a-raspberry-pi-pico-with-a-mac-swd/)

![Picoprobe hooked up](picoprobe/picoprobe--photo.jpeg)

### minicom

```shell
brew install minicom
ls -latr /dev/tty.usb*
minicom --baudrate 115200 --noinit --device /dev/tty.usbmodem224201
minicom --baudrate 115200 --noinit --device /dev/tty.usbmodem0000000000001
```

-	To exit minicom, use <kbd>Esc-z</kbd> followed by <kbd>x</kbd>.

### OpenOCD

In one terminal window

```shell
cd ~/projects/pico/openocd
src/openocd -f interface/picoprobe.cfg -f target/rp2040.cfg -s tcl
```

In another window, if using the picoprobe UART

```shell
minicom --baudrate 115200 --noinit --device /dev/tty.usbmodem*
```

In a third terminal window

```shell
cd ~/projects/pico/pico-examples/build/hello_world/serial
arm-none-eabi-gdb hello_serial.elf
```

connect GDB to OpenOCD

```console
(gdb) target remote localhost:3333
Remote debugging using localhost:3333
(gdb) load
Loading section .boot2, size 0x100 lma 0x10000000
Loading section .text, size 0x4178 lma 0x10000100
Loading section .rodata, size 0xe60 lma 0x10004278
Loading section .binary_info, size 0x28 lma 0x100050d8
Loading section .data, size 0x1e0 lma 0x10005100
Start address 0x100001e8, load size 21216
Transfer rate: 6 KB/sec, 3536 bytes/write.
(gdb) monitor reset init
target halted due to debug-request, current mode: Thread
xPSR: 0xf1000000 pc: 0x000000ee msp: 0x20041f00
target halted due to debug-request, current mode: Thread
xPSR: 0xf1000000 pc: 0x000000ee msp: 0x20041f00
(gdb) continue
Continuing.
```

Picotool
--------

from "Appendix B: Using Picotool"

```shell
cd ~/projects/pico
git clone https://github.com/raspberrypi/picotool.git
cd picotool

brew install libusb pkg-config
```

building

```shell
cd ~/projects/pico/picotool
mkdir build
cd build
echo $PICO_SDK_PATH
# export PICO_SDK_PATH=$HOME/projects/pico/pico-sdk
cmake ../
make
./picotool help
# Pico in BOOTSEL mode
./picotool info
./picotool info -a
```

can be used to inspect and manage local files

```shell
cd ~/projects/pico/picotool/build
./picotool info -a ~/projects/pico/pico-examples/build/blink/blink.uf2
./picotool info --pins ~/projects/pico/pico-examples/build/blink/blink.elf
```

can load a program

```shell
cd ~/projects/pico/picotool/build
./picotool info -a
# load and e(x)ecute a program
./picotool load -x ~/projects/pico/pico-examples/build/blink/blink.uf2
```

can reboot a pico

```shell
cd ~/projects/pico/picotool/build
./picotool info -a
# Reboot back into the (a)pplication
./picotool reboot --application
# Reboot back into BOOTSEL mode
./picotool reboot --usb
```

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
