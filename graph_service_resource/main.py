from neo4jresource import app
import sys, getopt

def usage():
    print("Usage: python main.py -a|--host <host> -p|--port <port>")

def main(argv):
    host = '0.0.0.0'
    port =  15135
    try:
        opts, args = getopt.getopt(argv, 'ha:p:', ['help',"host=", "port="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-a', '--host'):
            host = arg
        elif opt in ('-p', '--port'):
            port = int(arg)

    app.run(host=host, port=port)

if __name__ == '__main__':
    main(sys.argv[1:])