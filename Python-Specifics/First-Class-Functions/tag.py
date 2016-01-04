def tag(name, *content, cls=None, **attrs):
    if cls:
        attrs['class'] = cls

    if attrs:
        attr_str = ' '.join('%s=%s' % (k, v) for k, v in attrs.items())
    else:
        attr_str = ' '

    if content:
        return '\n'.join('<%s %s>%s<%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)


def test_func(a, *, b):
    return a, b
