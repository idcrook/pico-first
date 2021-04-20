Pico Neopixel Demo
==================

Demo that uses PIO to drive a 12 WS2812 LED ring using micropython.

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
