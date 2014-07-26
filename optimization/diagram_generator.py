from gprof2dot import PstatsParser, DotWriter, TEMPERATURE_COLORMAP
from StringIO import StringIO
from subprocess import Popen, PIPE
import sys


def generate_diagram_spec(stats_file):
    output = StringIO()
    parser = PstatsParser(stats_file)
    profile = parser.parse()
    dot = DotWriter(output)
    profile.prune(0.005, 0.001)
    theme = TEMPERATURE_COLORMAP
    theme.skew = 1.0
    dot.graph(profile, theme)
    return output.getvalue()


def generate_diagram_from_spec(specs, target_file):
    p = Popen(
        ['dot', '-Tpng', '-o', target_file],
        stdout=PIPE, stdin=PIPE, stderr=PIPE
    )
    stdout, stderr = p.communicate(input=specs)
    if stderr != '':
        raise RuntimeError(stderr)


def generate_diagram(stats_file, target_file):
    specs = generate_diagram_spec(stats_file)
    generate_diagram_from_spec(specs, target_file)


if __name__ == '__main__':
    stats_file, target_file = sys.argv[1:]
    generate_diagram(stats_file, target_file)
    print 'Generated diagram:', target_file
