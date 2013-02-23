from rfxcom.message import Message
from rfxcom.parsers.util import *

class OwlParser(object):
    bytes_to_groups = 'mnopcdabefghklij'
    units_to_bytes = '\x00\x10\x08\x18\x40\x50\x48\x58'
    bytes_to_units = dict( (ord(n), i) for i, n in enumerate(units_to_bytes) )
    bytes_to_command = {0x98: 'dim',
                        0x88: 'bright',
                        0x90: 'all_lights_on',
                        0x80: 'all_lights_off',
                        0x00: 'on',
                        0x20: 'off'}
    
    @staticmethod
    def parse(length, p):
        """
        >>> from rfxcom.parsers.util import _h
        >>> OwlParser.parse(0, _h(''))
        False
        >>> OwlParser.parse(120, _h('ea00a642000000169bff5f1dc05408'))
        Message('owl', current1=6.6, current2=0, current3=0, source='a6')
        >>> OwlParser.parse(120, _h('ea04320c00000015eaff5f9d408601'))
        Message('owl', current1=1.2, current2=0, current3=0, source='32')
        >>> OwlParser.parse(120, _h('ea07320e0000001a22ff5ffd40c601'))
        Message('owl', current1=1.4, current2=0, current3=0, source='32')
        """
        if not OwlParser.valid(length, p):
            return False
        
        device = '%02x' % p[2]
        current1 = (p[3] + ((p[4]&0x3)<<8))/10.0
        current2 = (((p[4]&0xfc)>>2) + ((p[5]&0xf)<<6))/10.0
        current3 = (((p[5]&0xf0)>>4) + ((p[6]&0x3f)<<4))/10.0
        
        return Message('owl', current1=current1, current2=current2, current3=current3, source=device)
    
    @staticmethod
    def valid(length, packet):
        """
        >>> from rfxcom.parsers.util import _h
        >>> OwlParser.valid(0, _h(''))
        False
        >>> OwlParser.valid(120, _h('010101010101010101010100101010'))
        False
        >>> OwlParser.valid(120, _h('ea00a642000000169bff5f1dc05408'))
        True
        >>> OwlParser.valid(120, _h('ea04320c00000015eaff5f9d408601'))
        True
        >>> OwlParser.valid(120, _h('ea07320e0000001a22ff5ffd40c601'))
        True
        """
        
        return (length == 120 and packet[0] == 0xea and packet[9] == 0xff and packet[10] == 0x5f)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
