import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')
parser.add_argument('floats', metavar='R', type=float, nargs='+', help='an float for XXX')
parser.add_argument('--print', dest='pr', action='store_const', const=print)
args = parser.parse_args()
print(args.accumulate(args.integers))
print(args.pr(args.floats))