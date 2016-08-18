"""Provides the dump_mem function, which dumps memory in hex/ASCII."""

import sys
if sys.implementation.name == 'micropython':
    import ubinascii
    def hexlify(buf):
        return ubinascii.hexlify(buf, ' ')
else:
    def hexlify(buf):
        # CPython's hexlify doesn't have the notion of a seperator character
        # so we just do this the old fashioned way
        return bytes(' '.join(['{:02x}'.format(b) for b in buf]), 'ascii')


def dump_mem(buf, prefix='', address=0, line_width=16, show_ascii=True,
             show_addr=True, log=print):
    """Dumps out a hex/ASCII representation of the given buffer."""
    if line_width < 0:
        line_width = 16
    if len(prefix) > 0:
        prefix += ':'
    if len(buf) == 0:
        log(prefix + 'No data')
        return
    buf_len = len(buf)
    mv = memoryview(buf)
    
    prefix_bytes = bytes(prefix, 'utf-8')
    prefix_len = len(prefix_bytes)
    out_len = prefix_len
    if show_addr:
        out_len += 6
    hex_offset = out_len
    out_len += line_width * 3
    if show_ascii:
        ascii_offset = out_len + 1
        out_len += line_width + 1
    out_line = memoryview(bytearray(out_len))
    out_line[0:prefix_len] = prefix_bytes

    line_hex = out_line[hex_offset:hex_offset + (line_width * 3)]
    line_hex[0] = ord(' ')
    if show_ascii:
        out_line[ascii_offset - 1] = ord(' ')
        line_ascii = out_line[ascii_offset:ascii_offset + line_width]

    for offset in range(0, buf_len, line_width):
        if show_addr:
            out_line[prefix_len:prefix_len + 6] = bytes(' {:04x}:'.format(address), 'ascii')
        line_bytes = min(buf_len - offset, line_width)
        line_hex[1:(line_bytes * 3)] = hexlify(mv[offset:offset+line_bytes])
        if line_bytes < line_width:
            line_hex[line_bytes * 3:] = b'   ' * (line_width - line_bytes)
        if show_ascii:
            line_ascii[0:line_bytes] = mv[offset:offset + line_bytes]
            if line_bytes < line_width:
                line_ascii[line_bytes:] = b' ' * (line_width - line_bytes)
            for i in range(line_bytes):
                char = line_ascii[i]
                if char < 0x20 or char > 0x7e:
                    line_ascii[i] = ord('.')
        log(bytes(out_line).decode('utf-8'))
        address += line_width
