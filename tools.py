import time

import ping3
from netifaces import interfaces, ifaddresses, AF_INET


class Delay:
    def __init__(self):
        self.delay_list = []
        self.default_len = 60

    def instert_value(self, delay_time):
        if len(self.delay_list) < self.default_len:
            self.delay_list.append(delay_time)
        else:
            self.delay_list.pop(-1)
            self.delay_list.append(delay_time)

    def get_avg(self):
        return sum(self.delay_list) / len(self.delay_list)

def get_local_ip():
    # 获取本机ip地址
    addrs = []
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        # print('%s: %s' % (ifaceName, ', '.join(addresses)))
        addrs.append(addresses)
    return addrs

def main():
    delay = Delay()
    loc_ips = get_local_ip()
    for i in loc_ips:
        print(loc_ips.index(i),i[0])
    local_addr_index = loc_ips[int(input('请输入本机ip地址序号：'))][0]
    # ping3.DEBUG = True
    site_addr = input('请输入要ping的地址：')
    timeout = input('请输入超时时间：(默认4s)')
    if not timeout:
        timeout = 4
    else:
        timeout = int(timeout)
    pass_index = 0
    failed_index = 0
    while True:
        log = open(f'{time.strftime("%Y-%m-%d-%H", time.localtime())}-{site_addr}', 'a+', encoding='utf-8')
        timestmp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        try:
            resp_time = ping3.ping(site_addr, timeout=timeout, unit='ms',src_addr=local_addr_index)
            if resp_time:
                pass_index += 1
                delay.instert_value(resp_time)
                print(f'[{timestmp}]{local_addr_index} ping {site_addr} success! cost_time:{round(resp_time, 3)}ms avg:{round(delay.get_avg(),3)}ms pass_rate:{round(pass_index/(pass_index+failed_index),3)}')
                log.write(f'[{timestmp}]{local_addr_index} ping {site_addr} success! cost_time:{round(resp_time, 3)}ms  avg:{round(delay.get_avg(),3)}ms pass_rate:{round(pass_index/(pass_index+failed_index),3)}\n')
            else:
                failed_index += 1
                print(f'[{timestmp}]{local_addr_index} ping {site_addr} failed!  cost_time:None failed times:{failed_index} pass_rate:{round(pass_index/(pass_index+failed_index),3)}')
                log.write(f'[{timestmp}]{local_addr_index} ping {site_addr} failed!  cost_time:None failed times:{failed_index} pass_rate:{round(pass_index/(pass_index+failed_index),3)}\n')
        except Exception as e:
            failed_index += 1
            print(e)
            log.write(f'[{timestmp}]{e}\n')
        finally:
            time.sleep(1)
            log.close()
if __name__ == '__main__':
    main()