import requests
from datetime import datetime, timedelta
import json

import book
import getPwd

start_time = 0
end_time = 23
retry = 0

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d")

def func():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'https://network-lab.mooc.buaa.edu.cn/index.php?m=Student&c=Index&a=add',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'm': 'Home',
        'c': 'Index',
        'a': 'ajaxQry',
        'labid': 'all',
        'date': formatted_time,
    }

    response = requests.get(
        'https://network-lab.mooc.buaa.edu.cn/index.php',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )

    jsondata = json.loads(response.text)['data']
    for item in jsondata:
        flag = True
        for i in range(start_time, end_time):
            str = f'T{i}'
            if item[str] == '1':
                flag = False
                break
        if flag:
            # print(f"labid: {item['laboratory_id']} devicegroupid: {item['devicegroup_id']}")
            labid = item['laboratory_id']
            devicegroupid = item['devicegroup_id']
            ret = book.run(labid=labid, devicegroupid=devicegroupid, cutTime=formatted_time, begin_time=start_time, end_time=end_time, cookies=cookies)
            
            if len(ret) == 1:
                print(ret[0])
            else:
                appid = ret[1]
                getPwd.get_infos(appid, cookies)
                return True
    
    print('无空闲实验室，请修改预约时间后重试')

def split_string_to_dict(input_str):
    result_dict = {}
    pairs = input_str.split('; ')
    for pair in pairs:
        key, value = pair.split('=', 1)
        result_dict[key] = value
    
    return result_dict

def is_valid_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False
    
    today = datetime.today()
    future_date = today + timedelta(days=8)
    
    if today <= date_obj <= future_date:
        return True
    else:
        return False

def get_input():
    global formatted_time, cookies, start_time, end_time
    while True:
        date = (input('日期（mm-dd）：'))
        if date == '':
            break
        elif is_valid_date(f'{current_time.year}-{date}'):
            formatted_time = f'{current_time.year}-{date}'
            break
        print('请检查输入格式')
      
    while True:
        start_time = int(input('开始时间：'))
        end_time = int(input('结束时间：'))
        if 1 <= end_time - start_time <= 4:
            break
        print('预约时段不合法')

    print(f"{'*' * 30}即将预约{formatted_time}的{start_time}:00至{end_time}:00{'*' * 30}")
    cookies = split_string_to_dict(input('cookies：'))

if __name__ == '__main__':
    get_input()
    flag = False
    while retry < 16:
        flag = func()
        if flag:
            break
        retry += 1
    if not flag:
        print('失败了')