# set system-wide proxy settings.

import sys

def setproxy(http,reset=False):
    if sys.platform=='linux':
        raise NotImplementedError
    elif sys.platform=='win32' or sys.platform=='cygwin':
        # write windows registry
        import winreg
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, # master
            r'Software\Microsoft\Windows\CurrentVersion\Internet Settings', #path
            0, # reserved
            winreg.KEY_SET_VALUE, # permission
        )

        winreg.SetValueEx(
            registry_key,
            'ProxyServer', # name
            0, # reserved
            winreg.REG_SZ, # string
            'http={};https={}'.format(http,http), # value
        )
        winreg.SetValueEx(
            registry_key,
            'ProxyOverride',
            0,
            winreg.REG_SZ,
            '<local>',
        )
        winreg.SetValueEx(
            registry_key,
            'ProxyEnable',
            0,
            winreg.REG_DWORD,
            1 if reset==False else 0,
        )

        winreg.CloseKey(registry_key)

    elif sys.platform=='darwin':
        raise NotImplementedError
    else:
        raise NotImplementedError

if __name__ == '__main__':
    setproxy('127.0.0.1:58080',reset=True)
