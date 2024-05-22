import requests
import re

def get_infos(app_id, cookies) :
    assert app_id != None
    assert cookies != None
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'https://network-lab.mooc.buaa.edu.cn/index.php?m=Student&c=Index&a=add',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'm': 'Student',
        'c': 'Index',
        'a': 'account',
        'id': app_id,
        'resend': '0',
    }

    response = requests.get(
        'https://network-lab.mooc.buaa.edu.cn/index.php',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )

    # print(response.status_code)
    html_content = response.text
    ip_port_pattern = re.compile(r'登录IP:端口：</td>\s*<td><span>(.*?)</span></td>', re.S)
    ip_port_match = ip_port_pattern.search(html_content)
    if ip_port_match:
        ip_port = ip_port_match.group(1)
        print("登录IP:端口:", ip_port)

    # 使用正则表达式提取登录账号和密码
    login_info_pattern = re.compile(r'登录账号&nbsp;\(密码\)：</td>\s*<td><span>(.*?)</span><span>\((.*?)\)</span></td>', re.S)
    login_info_match = login_info_pattern.search(html_content)
    if login_info_match:
        login_account = login_info_match.group(1)
        password = login_info_match.group(2)
        print("登录账号:", login_account)
        print("密码:", password)
