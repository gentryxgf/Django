# 公共登录表单，对应到settings里面templates设置

from .forms import LoginForm


def login_modal_form(request):
    return {'login_modal_form': LoginForm()}