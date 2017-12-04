# test subprocess.

import time
import subprocess as sp

def run_subprocess(args, end_callback=None, print_callback=print):
    print_callback(
        '[run_subprocess] starting process "{}"'.format(' '.join(args))
    )
    pop = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE)
    def stdout_poll():
        while True:
            err = pop.stderr.readline()
            print_callback(err.decode('utf-8'))
            if pop.poll() is not None:
                break

    def stderr_poll():
        while True:
            out = pop.stdout.readline()
            print_callback(out.decode('utf-8'))
            if pop.poll() is not None:
                break

    def process_poll():
        while True:
            if pop.poll() is not None:
                print_callback(
                    '[run_subprocess] process "',
                    ' '.join(args),
                    '" ended with status',
                    pop.returncode
                )
                if end_callback is not None:
                    end_callback()
                break
            else:
                time.sleep(0.2)

    import threading as th
    t = [th.Thread(target=k, daemon=True) for k in [stdout_poll,stderr_poll,process_poll]]

    [k.start() for k in t]
    return t,pop

import sys
def stdoutprint(*args):
    args = list(map(lambda x:str(x),args))
    s = ' '.join(args)
    sys.stdout.write(s)
    sys.stdout.flush()

if __name__ == '__main__':
    t, pop = run_subprocess(
        ['ping','baidu.com'],
        print_callback=stdoutprint,
    )
    [k.join() for k in t]
