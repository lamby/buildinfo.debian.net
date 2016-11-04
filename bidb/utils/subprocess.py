from __future__ import absolute_import

import subprocess

def check_output2(args, stdin=None):
    p = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    out, _ = p.communicate(input=stdin)

    retcode = p.wait()

    if retcode:
        raise subprocess.CalledProcessError(retcode, ' '.join(args), out)

    return out
