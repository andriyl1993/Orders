import json

from django.http import HttpResponseBadRequest, HttpResponse


def required_fields(class_name, fields):
    def wrapper(fn):
        def wrapper_wrapper(request):
            if request.method == 'POST':
                data = json.loads(request.body)
                class_data = data.get('data-' + class_name, {})
                if class_data:
                    wrong_fields = []
                    for field in fields:
                        if not class_data.get(field, False):
                            wrong_fields.append(field)
                    if wrong_fields:
                        return HttpResponseBadRequest(json.dumps({'error': 'require_field', 'data': wrong_fields, 'result': False}))
                else:
                    return HttpResponseBadRequest(json.dumps({'error': 'wrong_class', 'data': [], 'result': False}))
            res = fn(request)
            return res
        return wrapper_wrapper
    return wrapper


def form_valid(form_cls, form_single=False):
    def wrapper(fn):
        def wrapper_wrapper(request):
            if request.method == 'POST':
                if not form_single:
                    class_name = form_cls.Meta.model.__name__
                else:
                    class_name = form_cls.__name__
                data = json.loads(request.body).get('data-' + class_name, {})
                form = form_cls(data)
                if not form.is_valid():
                    return HttpResponseBadRequest(json.dumps({'error': 'invalid_form', 'data': [], 'result': False}))
            return fn(request)
        return wrapper_wrapper
    return wrapper


def resp_json(fn):
    def wrapper(request):
        res = fn(request)
        if isinstance(res, dict):
            json_res = json.dumps(res)
            return HttpResponse(json_res) if res.get('result') else HttpResponseBadRequest(json_res)
        else:
            return res
    return wrapper
