# Create your views here.

import redis

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_backends
from django.contrib.sites.models import get_current_site
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from django.conf import settings

from utils import generate_random_string, salted_hash
from qr import make_qr_code

AUTH_QR_CODE_EXPIRATION_TIME = getattr(
    settings,
    "AUTH_QR_CODE_EXPIRATION_TIME",
    300
)

AUTH_QR_CODE_REDIRECT_URL = getattr(
    settings,
    "AUTH_QR_CODE_REDIRECT_URL",
    "/"
)

AUTH_QR_CODE_REDIS_KWARGS = getattr(
    settings,
    "AUTH_QR_CODE_REDIS_KWARGS",
    {}
)

def uses_redis(func):
    def wrapper(*args, **kwargs):
        kwargs["r"] = redis.StrictRedis(**AUTH_QR_CODE_REDIS_KWARGS)
        return func(*args, **kwargs)

    return wrapper

@login_required
@uses_redis
def qr_code_page(request, r=None):
    auth_code = generate_random_string(50)
    auth_code_hash = salted_hash(auth_code)

    r.setex(
        "".join(["qrauth_", auth_code_hash]),
        AUTH_QR_CODE_EXPIRATION_TIME,
        request.user.id
    )

    return render_to_response("qrauth/page.html",
                              {"auth_code": auth_code},
                              context_instance=RequestContext(request))

@login_required
@uses_redis
def qr_code_picture(request, auth_code, r=None):
    auth_code_hash = salted_hash(auth_code)

    user_id = r.get("".join(["qrauth_", auth_code_hash]))

    if (user_id == None) or (user_id != str(request.user.id)):
        raise Http404("No such auth code")

    current_site = get_current_site(request)
    scheme = request.is_secure() and "https" or "http"

    login_link = "".join([
        scheme,
        "://",
        current_site.domain,
        reverse("qr_code_login", args=(auth_code_hash,)),
    ])

    img = make_qr_code(login_link)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

@uses_redis
def login_view(request, auth_code_hash, r=None):
    redis_key = "".join(["qrauth_", auth_code_hash])

    user_id = r.get(redis_key)

    if user_id == None:
        return HttpResponseRedirect(reverse("invalid_auth_code"))

    r.delete(redis_key)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("invalid_auth_code"))

    # In lieu of a call to authenticate()
    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)

    return HttpResponseRedirect(AUTH_QR_CODE_REDIRECT_URL)
