
import subprocess

def send_query(query_string):
    args = ['curl', '--data', '@-',
            'http://www.overpass-api.de/api/interpreter']
    curl = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=open('/dev/null', 'w'))
    curl.stdin.write(query_string)
    curl.stdin.close()
    return curl.stdout.read()
