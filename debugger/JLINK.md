
## Segger J-Link EDU

https://wiki.segger.com/Raspberry_Pi_Pico


```shell
sudo apt install ./JLink_Linux_V698e_x86_64.deb
tar zxvf Setup_EmbeddedStudio_ARM_v542_linux_x64.tar.gz
sudo arm_segger_embedded_studio_542_linux_x64/install_segger_embedded_studio
# /usr/share/segger_embedded_studio_for_arm_5.42/
# -> /usr/share/segger_embedded_studio_for_arm_5.42/bin/emStudio
sudo apt install ./Ozone_Linux_V322e_x86_64.deb
```


## firmware update (log)

```console
$ JLinkExe
SEGGER J-Link Commander V6.98e (Compiled Mar 29 2021 14:22:14)
DLL version V6.98e, compiled Mar 29 2021 14:21:59

Connecting to J-Link via USB...Updating firmware:  J-Link V9 compiled Feb  2 2021 16:34:10
Replacing firmware: J-Link V9 compiled May 17 2019 09:50:41
Waiting for new firmware to boot
New firmware booted successfully
O.K.
Firmware: J-Link V9 compiled Feb  2 2021 16:34:10
Hardware version: V9.30
S/N: 269302253
License(s): FlashBP, GDB
OEM: SEGGER-EDU
VTref=0.000V


Type "connect" to establish a target connection, '?' for help
J-Link>
```

## Ozone

```shell
Ozone
```

After configuring for a RP2040, it errors and says Hardware rev of JLink does not support multi-drop SWD and stops.

Hardware Rev is 9.3 and [wiki page for Segger Pico](https://wiki.segger.com/Raspberry_Pi_Pico) says Rev 11 is required.
