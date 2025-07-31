from django.http import HttpResponse
from django.http.response import JsonResponse


def hello_world(request):
    print(request)
    return HttpResponse({"hello": "world"})


def navbar_view(request):
    menus = [
        {
            "label": "用户管理",
            "icon": "user",
            "route": "/users",
            "children": [
                {"label": "用户列表", "route": "/users/list"},
                {"label": "角色管理", "route": "/users/roles"},
            ],
        },
    ]
    return JsonResponse(menus, safe=False)
