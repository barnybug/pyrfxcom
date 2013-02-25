from rfxcom.message import Message
from rfxcom.parsers.util import hi_nibble, lo_nibble, nibble_sum, \
    dec_byte

def checksum1(p):
    c = hi_nibble(p[6]) + (lo_nibble(p[7])<<4)
    s = ( ( nibble_sum(6, p) + lo_nibble(p[6]) - 0xa) & 0xff)
    return s == c

def checksum2(p):
    return p[8] == ((nibble_sum(8, p) - 0xa) & 0xff)
    
def checksum3(p):
    return p[11] == ((nibble_sum(11, p) - 0xa) & 0xff)
    
def checksum4(p):
    return p[9] == ((nibble_sum(9, p) - 0xa) & 0xff)
    
def checksum5(p):
    return p[10] == ((nibble_sum(10, p) - 0xa) & 0xff)
    
def checksum6(p):
    return (hi_nibble(p[8])+(lo_nibble(p[9])<<4) ==
      ((nibble_sum(8, p) - 0xa) & 0xff))
      
def checksum7(p):
    return p[7] == ((nibble_sum(7, p) - 0xa) & 0xff)
    
def checksum8(p):
    c = hi_nibble(p[9]) + (lo_nibble(p[10])<<4)
    s = ( ( nibble_sum(9, p) - 0xa) & 0xff)
    return s == c

def temperature(p, message):
    temp = (((p[6]&0x8) and -1 or 1) *
        (hi_nibble(p[5])*10.0 + lo_nibble(p[5]) +
         hi_nibble(p[4])/10.0))
    message['temp'] = temp
    
def humidity(p, message):
    hum = lo_nibble(p[7])*10 + hi_nibble(p[6])
    message['humidity'] = hum
    
def simple_battery(p, message):
    battery_low = p[4]&0x4
    bat = battery_low and 10 or 90
    message['battery'] = bat
    
def percentage_battery(p, message):
    message['battery'] = 100 - 10*lo_nibble(p[4])

def common_temp(part, message, p):
    message['source'] = message['sensor'] = '%s.%02x' % (part, p[3])
    temperature(p, message)
    simple_battery(p, message)
    
def common_temphydro(part, message, p):
    message['source'] = message['sensor'] = '%s.%02x' % (part, p[3])
    temperature(p, message)
    humidity(p, message)
    simple_battery(p, message)

def alt_temphydro(part, message, p):
    message['source'] = message['sensor'] = '%s.%02x' % (part, p[3])
    temperature(p, message)
    humidity(p, message)
    percentage_battery(p, message)

WIND_DIRECTIONS = [ "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NWN" ]
def wtgr800_anemometer(part, message, p):
    dirno = hi_nibble(p[4])
    speed = lo_nibble(p[7]) * 10 + hi_nibble(p[6]) + lo_nibble(p[6]) / 10.0
    avgspeed = hi_nibble(p[8]) * 10 + lo_nibble(p[8]) + hi_nibble(p[7]) / 10.0
    message['source'] = message['sensor'] = part
    message['dir'] = dirno
    message['speed'] = speed
    message['avgspeed'] = avgspeed

def pcr800_rain(part, message, p):
    message['source'] = message['sensor'] = '%s.%02x' % (part, p[3])
    rain = (lo_nibble(p[6])*10 +
        hi_nibble(p[5]) + lo_nibble(p[5])/10.0 +
        hi_nibble(p[4])/100.0)
    rain *= 25.4 # convert from inch/hr to mm/hr
    
    train = (lo_nibble(p[9])*100 +
      dec_byte(p, 8) + dec_byte(p, 7)/100.0 +
        hi_nibble(p[6])/1000.0)
    train *= 25.4 # convert from inch/hr to mm/hr
    
    message['speed'] = rain
    message['total'] = train
    simple_battery(p, message)
  
class OregonParser(object):
    messages = {
        (0xfa28, 80):
        {
            'part': 'THGR810', 'topic': 'temp', 'checksum': checksum2, 'method': common_temphydro,
        },
        (0xfab8, 80):
        {
            'part': 'WTGR800', 'topic': 'temp', 'checksum': checksum2, 'method': alt_temphydro,
        },
        (0x1a99, 88):
        {
            'part': 'WTGR800', 'topic': 'wind', 'checksum': checksum4, 'method': wtgr800_anemometer,
        },
        #(0x1a89, 88):
        #{
        #    'part': 'WGR800', 'checksum': checksum4, 'method': wtgr800_anemometer,
        #},
        #(0xda78, 72):
        #{
        #    'part': 'UVN800', 'checksum': checksum7, 'method': uvn800,
        #},
        #(0xea7c, 120):
        #{
        #    'part': 'UV138', 'checksum': checksum1, 'method': uv138,
        #},
        (0xea4c, 80):
        {
            'part': 'THWR288A', 'topic': 'temp', 'checksum': checksum1, 'method': common_temp,
        },
        (0xea4c, 68):
        {
            'part': 'THN132N', 'topic': 'temp', 'checksum': checksum1, 'method': common_temp,
        },
        #(0x9aec, 104):
        #{
        #    'part': 'RTGR328N', 'checksum': checksum3, 'method': rtgr328n_datetime,
        #},
        #(0x9aea, 104):
        #{
        #    'part': 'RTGR328N', 'checksum': checksum3, 'method': rtgr328n_datetime,
        #},
        #(0x1a2d, 80):
        #{
        #    'part': 'THGR228N', 'checksum': checksum2, 'method': common_temphydro,
        #},
        #(0x1a3d, 80):
        #{
        #    'part': 'THGR918', 'checksum': checksum2, 'method': common_temphydro,
        #},
        #(0x5a5d, 88):
        #{
        #    'part': 'BTHR918', 'checksum': checksum5, 'method': common_temphydrobaro,
        #},
        #(0x5a6d, 96):
        #{
        #    'part': 'BTHR918N', 'checksum': checksum5, 'method': alt_temphydrobaro,
        #},
        #(0x3a0d, 80):
        #{
        #    'part': 'WGR918', 'checksum': checksum4, 'method': wgr918_anemometer,
        #},
        #(0x3a0d, 88):
        #{
        #    'part': 'WGR918', 'checksum': checksum4, 'method': wgr918_anemometer,
        #},
        #(0x2a1d, 84):
        #{
        #    'part': 'RGR918', 'checksum': checksum6, 'method': common_rain,
        #},
        #(0x0a4d, 80):
        #{
        #    'part': 'THR128', 'checksum': checksum2, 'method': common_temp,
        #},
        #(0xca2c, 80):
        #{
        #    'part': 'THGR328N', 'checksum': checksum2, 'method': common_temphydro,
        #},
        #(0xca2c, 120):
        #{
        #    'part': 'THGR328N', 'checksum': checksum2, 'method': common_temphydro,
        #},
        ## masked
        #(0x0acc, 80):
        #{
        #    'part': 'RTGR328N', 'checksum': checksum2, 'method': common_temphydro,
        #},
        (0x2a19, 92):
        {
            'part': 'PCR800', 'topic': 'rain', 'checksum': checksum8, 'method': pcr800_rain,
        },
    }

    @staticmethod
    def parse(length, packet):
        """
        >>> from rfxcom.parsers.util import _h
        >>> OregonParser.parse(0, [])
        False
        >>> OregonParser.parse(0x44, _h('ea4c204d4200706319'))
        Message('temp', battery=90, sensor='thn132n.4d', source='thn132n.4d', temp=0.4)
        >>> OregonParser.parse(0x50, _h('fa282462320290053c64'))
        Message('temp', battery=90, humidity=59, sensor='thgr810.62', source='thgr810.62', temp=2.3)
        >>> OregonParser.parse(0x50, _h('fab814c676000094534d'))
        Message('temp', battery=40, humidity=40, sensor='wtgr800.c6', source='wtgr800.c6', temp=0.7)
        >>> OregonParser.parse(0x58, _h('1a9904c634c00000003c1f'))
        Message('wind', avgspeed=0, dir='ENE', sensor='wtgr800', source='wtgr800', speed=0)
        >>> OregonParser.parse(0x58, _h('1a99042f10c01200013980'))
        Message('wind', avgspeed=1, dir='NNE', sensor='wtgr800', source='wtgr800', speed=1.2)
        >>> OregonParser.parse(0x5c, _h('2a19046f000000854280130e'))
        Message('rain', battery=90, sensor='pcr800.6f', source='pcr800.6f', speed=0, total=1088)
        >>> OregonParser.parse(0x5c, _h('2a19043f300080220120230a'))
        Message('rain', battery=90, sensor='pcr800.3f', source='pcr800.3f', speed=0.762, total=31.19)
        """
        if not OregonParser.valid(length, packet):
            return False

        type = (packet[0] << 8) + packet[1]
        m = OregonParser.messages[(type, length)]
        msg = Message(m['topic'])
        m['method'](m['part'].lower(), msg, packet)
        
        return msg
    
    @staticmethod
    def valid(length, packet):
        """
        >>> from rfxcom.parsers.util import _h
        >>> OregonParser.valid(0, [])
        False
        >>> OregonParser.valid(0x44, _h('ea4c204d4200706319'))
        True
        >>> OregonParser.valid(0x50, _h('fa282462320290053c64'))
        True
        >>> OregonParser.valid(0x50, _h('fab814c676000094534d'))
        True
        >>> OregonParser.valid(0x58, _h('1a9904c634c00000003c1f'))
        True
        >>> OregonParser.valid(0x5c, _h('2a19046f000000854280130e'))
        True
        """
        if length < 2:
            return False
        type = (packet[0] << 8) + packet[1]
        rec = OregonParser.messages.get((type, length))
        if not rec:
            return False
        return rec['checksum'](packet)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
