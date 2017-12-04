import tkinter as tk
import time
from form import Form

title_string = 'wengui - GUI for `went`'
form = Form(title = title_string)
root = form.master

# first line
f1 = tk.Frame(form)
f1.pack(side='top',pady=3)

l = tk.Label(f1)
l['text'] = 'Server Address'
l.pack(side='left',padx=3)

VarAddr = tk.StringVar()
VarAddr.set('127.0.0.1')

TxtAddr = tk.Entry(f1)
TxtAddr['textvariable'] = VarAddr
TxtAddr.pack(side='left', fill='x', padx=3)

BtnStart = tk.Button(f1)
BtnStart['text'] = 'Start'
BtnStart.pack(side='left',padx=3)

BtnStop = tk.Button(f1)
BtnStop['text'] = 'Stop'
BtnStop.pack(side='left',padx=3)

# second line
f2 = tk.Frame(form)
f2.pack(side='top', pady=3)

VarInfo = tk.StringVar()
VarInfo.set('info section')

LblInfo = tk.Label(f2)
LblInfo['textvariable'] = VarInfo
LblInfo.pack(side='left')

# third line
f3 = tk.Frame(form)
f3['bg'] = '#333'
f3.pack(side='top',fill='both',expand=True)

VarLog = tk.StringVar()
VarLog.set('log section\nsecondline\ntest\n\n\n\n\n\n\n\n\n\n\nalpha')

LblStdout = tk.Label(f3)
LblStdout.config(
    textvariable = VarLog,
    bg = '#444',
    fg = '#fff',
    justify = tk.LEFT,
    anchor = tk.SW,
    height = '10',
    width = '50',
)
LblStdout.pack(side='left',fill='both',expand=True)

# print things into log area
logbuf = []
def debugprint(*args):
    global logbuf
    lines=(' '.join(list(map(lambda x:str(x),args))).split('\n'))
    lines=list(filter(lambda x:len(x)>0, map(lambda x:x.strip(),lines)))
    # you just witnessed the ugliness of python.
    logbuf+=lines
    if len(logbuf)>100:
        logbuf.pop(0) # trim excess length
    VarLog.set('\n'.join(logbuf))

state = {
    'server':'127.0.0.1',
    'instance':None,
    'v2instance':None,

    'socks_proxy':'127.0.0.1:51080',
    'http_proxy':'127.0.0.1:58080',
}

# show current state and auxillary info in LblInfo
def showstate():
    global state
    s = []
    s.append(
        'Server: {}'.format(state['server'])
    )
    s.append(
        'Main Program: {}'.format(
            'Started' if state['instance'] is not None else 'Not Started'
        )
    )
    s.append(
        'V2Ray(HTTP proxy support): {}'.format(
            'Started' if state['v2instance'] is not None else 'Not Started'
        )
    )
    s.append('SOCKS(4/4a/5) proxy: ' + state['socks_proxy'])
    s.append('HTTP(S) proxy: ' + state['http_proxy'])

    # color indicator
    LblInfo['fg'] = '#482' if state['v2instance'] is not None else '#c42'
    VarInfo.set('\n'.join(s))

from sp import run_subprocess

def Start():
    global state
    addr = VarAddr.get().strip() # the ip address specified
    if state['instance'] is None:
        Stop() # just to make sure

        def ec():
            # callback on process end
            state['instance'] = None
            showstate()

        def v2ec():
            state['v2instance']=None
            showstate()

        # executable names differ from OS to OS
        import sys
        if sys.platform=='win32' or sys.platform=='cygwin':
            went_bin = 'went_win64'
            v2ray_bin = 'v2ray'
        elif sys.platform=='linux':
            went_bin = './went_linux64'
            v2ray_bin = './v2ray'
        elif sys.platform=='darwin':
            went_bin = './went_darwin'
            v2ray_bin = './v2ray'
        else:
            debugprint('Unsupported OS')
            return

        try:
            t,pop = run_subprocess(
                # ['ping','baidu.com'],
                [went_bin,'--connect',addr],
                print_callback=debugprint,
                end_callback=ec,
            )
            state['instance'] = t,pop

            v2t,v2pop = run_subprocess(
                [v2ray_bin],
                print_callback=debugprint,
                end_callback=v2ec,
            )
            state['v2instance'] = v2t,v2pop
        except Exception as e:
            debugprint('Exception on run_subprocess()')
            debugprint(e)
            Stop()
            return

        state['server'] = addr
        # finally started
        showstate()

        from setproxy import setproxy
        try:
            setproxy(state['http_proxy'])
        except Exception as e:
            debugprint('set system proxy failed')
            debugprint(e)
            traceback.print_exc()
        else:
            debugprint('set system proxy success')

    else:
        # if instance exists
        debugprint('Please stop the running instance before starting.')

def Stop():
    global state
    if state['instance'] is not None:
        pop = state['instance'][1]
        debugprint('Sending SIGKILL...')
        pop.kill()

    if state['v2instance'] is not None:
        v2pop = state['v2instance'][1]
        debugprint('Sending SIGKILL...')
        v2pop.kill()

    from setproxy import setproxy
    try:
        setproxy(state['http_proxy'],reset=True)
    except Exception as e:
        debugprint('unset system proxy failed')
        debugprint(e)
        traceback.print_exc()
    else:
        debugprint('unset system proxy success')

settings = {}
def OnLoad():
    global settings
    # load settings from local file on start
    import json
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
    except Exception as e:
        debugprint(e)
        settings = {'server_addr':'127.0.0.1'}

    VarAddr.set(settings['server_addr'])
    debugprint('wengui')
    debugprint('https://github.com/ctmakro/went')
    debugprint('https://github.com/ctmakro/wengui')
    debugprint('https://github.com/v2ray/v2ray-core')
    debugprint('Required in CWD: `went` executable; `v2ray` executable & config.json')
    debugprint('请不要安装使用任何国产杀毒软件/安全工具')
    debugprint('本软件自动设置系统代理 请使用管理员权限运行')

def OnClose():
    # save settings to local file
    global settings
    settings['server_addr'] = VarAddr.get()

    import json
    try:
        with open('settings.json','w') as f:
            json.dump(settings,f)
    except:
        pass

    # stop all process on exit to allow fast termination of host process
    Stop()
    root.destroy()

BtnStart['command'] = Start
BtnStop['command'] = Stop
showstate()

root.protocol("WM_DELETE_WINDOW", OnClose)
OnLoad()

root.mainloop()
