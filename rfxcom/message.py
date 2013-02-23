class Message(object):
    def __init__(self, topic, **values):
        self.topic = topic
        self.values = values

    def __str__(self):
        """
        >>> str(Message('a', b=1))
        'topic: a, b: 1'
        """
        return 'topic: %s, %s' % (self.topic, ', '.join('%s: %s' % m for m in self.values.iteritems()))

    def __repr__(self):
        """
        >>> repr(Message('a'))
        \"Message('a')\"
        >>> repr(Message('a', b=1))
        \"Message('a', b=1)\"
        """
        if self.values:
            def fmt(x):
                if isinstance(x, float):
                    return '%.4g' % x
                else:
                    return '%r' % x
            vs = ['%s=%s' % (k, fmt(v)) for k, v in sorted(self.values.iteritems())]
            return 'Message(%r, %s)' % (self.topic, (', '.join(vs)))
        else:
            return 'Message(%r)' % self.topic

    def __eq__(self, m):
        """
        >>> Message('a', b=1) == Message('a', b=1)
        True
        >>> Message('a', b=1) == Message('a', b=2)
        False
        >>> Message('a', b=1) == Message('b', b=1)
        False
        """
        return self.topic == m.topic and self.values == m.values

    def __setitem__(self, k, v):
        """
        >>> m = Message('a', b=1); m['b'] = 2; m == Message('a', b=2)
        True
        >>> m = Message('a', b=1); m['c'] = 2; m == Message('a', b=1, c=2)
        True
        """
        self.values[k] = v

    def __getitem__(self, k):
        """
        >>> m = Message('a', b=1); m['b']
        1
        """
        return self.values[k]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
