import sys

from reclut import __version__


def main():
    try:
        action = sys.argv[1]
    except:
        print_help()
        quit()
    if action == "download":
        from reclut import download
        download.main(sys.argv[2:])
    elif action == "block":
        from reclut import block
        block.main()
    elif True:
        for arg in sys.argv[1:]:
            if arg == "-h" or arg == "--help" or arg == "help":
                print_help()
            else:
                print(f"Invalid Action: {action}\n")
                print_help()
                exit()


def print_help():
    print(f"""
Reddit Command Line Utilities: For data-hoarding, automation and general avoidance of reddit's web ui

usage: reclut --help/-h
    reclut download [see --help/-h]
    reclut block [user1] [user2]

See README at github.com/vitezfh/reclut on how to configure reclut

Version: ({__version__})
""")


if __name__ == '__main__':
    main()
