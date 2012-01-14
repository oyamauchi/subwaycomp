
import hashlib
import os
import subprocess

def send_query(query_string):
    hsh = hashlib.sha1(query_string).hexdigest()
    cachefile = os.path.join('.', 'datacache', hsh)
    cachefile = os.path.realpath(cachefile)
    if os.path.exists(cachefile):
        return open(cachefile).read()

    args = ['curl', '--data', '@-',
            'http://www.overpass-api.de/api/interpreter']
    curl = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=open('/dev/null', 'w'))
    curl.stdin.write(query_string)
    curl.stdin.close()

    result = curl.stdout.read()

    if not os.path.exists(os.path.dirname(cachefile)):
        os.mkdir(os.path.dirname(cachefile))
    open(cachefile, 'w').write(result)

    return result
