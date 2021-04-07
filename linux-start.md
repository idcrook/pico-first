Using C++ SDK on Ubuntu Linux
=============================

https://datasheets.raspberrypi.org/pico/getting-started-with-pico.pdf

Get SDK and examples
--------------------

```shell
mkdir -p ~/projects/pico
cd ~/projects/pico
git clone --recurse-submodules https://github.com/raspberrypi/pico-sdk.git
git clone https://github.com/raspberrypi/pico-examples.git
```

Install the toolchain
---------------------

```shell
sudo apt update
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential
# on Ubuntu
sudo apt install libstdc++-arm-none-eabi-newlib
# for GDB and OpenOCD
sudo apt install gdb-multiarch
```

Blink an LED
------------

```shell
cd ~/projects/pico/pico-examples

echo $PICO_SDK_PATH
#export PICO_SDK_PATH=../../pico-sdk

mkdir build
cd build
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

```shell
cd ~/projects/pico
git clone https://github.com/raspberrypi/picotool.git
cd picotool
# dependencies
sudo apt-get install libusb-1.0-0-dev
```

building

```shell
cd ~/projects/pico/picotool
mkdir build
cd build
export PICO_SDK_PATH=$HOME/projects/pico/pico-sdk
cmake ../
make
./picotool help
# Pico in BOOTSEL mode
sudo ./picotool info -a
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
sudo ./picotool info -a
# load and e(x)ecute a program
sudo ./picotool load -x ~/projects/pico/pico-examples/build/blink/blink.uf2
```

reboot

```shell
cd ~/projects/pico/picotool/build
sudo ./picotool info -a
# Reboot back into the (a)pplication
sudo ./picotool reboot -a
```

minicom
-------

```shell
sudo apt install minicom
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