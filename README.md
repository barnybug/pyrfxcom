pyrfxcom
========

### If you're looking the RFXCOM RFXtrx433 USB, I suggest using the pyRFXtrx library here:
https://github.com/woudt/pyRFXtrx

Python library for reading from an rfxcom USB unit (now discontinued)

Supported devices
-----------------
- Oregon weather devices (THGR810, WTGR800, THN132N, PCR800, etc.)
- OWL power meter (eg. CM113)
- X10 RF devices (Domia Lite, HE403, etc.)
- HomeEasy devices (HE300, HE301, HE303, HE305, etc.)

RFXCOM Devices tested
---------------------
- RFXCOM RFXtrx433 USB Transceiver
- RFXCOM USB 433.92MHz Receiver

Installation
------------
Run::

    pip install pyrfxcom

Usage
-----
Example::

    import rfxcom

    def on_message(message):
        print message
    rfx = RFXCom(on_message)
    rfx.setup()
    rfx.run()


Changelog
---------
0.1.0

- First release
