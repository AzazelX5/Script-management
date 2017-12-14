import json
from django.core import serializers
from . import models
from django.http import HttpResponse
# Create your views here.


def get_script(request, script_id=None):
    """
    获取脚本:无script_id则获取全部
    :param request:
    :param script_id: 脚本ID
    :return:
    """
    if script_id is None:
        json_str = serializers.serialize('json', models.Script.objects.all())
    else:
        json_str = serializers.serialize('json', models.Script.objects.filter(id__startswith=script_id))
    return HttpResponse(json_str, content_type="application/json")


def save_script(request):
    """
    保存脚本
    :param request:
    :return:
    """
    name_exist = []
    name_success = []
    if request.method == 'POST':
        script_dict = json.loads(request.body)
        try:
            for key in script_dict:
                # 判断脚本是否已经存在
                result = models.Script.objects.filter(name=key)[:1]
                if result:
                    # 存在则返回已经存在脚本的名称
                    name_exist.append('    ' + key + '\n')
                else:
                    # 不存在则在数据库中新建，之后返回保存成功的脚本名单
                    models.Script.objects.create(name=key, content=script_dict[key])
                    name_success.append('    ' + key + '\n')
            json_str = json.dumps({'success': name_success, 'exist': name_exist})
        except BaseException:
            return HttpResponse('Upload failed')
        return HttpResponse(json_str, content_type="application/json")
    else:
        return HttpResponse('Wrong request method')

