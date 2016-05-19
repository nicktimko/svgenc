import sys
import argparse
import base64

from jinja2 import Environment, PackageLoader

def check_css(uri, style):
    return ".chk-{} {{background-image:url('{}');}}".format(style, uri)

env = Environment(loader=PackageLoader('makepage', '.'))
env.filters['chkcss'] = check_css

def generate_data_uri(payload, mime='image/svg+xml', charset=None):
    return 'data:{}{},{}'.format(mime, (';' + charset) if charset else '', payload)

gdi = generate_data_uri

def get_template(f):
    return env.get_template(f)

URL_ENC_CHARS = " !\"#$%&'(),:;<=>?[\]^`{|}~"
MINIMAL_CHARS = "\"#%<>[]^{|}`"

def url_encode(payload, chars=URL_ENC_CHARS, skip=''):
    return ''.join(
        '%{:02X}'.format(ord(c)) if (c not in skip) and (c in chars) else c
        for c
        in payload
    )

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('svg', type=argparse.FileType('r'))

    args = parser.parse_args()

    svg = ''.join(l.strip() for l in args.svg)
    context = {}
    context['general'] = [
        {'name': 'SVG file', 'cls': 'file', 'uri': 'check.min.svg'},
        {'name': 'No encoding', 'cls': 'raw', 'uri': gdi(svg)},
        {'name': 'Base64 encoded', 'cls': 'b64', 'uri': gdi(base64.b64encode(svg), charset='base64')},
        {'name': 'URL encoded default', 'cls': 'url', 'uri': gdi(url_encode(svg))},
        {'name': 'URL encoded only <code>"#%&lt;>[]^{|}`</code>', 'cls': 'min', 'uri': gdi(url_encode(svg, chars=MINIMAL_CHARS))},
    ]

    available_chars = [c for c in URL_ENC_CHARS if c in svg]

    context['skips'] = []
    for c in available_chars:
        svg_encoded = url_encode(svg, chars=available_chars, skip=c)
        context['skips'].append({
            'c': c,
            'x': format(ord(c), 'X'),
            'uri': gdi(svg_encoded),
            'uri_u8': gdi(svg_encoded, charset='utf8'),
            'uri_u8f': gdi(svg_encoded, charset='charset=UTF-8'),
        })

    template = env.get_template('template.html')
    with open('index.html', 'w') as f:
        f.write(template.render(context))


if __name__ == '__main__':
    sys.exit(main())
