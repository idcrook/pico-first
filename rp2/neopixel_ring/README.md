Pico Neopixel Demo
==================

Demo that uses Pico PIO to drive a 12 WS2812 LED ring using micropython.

Adapted from https://github.com/raspberrypi/pico-micropython-examples/blob/master/pio/neopixel_ring/neopixel_ring.py

Setup
-----

| Ring  | Pico   | pin | Voltage  |
|-------|--------|-----|----------|
| `DI`  | `GP6`  | 9   | 3.3V     |
| `5V`  | `VBUS` | 40  | 5V (USB) |
| `GND` | `GND`  | 38  |          |
| `DO`  | NC     |     |          |

-	connect ring `pin.5V` to Pico `VBUS` (5V USB)
-	connect ring `pin.GND` to Pico GND
-	connect ring `pin.DI` to Pico `GP6` (3.3V)
-	no-connect ring `pin.DO`

Run
---

```shell
cd ~/projects/pico/pico-first-projects/
cd rp2/neopixel_ring/
rshell --buffer-size=512 -p /dev/ttyACM0
> cp neopixel_ring.py /pyboard/
```

Enter `repl` from `rshell`

```console
> repl
>>> import neopixel_ring
```
