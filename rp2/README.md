micropython projects
====================

-	[`gps_clock`](gps_clock/#readme): An accurate clock based on GPS receiver
-	[`neopixel_ring`](neopixel_ring/#readme): Driving a generic W2812 12-pixel ring (uses example `pio` code from [pico-micropython-examples](https://github.com/raspberrypi/pico-micropython-examples))

Build micropython from source
-----------------------------

Can get the very latest micropython firmware for Raspberry Pi Pico.

Or change default features. For example, switch to a hardware UART serial port for interactive micropython prompt. Since Pico micropython default config uses the virtual UART over USB for this, setting a hardware UART for this is disabled by default in Pico.

See [BUILD.md](BUILD.md)

Install Thonny
--------------

[Thonny](https://thonny.org/) is self-described as a "Python IDE for beginners" and has some built-in support for micropython on Pico.

This will install latest thonny (`3.3.6`) using PIP. it is more recent than the distribution version (`3.2.7-1`) that is available with `apt install`.

```shell
sudo apt install python3-pip python3-tk
pip3 install --user thonny
# optional: install other recommended packages
sudo apt install -y \
  $(apt-cache depends thonny | grep Recommends: | sed "s/.*ends:\ //" | tr '\n' ' ')
```

Assuming your $PATH is configured correctly for `--user` pip3 python installations, you can launch `thonny` from the command line.

```shell
thonny
```

In menubar item `Tools`, select `Options...`, then navigate to `Interpreter` tab. Select `MicroPython (Raspeberry Pi Pico)` in the dropdown menu for "Which interpreter or device...?"

Since I already had my user configured for `/dev` serial port access (group `dialout` on ubuntu), I left the Port to `< Try to detect port automatically >`, and it found the attached Pico running micropython without any problem.

Enter the program into Thonny's main text panel. Save to Pico as file named `test.py` and click the green arrow button to run on device.

```python
from machine import Pin, Timer

led = Pin(25, Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
```

**NOTE**: If you save to a file specially named `main.py` to the Pico device, it will automatically execute that file after reset / boot.

### Using `rshell`

Install

```shell
pip3 install --user rshell
```

Connect to attached Pico

-	Serial port must be available, so `minicom` and `thonny` need to not be using it.

	```
	rshell --buffer-size=512 -p /dev/ttyACM0
	```

`rshell` session

```console
# ... bunch of startup information ...
/home/pi> ls -l /pyboard
   173 Apr 19 09:26 test.py
/home/pi> cat /pyboard/test.py
from machine import Pin, Timer

led = Pin(25, Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
/home/pi> repl
Entering REPL. Use Control-X to exit.
>
MicroPython v1.15 on 2021-04-19; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>>
>>> import test
>>>
/home/pi>
```

To exit rshell REPL: <kbd>Ctrl</kbd>\-<kbd>x</kbd>

To exit rshell: <kbd>Ctrl</kbd>\-<kbd>d</kbd>

`rshell` Documention: https://github.com/dhylands/rshell/blob/master/README.rst

Examples and other projects
---------------------------

### Official Python SDK Book Examples

```shell
cd ~/projects/pico
git clone https://github.com/raspberrypi/pico-micropython-examples.git
cd pico-micropython-examples
```

Included is an example for a NeoPixel Ring with 12 WS2812 LEDs driven by Pico `pio` hardware.

```shell
cd ~/projects/pico/
cd pico-micropython-examples/
cd pio/neopixel_ring/
```

See wiring diagram in that directory, or here: https://github.com/raspberrypi/pico-micropython-examples/tree/master/pio/neopixel_ring#readme
