def _h(x):
    return [ ord(y) for y in x.decode('hex') ]

def hi_nibble(x):
    return x >> 4

def lo_nibble(x):
    return x & 0xf

def nibble_sum(c, y):
    s = 0
    for i in range(0, c):
        s += hi_nibble(y[i])
        s += lo_nibble(y[i])
    if int(c) != c:
        s += hi_nibble(y[c])
    return s

def dec_byte(p, n):
    return hi_nibble(p[n]) * 10 + lo_nibble(p[n])
