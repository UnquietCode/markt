import sys
import mistletoe

from unquietcode.tools.markt import TerminalRenderer



def main():
    file_ = sys.argv[1]
    
    with open(file_, 'r') as fin:
        rendered = mistletoe.markdown(fin, TerminalRenderer)

    print(rendered)





if __name__ == '__main__':
    main()
