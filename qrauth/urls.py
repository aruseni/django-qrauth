from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('qrauth.views',
    url(
        r'^pic/(?P<auth_code>[a-zA-Z\d]{50})/$',
        'qr_code_picture',
        name='auth_qr_code'
    ),
    url(
        r'^(?P<auth_code_hash>[a-f\d]{40})/$',
        'login_view',
        name='qr_code_login'
    ),
    url(
        r'invalid_code/$',
        TemplateView.as_view(
            template_name='qrauth/invalid_code.html'
        ),
        name='invalid_auth_code'
    ),
    url(
        r'^$',
        'qr_code_page',
        name='qr_code_page'
    ),
)
