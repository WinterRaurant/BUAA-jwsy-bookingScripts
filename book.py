import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(labid=300, devicegroupid = 333, cutTime = '1970-01-01', begin_time=0, end_time=23, cookies=''):

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://network-lab.mooc.buaa.edu.cn',
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
        'm': 'Student',
        'c': 'Index',
        'a': 'ajaxAdd',
    }

    data = {
        'labid': labid,
        'devicegroupid': devicegroupid,
        'system': '0',
        'appointdate': cutTime,
        'begintime': begin_time,
        'endtime': end_time,
        'assistorcount': '0',
        'experimentid': '49',
        'memo': '',
    }


    response = requests.post(
        'https://network-lab.mooc.buaa.edu.cn/index.php',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False
    )

    jsondata = json.loads(response.text)
    status_code = jsondata['status']
    msg = jsondata['info']
    if status_code == 1:
        app_id = jsondata['data']['appointid']
        return msg, app_id
    else:
        return msg