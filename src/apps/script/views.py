import json
from django.core import serializers
from . import models
from django.http import HttpResponse
# Create your views here.


def get_script(request, script_id=None):
    if script_id is None:
        json_str = serializers.serialize('json', models.Script.objects.all())
    else:
        # scripts = models.Script.objects.filter(id__icotains=script_id)
        # json_str = json.dumps({
        #     'name': scripts.name,
        #     'content': scripts.content
        # })
        json_str = serializers.serialize('json', models.Script.objects.filter(id__startswith=script_id))
    return HttpResponse(json_str, content_type="application/json")


def save_script(request):
    name_exist = []
    name_success = []
    if request.method == 'POST':
        script_dict = json.loads(request.body)
        try:
            for key in script_dict:
                result = models.Script.objects.filter(name=key)[:1]
                if result:
                    name_exist.append('    ' + key + '\n')
                else:
                    models.Script.objects.create(name=key, content=script_dict[key])
                    name_success.append('    ' + key + '\n')
            json_str = json.dumps({'success': name_success, 'exist': name_exist})
        except BaseException:
            return HttpResponse('Upload failed')
        return HttpResponse(json_str, content_type="application/json")
    else:
        return HttpResponse('Wrong request method')

