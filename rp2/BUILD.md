# BUILD micropython from source

These instructions are written based on Ubuntu systems I had available.

Based on `raspberry-pi-pico-python-sdk.pdf`

### Clone the micropython git repository

```shell
mkdir -p ~/projects/pico
cd ~/projects/pico
git clone -b master https://github.com/micropython/micropython.git
cd micropython
git submodule update --init -- lib/pico-sdk lib/tinyusb
```


### do the build stuff

```shell
cd ~/projects/pico
cd micropython

sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential

make -C mpy-cross

cd ports/rp2
make -j4

ls build-PICO/*.{uf2,elf}
```

#### inspect with `picotool`


```shell
cd ~/projects/pico/micropython
cd ports/rp2/
~/projects/pico/picotool/build/picotool info -a \
    build-PICO/firmware.uf2
```

Output

    File build-PICO/firmware.uf2:

    Program Information
     name:            MicroPython
     version:         v1.15
     features:        USB REPL
                      thread support
     frozen modules:  _boot, rp2, onewire, ds18x20, uasyncio, uasyncio/core,
                      uasyncio/event, uasyncio/funcs, uasyncio/lock, uasyncio/stream
     binary start:    0x10000000
     binary end:      0x10044374
     embedded drive:  0x100a0000-0x10200000 (1408K): MicroPython

    Fixed Pin Information
     none

    Build Information
     sdk version:       1.1.0
     pico_board:        pico
     boot2_name:        boot2_w25q080
     build date:        Apr 19 2021
     build attributes:  MinSizeRel


## Test the firmware build

Connect a Pico to your computer via USB, holding down the `BOOTSEL` button as this is done. Release the `BOOTSEL` button. It should appear to your computer as a USB drive named `RPI-RP2`.

Now, can drag the `firmware.uf2` file that was built above onto drive created by connected Pico in `BootSel` mode. Once the micropython firmware has been installed, the Pico should re-boot, this time running the micropython firmware that was just installed.

It will appear as something like `/dev/ttyACM0` - this is the USB virtual serial port.

```shell
sudo apt install minicom
minicom -o -D /dev/ttyACM0
```

There is no need to specify a baud rate, since we are using the USB virtual serial port.

Can press <kbd>Enter</kbd> a few times in the terminal to bring up a prompt:

```python
>>>
>>> help()
```

<kbd>Ctrl</kbd>-<kbd>d</kbd> at an empty prompt will do a _soft reset_ and should come back to a micropython REPL prompt

```python
MPY: soft reboot
MicroPython v1.15 on 2021-04-19; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>> from machine import Pin
>>> led = Pin(25, Pin.OUT)
>>> led.value(1)
>>> led.value(0)
>>>
```

<kbd>Ctrl</kbd>-<kbd>a</kbd> <kbd>x</kbd>  will allow `minicom` to disconnect/exit.


## Customize micropython build

Example to enable Hardware UART REPL (if the USB virtual serial port is not available, for example)

```console
$ cd ~/projects/pico/micropython
$ cd ports/rp2/
$ grep MICROPY_HW_ENABLE_UART_REPL mpconfigport.h
#define MICROPY_HW_ENABLE_UART_REPL             (0) // useful if there is no USB
$ vi mpconfigport.h
### change from (0) to (1) to enable hw uart repl

$ make
```
