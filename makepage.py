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

def url_encode(payload, chars=URL_ENC_CHARS, skip=''):
    return ''.join(
        '%{:02X}'.format(ord(c)) if (c not in skip) and (c in URL_ENC_CHARS) else c
        for c
        in payload
    )

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('svg', type=argparse.FileType('r'))

    args = parser.parse_args()

    svg = ''.join(l.strip() for l in args.svg)
    context = {
        'raw': gdi(svg),
        'b64': gdi(base64.b64encode(svg), charset='base64'),
    }

    context['skips'] = [
        {
            'c': c,
            'x': format(ord(c), 'X'),
            'uri': gdi(url_encode(svg, skip=c)),
            'uri_u8': gdi(url_encode(svg, skip=c), charset='utf8'),
            'uri_u8f': gdi(url_encode(svg, skip=c), charset='charset=UTF-8'),
        }
        for c in URL_ENC_CHARS
    ]

    template = env.get_template('template.html')
    with open('svgenc.html', 'w') as f:
        f.write(template.render(context))


if __name__ == '__main__':
    sys.exit(main())
