What is django-qrauth?
======================

django-qrauth allows you to easily spice up your website with instant user authentication: once a user has signed in on their Mac or PC, they can pick up their smartphone (or tablet, iPod, etc: actually, anything that has Internet access, a camera and a QR code scanning application should work), scan a QR code (which appears on the display after the user clicks the corresponding link) and immediately sign in on their smartphone or other mobile device they use (so they don’t have to enter the site address, nor their login/email, nor password).

![A screenshot: scanning an authentication QR code on an Android phone](example.png "Scanning an authentication QR code on an Android phone")

You can see the detailed walkthrough in [this screencast](http://www.youtube.com/watch?v=6ob3oR_Frhk) (in Russian) and in [this blog post](http://habrahabr.ru/post/181093/) (also in Russian).

Visit [Background Dating](http://backgrounddating.com/) to see this in action.

Installation
============

Step 1
------

Install [Redis](http://redis.io/).

Step 2
------

Install django-qrauth:

    pip install django-qrauth

Step 3
------

Open your templates directory and add the following templates: qrauth/invalid_code.html and qrauth/page.html. For example:

**qrauth/invalid_code.html**

    {% extends "base.html" %}

    {% block title %}Invalid QR code{% endblock %}

    {% block content %}
    <div class="error">
        <h1>Invalid QR code</h1>
        <p>The QR code you are using for authentication is invalid. Please try to open the page with the QR code again and then rescan it.</p>
    </div>
    {% endblock %}

**qrauth/page.html**

    {% extends "base.html" %}

    {% block title %}Authentication QR code{% endblock %}

    {% block content %}
    <div class="qr_code">
        <h1>Authentication QR code</h1>
        <p>Scan this QR code to instantly sign in to the website on your mobile device (a smartphone, a tablet, etc):</p>
        <div><img src="{% url auth_qr_code auth_code %}" alt="QR"></div>
        <p>Every generated QR code only works once and only for 5 minutes. If you need another QR code, just open <a href="{% url qr_code_page %}">this page</a> again.</p>
    </div>
    {% endblock %}

Step 4
------

Open your root urlconf (the module is specified in the ROOT_URLCONF setting) and include the URLs used by the qrauth application:

    urlpatterns = patterns('',
        # …
        url(r'^qr/', include('qrauth.urls')),
        # …
    )

Configuration
=============

You may also want to set a custom expiration time for the authentication QR codes. By default, the QR codes are valid for 300 seconds (5 minutes). If you want to change this, set any other value (in seconds) for the AUTH_QR_CODE_EXPIRATION_TIME setting. For example:

    AUTH_QR_CODE_EXPIRATION_TIME = 600 # Ten minutes

If you want to specify the page where the user should be redirected after they successfully sign in using a QR code, you have to set the URL using the AUTH_QR_CODE_REDIRECT_URL setting. For example:

    AUTH_QR_CODE_REDIRECT_URL = "/welcome/"

By default, the user is redirected to "/" (which is usually the index page).

Also, make sure that [LOGIN_URL](https://docs.djangoproject.com/en/dev/ref/settings/#login-url) has a correct value. Otherwise, users can be redirected to a page that does not exist (for example, if someone who is not authenticated tries to open the page with the QR code).

How to test
===========

If you want to test this locally, make sure that your locally run web server is available from your mobile device. For example, if your computer and your mobile device are both connected to same LAN, you should specify your LAN IP address (like 192.168.0.5:8000 or 0.0.0.0:8000 in case you want the web server to listen on all network interfaces) so the web server will listen on this address.

If you use [the “sites” framework](https://docs.djangoproject.com/en/dev/ref/contrib/sites/) (django.contrib.sites), make sure that you have correcly set the domain for the current site.

For example, if your LAN IP address is 192.168.0.5 and the development server is listening on port 8000, the domain should be 192.168.0.5:8000. You can set it in the admin interface (/admin/sites/site/).

If you don’t have the “sites” framework enabled, the current site’s domain will be dynamically determined based on the “Host” header (the get_host() method of the HttpRequest object is used in this case), so even if the development server is listening on both loopback interface and the LAN interface, you should open the website using the LAN IP address (otherwise your mobile device won’t be able to browse to the authentication URL as a loopback interface’s IP will be used in the link).

Now it’s time to try the QR code authentication. Make sure that you are logged in, browse to /qr/ (or use other path if you have specified something else in your root urlconf), pick up your mobile device and try to scan it.

A note on HTTP/HTTPS
====================

If your web server is behind a reverse proxy (like nginx) and you use SSL for your website, please make sure that the upstream (the web server that you use to run your Django website) is being informed about that, so request.is_secure() will act correctly (so the authentication URLs will have correct scheme). You can do that by adding the [SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header) setting and supplying the corresponding header from the reverse proxy (but don’t forget to _always_ set or strip this header, in all the requests the reverse proxy sends to the upstream: otherwise, say, if your website is available via both HTTP and HTTPS, then a user who opens the website via HTTP will be able to set this header at the client side, so request.is_secure() will return True, which is not good from the point of security).
