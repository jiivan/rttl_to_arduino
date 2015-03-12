# http://merwin.bespin.org/t4a/specs/nokia_rtttl.txt
# http://arduino.cc/en/Tutorial/Tone

import re
import sys

MAX_NOTES_CNT = 100;

def parse_defaults(s):
    bpm = 63
    duration = 4
    scale = 6
    for part in s.lower().split(','):
        key, value = part.strip().split('=')
        value = int(value)
        if key == 'd':
            duration = value
        if key == 'o':
            scale = value
        if key == 'b':
            bpm = value
    return bpm, duration, scale

def parse_notes(s, d_bpm, d_duration, d_scale):
    NOTE_RE = re.compile(r'''(?P<duration>1|2|4|8|16|32)?(?P<note>p|c|c#|d|d#|e|f|f#|g|g#|a|a#|b)(?P<dotted>\.)?(?P<scale>4|5|6|7)?''')
    cnt = 0
    sys.stdout.write('  { ')
    for item in s.lower().split(','):
        item = item.strip()
        if '=' in item:
            k,v = item.split('=')
            v = int(v)
            if k == 'd':
                d_duration = v
            if k == 'o':
                d_scale = v
            if k == 'b':
                d_bpm = v
            continue
        m = NOTE_RE.match(item)
        duration, note, dotted, scale = m.groups()
        if duration is None:
            duration = d_duration
        else:
            duration = int(duration)
        if dotted:
            duration += duration * 2
        if scale is None:
            scale = d_scale
        else:
            scale = int(scale)
        #sys.stderr.write('%d%s%d ' % (duration, note, scale))
        full_note = 60*1000 / d_bpm
        millis = full_note / duration
        if note == 'p':
            tone_constant = '0'
        else:
            tone_constant = ('NOTE_%s%d' % (note.upper(), scale)).replace('#', 'S')
        sys.stdout.write('{%s, %d},' % (tone_constant, millis))
        cnt += 1
    sys.stderr.write('Notes cnt: %d\n' % cnt)
    if cnt > MAX_NOTES_CNT:
        raise RuntimeError('Increase MAX_NOTES_CNT to at least %d' % cnt);
    while cnt < MAX_NOTES_CNT:
        sys.stdout.write('{0, 0}')
        cnt += 1
        if cnt < MAX_NOTES_CNT:
            sys.stdout.write(',')
    sys.stdout.write(' }')

def main(s):
    title, defaults, notes = s.split(':')
    sys.stderr.write('Title:  %s\n' % title)
    d_bpm, d_duration, d_scale = parse_defaults(defaults)
    sys.stderr.write('BPM:    %d (%dms)\n' % (d_bpm, 60000/d_bpm))
    sys.stderr.write('Note:   %d\n' % d_duration)
    sys.stderr.write('Octave: %d\n' % d_scale)
    sys.stdout.write('  // %s\n' % title)
    parse_notes(notes, d_bpm, d_duration, d_scale)

if __name__ == '__main__':
    songs = (
        'Simpsons:d=4,o=5,b=160:32p,c.6,e6,f#6,8a6,g.6,e6,c6,8a,8f#,8f#,8f#,2g',
        'Super Mario Brothers:d=4,o=5,b=100:16e6,16e6,32p,8e6,16c6,8e6,8g6,8p,8g,8p,8c6,16p,8g,16p,8e,16p,8a,8b,16a#,8a,16g.,16e6,16g6,8a6,16f6,8g6,8e6,16c6,16d6,8b,16p,8c6,16p,8g,16p,8e,16p,8a,8b,16a#,8a,16g.,16e6,16g6,8a6,16f6,8g6,8e6,16c6,16d6,8b,8p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16g#,16a,16c6,16p,16a,16c6,16d6,8p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16c7,16p,16c7,16c7,p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16g#,16a,16c6,16p,16a,16c6,16d6,8p,16d#6,8p,16d6,8p,16c6',
        'Super Mario Uderground Theme:d=4,o=6,b=100:32c,32p,32c7,32p,32a5,32p,32a,32p,32a#5,32p,32a#,2p,32c,32p,32c7,32p,32a5,32p,32a,32p,32a#5,32p,32a#,2p,32f5,32p,32f,32p,32d5,32p,32d,32p,32d#5,32p,32d#,2p,32f5,32p,32f,32p,32d5,32p,32d,32p,32d#5,32p,32d#',
        'Super Mariod Death Theme:d=4,o=5,b=90:32c6,32c6,32c6,8p,16b,16f6,16p,16f6,16f.6,16e.6,16d6,16c6,16p,16e,16p,16c',
        'HauntHouse: d=4,o=5,b=108: 2a4, 2e, 2d#, 2b4, 2a4, 2c, 2d, 2a#4, 2e., e, 1f4, 1a4, 1d#, 2e., d, 2c., b4, 1a4, 1p, 2a4, 2e, 2d#, 2b4, 2a4, 2c, 2d, 2a#4, 2e., e, 1f4, 1a4, 1d#, 2e., d, 2c., b4, 1a4',
    )
    sys.stdout.write('const int MELODIES_LEN=%d;\n' % len(songs))
    sys.stdout.write('const int MELODIES_MAX_NOTES=%d;\n' % MAX_NOTES_CNT)
    sys.stdout.write('const int MELODIES[MELODIES_LEN][MELODIES_MAX_NOTES][2] = {')
    cnt = 0
    for s in songs:
        if cnt:
            sys.stdout.write(',')
        sys.stdout.write('\n')
        main(s)
        cnt += 1
    sys.stdout.write('\n};\n')
