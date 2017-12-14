#!/usr/bin/python2.7
# coding=utf-8
import sys
import urllib2
import json
import os

reload(sys)
sys.setdefaultencoding('utf-8')

# 记录命令行输入内容
data_input = sys.argv


# 获取脚本函数
def get_script():
    req = urllib2.Request('http://0.0.0.0/script/get_script/')
    res = urllib2.urlopen(req)
    script_list = json.loads(res.read())

    str_exist = ''  # 已存在脚本名称
    str_success = ''  # 成功更新到本地脚本名称
    str_result = 'Download failed!'
    try:
        for result_dict in script_list:
            script_name = result_dict.get('fields').get('name')
            script_content = result_dict.get('fields').get('content')
            # 判断本地是否已经存在该脚本
            if os.path.exists(script_name):
                # 存在则将脚本名称保存
                str_exist += ('    ' + script_name + '\n')
            else:
                # 不存在则新建脚本文件后写入，且将名称记录下来
                with open(script_name, 'w+') as f:
                    f.write(script_content)
                str_success += ('    ' + script_name + '\n')
    except BaseException:
        print str_result

    if len(str_exist) == 0:
        # 将服务器上所有脚本都更新到本地提示信息
        str_result = 'All scripts have been downloaded locally!'
    elif len(str_success) == 0:
        # 本地已有所有脚本后提示信息
        str_result = 'All scripts exist locally!'
    else:
        # 本地只有部分脚本，则只更新不存在的提示信息
        str_result = 'The name of the script successfully downloaded locally:\n{}'.format(str_success[:-1]) + '\n' + \
                     'The name of the script already exists locally:\n{}'.format(str_exist[:-1])

    print str_result


# 上传脚本函数
def save_script():
    name_list = os.listdir('.')
    # 判断是否有脚本可以上传
    if len(name_list) == 1:
        # 没有脚本可上传提示信息
        print 'No script can be uploaded, please check before operation!'
    else:
        name_list.remove('script.py')  # 删除上传脚本
        script_dict = {}
        # 将上传脚本所在文件夹下的所有脚本(上传脚本除外)信息存入一个字典
        for name in name_list:
            with open(name, 'r') as f:
                script_dict[name] = f.read()
        url = 'http://0.0.0.0/script/save_script/'  # 服务器地址
        req = urllib2.Request(url, json.dumps(script_dict))
        res = urllib2.urlopen(req)
        result = res.read()
        if result == 'Upload failed':
            print 'Upload failed！'
        elif result == 'Wrong request method':
            print 'Wrong request method！'
        else:
            str_exist = ''
            str_success = ''
            result_dict = json.loads(result)

            # 判断服务器的返回信息
            if len(result_dict['exist']) == 0:
                # 如果服务器上没有本次上传的所有脚本的提示信息
                for success in result_dict['success']:
                    str_success += success
                print 'Update successful script name:\n{}'.format(str_success[:-1])
            elif len(result_dict['success']) == 0:
                # 服务器上存在这次上传的所有脚本的提示信息
                print 'The server already has all the scripts!'
            else:
                # 服务其上只存在部分脚本的提示信息
                for success in result_dict['success']:
                    str_success += success
                for exist in result_dict['exist']:
                    str_exist += exist
                print 'Update successful script name:\n{}'.format(str_success[:-1])
                print 'The server already has a script name:\n{}'.format(str_exist[:-1])


# 查看服务器上脚本名称函数
def search_script(num=8, id=None):
    # 判断是查看单个脚本还是全部
    if id is None:
        url = 'http://0.0.0.0/script/get_script/'
    else:
        url = 'http://0.0.0.0/script/get_script/' + id
    req = urllib2.Request(url)
    try:
        res = urllib2.urlopen(req)
    except urllib2.HTTPError:
        print 'Did not find the relevant script!'
        exit()

    script_list = json.loads(res.read())
    if len(script_list) == 0:
        # 没有找到脚本提示信息
        print 'Did not find the relevant script!'
    else:
        str_script = ''
        # 默认显示脚本的UUID为8为 -a参数可以显示所有
        if num == 8:
            for result_dict in script_list:
                str_script += (result_dict.get('pk')[:8] + ' ' * 5 + result_dict.get('fields').get('name') + '\n')
        else:
            for result_dict in script_list:
                str_script += (result_dict.get('pk') + ' ' * 5 + result_dict.get('fields').get('name') + '\n')
        print 'A list of all the scripts in the server:\nID' + ' ' * (num + 3) + 'NAME\n{}'.format(str_script[:-1])


# 判断请求
if len(data_input) == 2 and data_input[1] == 'push':
    # 将本地脚本全部上传到服务器
    save_script()
elif len(data_input) == 2 and data_input[1] == 'pull':
    # 叫服务器脚本下载到本地
    get_script()
elif len(data_input) == 2 and data_input[1] == 'ls':
    # 查看服务器中已存在的脚本，默认UUID只显示8位
    search_script()
elif len(data_input) == 3 and data_input[1] == 'ls' and data_input[2] == '-a':
    # 查看服务器中已存在的脚本，-a 参数表示显示全部UUID
    search_script(num=36)
elif len(data_input) >2 and data_input[1] == 'search':
    # 按UUID模糊查找服务器中的脚本，查询结果默认显示8位UUID， -a参数表示显示全部UUID
    if len(data_input) == 3:
        search_script(id=data_input[2])
    elif len(data_input) == 4:
        if data_input[2] == '-a':
            search_script(num=36, id=data_input[3])
        elif data_input[3] == '-a':
            search_script(num=36, id=data_input[2])
else:
    print 'push: Updated\npull: Download\nls [-a]: View\nsearch [-a] id: Fuzzy query'

