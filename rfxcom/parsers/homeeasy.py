from rfxcom.message import Message

class HomeEasyParser(object):
    @staticmethod
    def parse(length, packet):
        """
        >>> from rfxcom.parsers.util import _h
        >>> HomeEasyParser.parse(0, [])
        False
        >>> HomeEasyParser.parse(34, _h('c7e05dda00'))
        Message('homeeasy', address='31f8177', command='on', device='10', source='31F8177A')
        >>> HomeEasyParser.parse(34, _h('c7e05de000'))
        Message('homeeasy', address='31f8177', command='off', device='group', source='31F8177G')
        >>> HomeEasyParser.parse(36, _h('c7e05dca70'))
        Message('homeeasy', address='31f8177', command='preset', device='10', level=7, source='31F8177A')
        """
        if not HomeEasyParser.valid(length, packet):
            return False
        
        address = ((packet[0] << 18) + (packet[1] << 10) +
            (packet[2] << 2) + (packet[3] >> 6))
        address = '%07x' % address
        command = (packet[3] >> 4) & 0x3
        device = (command & 0x2) and 'group' or ('%02d' % (packet[3] & 0xf))
        source = '%s%s' % (address.upper(), (command & 0x2) and 'G' or ('%1X' % (packet[3] & 0xf)))
        if length == 36:
            level = packet[4] >> 4
            return Message('homeeasy', address=address, device=device, level=level, command='preset', source=source)
        else:
            command = (command & 0x1) and 'on' or 'off'
            return Message('homeeasy', address=address, device=device, command=command, source=source)
    
    @staticmethod
    def valid(length, packet):
        """
        >>> from rfxcom.parsers.util import _h
        >>> HomeEasyParser.valid(0, [])
        False
        >>> HomeEasyParser.valid(34, _h('c7e05dda00'))
        True
        >>> HomeEasyParser.valid(34, _h('c7e05de000'))
        True
        >>> HomeEasyParser.valid(36, _h('c7e05dca70'))
        True
        """
        return length in (34, 36)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
