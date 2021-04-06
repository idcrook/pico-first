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


1. Wire up as in Appendix A.
2. Flash `picoprobe.uf2` onto "probe" Pico
3. Other startup tasks
   a. For Picoprobe's UART: `sudo minicom -D /dev/ttyACM0 -b 115200`
   b. `sudo src/openocd -f interface/picoprobe.cfg -f target/rp2040.cfg -s tcl`
       - didn't work from Pi without `sudo`

#### Picoprobe Wiring

![Picoprobe wiring](picoprobe/picoprobe-wiring-with-serial-1.png)
