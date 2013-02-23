from rfxcom.message import Message

class X10Parser(object):
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
    def parse(length, packet):
        """
        >>> from rfxcom.parsers.util import _h
        >>> X10Parser.parse(0, [])
        False
        >>> X10Parser.parse(16, _h('65'))
        False
        >>> X10Parser.parse(32, _h('659b08f7'))
        False
        >>> X10Parser.parse(32, _h('649b08f7'))
        Message('x10', command='on', device='11', group='a', source='a11')
        >>> X10Parser.parse(32, _h('e01f609f'))
        Message('x10', command='off', device='05', group='i', source='i05')
        >>> X10Parser.parse(32, _h('00ff38c7'))
        Message('x10', command='off', device='04', group='m', source='m04')
        """
        if not X10Parser.valid(length, packet):
            return False
        
        group = X10Parser.bytes_to_groups[((packet[0]&0xf0)>>4)]
        mask = 0x98
        device = 0
        if packet[2] & 0x80 == 0:
            device = X10Parser.bytes_to_units[ packet[2] & 0x58 ]
            if packet[0] & 0x4:
                device += 8
            device = '%02d' % (device+1)
            mask = 0x20
        
        command = X10Parser.bytes_to_command[ packet[2] & mask ]
        source = '%s%s' % (group, device)

        return Message('x10', group=group, device=device, command=command, source=source)
    
    @staticmethod
    def valid(length, packet):
        """
        >>> from rfxcom.parsers.util import _h
        >>> X10Parser.valid(0, _h(''))
        False
        >>> X10Parser.valid(24, _h('659b08'))
        False
        >>> X10Parser.valid(32, _h('659b08f7'))
        False
        >>> X10Parser.valid(32, _h('649b08f7'))
        True
        """
        return (length == 32 and packet[0]^packet[1] == 0xff and packet[2]^packet[3] == 0xff)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
