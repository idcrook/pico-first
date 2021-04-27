pico-first-projects
===================

Tracking my early experiments and usage of Raspberry Pi Pico.

```
├── debugger
├── doc
├── picoprobe
└── rp2
```

-	[`debugger`](debugger/#readme): notes from unsuccessful Segger J-LINK attempt
-	`doc`: placeholder directory for local downloads
-	[`picoprobe`](picoprobe/#readme): notes for `picoprobe` (using a Pico to debug with SWD another Pico)
-	[`rp2`](rp2/#readme): MicroPython projects. `rp2` is what the micropython uses for RP2040 (Pico) board.

Getting started notes
---------------------

Start from the beginning with Raspberry Pi Pico and its RP2040. Successfully did this on three platforms: macOS, (Ubuntu) Linux (x86_64), and Raspberry Pi OS (32-bit, Model 4 B)

https://www.raspberrypi.org/documentation/rp2040/getting-started/

-	https://rptl.io/pico-get-started \[pdf\]

Notes from following the guide:

-	[C/C++ notes on Raspberry Pi OS](raspios-start.md)
-	[C/C++ notes on macOS](macos-start.md)
-	[C/C++ notes on (Ubuntu) Linux](linux-start.md)

MicroPython projects
--------------------

Kept in directory named [`rp2`](rp2/#readme) as that is what MicroPython has named its RP2040 machine support.

```shell
cd ~/projects/pico
cd pico-first-projects/  # this repo
cd rp2                   # micropython projects
cat README.md
```

Along with its [README](rp2/README.md), also includes instructions to [build micropython from source](rp2/BUILD.md).

picoprobe wiring
----------------

See directory [picoprobe](picoprobe/#readme)
