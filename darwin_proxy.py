import os
from sp import run_subprocess

def get_network_services():
    collected = ''
    def collect(*args):
        nonlocal collected
        s = ' '.join(list(map(lambda x:str(x), args)))
        collected+=s
    t,pop = run_subprocess(
        ['networksetup','-listallnetworkservices'],
        print_callback=collect,
    )
    [k.join() for k in t]

    # print(collected)
    collected = collected.split('\n')
    collected = map(lambda x:x.strip(),collected)
    collected = filter(lambda x:len(x)>0,collected)
    collected = filter(lambda x:not(x.startswith('[') or x.startswith('An')),collected)
    collected = list(collected)
    # print(collected)
    return collected

def set_proxy(domain, port, reset=False):
    print('darwin set_proxy',domain,port,'reset:',reset)
    services = get_network_services()
    print('list of services found:',services)
    
    if len(services)<1:
        print('Can\'t find any network service. Please try restart the program.')
        print('找不到任何网络服务。请尝试重启程序。')
        raise NotImplementedError('Failed to find any network service')

    service = services[0]
    # print(service)

    def ignore(*args):
        pass

    # escalation
    if os.geteuid() != 0:
        # if not root
        print('No root priviledge. Might need your password.')
        print('没有root权限，可能需要你账户的密码。')
        t,pop = run_subprocess(
            ['sudo','true'], print_callback=ignore,
        )
        [k.join() for k in t]
        if pop.returncode!=0:
            raise PermissionError('Failed to grant priviledge. 权限获取失败。')
    else:
        # print('is root')
        pass

    if reset==False:
        t,pop = run_subprocess(
            ['sudo','networksetup','-setwebproxy',service,domain,str(port)],
            print_callback=ignore,
        )
        [k.join() for k in t]
        t,pop = run_subprocess(
            ['sudo','networksetup','-setsecurewebproxy',service,domain,str(port)],
            print_callback=ignore,
        )
        [k.join() for k in t]

    t,pop = run_subprocess(
        ['sudo','networksetup','-setwebproxystate',service,'off' if reset else 'on'],
        print_callback=ignore,
    )
    [k.join() for k in t]
    t,pop = run_subprocess(
        ['sudo','networksetup','-setsecurewebproxystate',service,'off' if reset else 'on'],
        print_callback=ignore,
    )
    [k.join() for k in t]

if __name__ == '__main__':
    set_proxy('127.0.0.1',58080)
