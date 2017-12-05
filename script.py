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


def get_script():
    req = urllib2.Request('http://108.61.86.91/script/get_script/')
    res = urllib2.urlopen(req)
    script_list = json.loads(res.read())

    str_exist = ''
    str_success = ''
    str_result = 'Download failed!'
    try:
        for result_dict in script_list:
            script_name = result_dict.get('fields').get('name')
            script_content = result_dict.get('fields').get('content')
            if os.path.exists(script_name):
                str_exist += ('    ' + script_name + '\n')
            else:
                with open(script_name, 'w+') as f:
                    f.write(script_content)
                str_success += ('    ' + script_name + '\n')
    except BaseException:
        print str_result

    if len(str_exist) == 0:
        str_result = 'All scripts have been downloaded locally!'
    elif len(str_success) == 0:
        str_result = 'All scripts exist locally!'
    else:
        str_result = 'The name of the script successfully downloaded locally:\n{}'.format(str_success[:-1]) + '\n' + \
                     'The name of the script already exists locally:\n{}'.format(str_exist[:-1])

    print str_result


def save_script():
    name_list = os.listdir('.')
    if len(name_list) == 1:
        print 'No script can be uploaded, please check before operation!'
    else:
        name_list.remove('script.py')
        script_dict = {}
        for name in name_list:
            with open(name, 'r') as f:
                script_dict[name] = f.read()
        url = 'http://108.61.86.91/script/save_script/'
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

            if len(result_dict['exist']) == 0:
                for success in result_dict['success']:
                    str_success += success
                print 'Update successful script name:\n{}'.format(str_success[:-1])
            elif len(result_dict['success']) == 0:
                print 'The server already has all the scripts!'
            else:
                for success in result_dict['success']:
                    str_success += success
                for exist in result_dict['exist']:
                    str_exist += exist
                print 'Update successful script name:\n{}'.format(str_success[:-1])
                print 'The server already has a script name:\n{}'.format(str_exist[:-1])


def search_script(num=8, id=None):
    if id is None:
        url = 'http://108.61.86.91/script/get_script/'
    else:
        url = 'http://108.61.86.91/script/get_script/' + id
    req = urllib2.Request(url)
    try:
        res = urllib2.urlopen(req)
    except urllib2.HTTPError:
        print 'Did not find the relevant script!'
        exit()

    script_list = json.loads(res.read())
    if len(script_list) == 0:
        print 'Did not find the relevant script!'
    else:
        str_script = ''
        if num == 8:
            for result_dict in script_list:
                str_script += (result_dict.get('pk')[:8] + ' ' * 5 + result_dict.get('fields').get('name') + '\n')
        else:
            for result_dict in script_list:
                str_script += (result_dict.get('pk') + ' ' * 5 + result_dict.get('fields').get('name') + '\n')
        print 'A list of all the scripts in the server:\nID' + ' ' * (num + 3) + 'NAME\n{}'.format(str_script[:-1])


# 判断请求
if len(data_input) == 2 and data_input[1] == 'push':
    save_script()
elif len(data_input) == 2 and data_input[1] == 'pull':
    get_script()
elif len(data_input) == 2 and data_input[1] == 'ls':
    search_script()
elif len(data_input) == 3 and data_input[1] == 'ls' and data_input[2] == '-a':
    search_script(num=36)
elif len(data_input) >2 and data_input[1] == 'search':
    if len(data_input) == 3:
        search_script(id=data_input[2])
    elif len(data_input) == 4:
        if data_input[2] == '-a':
            search_script(num=36, id=data_input[3])
        elif data_input[3] == '-a':
            search_script(num=36, id=data_input[2])
else:
    print 'push: Updated\npull: Download\nls [-a]: View\nsearch [-a] id: Fuzzy query'

