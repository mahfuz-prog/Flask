from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse
from flask import url_for, request


def login_url(login_view, next_url=None, next_field="next"):
    base = expand_login_view(login_view)

    if next_url is None:
        return base

    parsed_result = urlparse(base)
    md = url_decode(parsed_result.query)
    md[next_field] = make_next_param(base, next_url)
    netloc = current_app.config.get("FORCE_HOST_FOR_REDIRECTS") or parsed_result.netloc
    parsed_result = parsed_result._replace(
        netloc=netloc, query=url_encode(md, sort=True)
    )
    return urlunparse(parsed_result)

def expand_login_view(login_view):
    if login_view.startswith(("https://", "http://", "/")):
        return login_view

    return url_for(login_view)

def make_next_param(login_url, current_url):
    l_url = urlparse(login_url)
    c_url = urlparse(current_url)

    if (not l_url.scheme or l_url.scheme == c_url.scheme) and (
        not l_url.netloc or l_url.netloc == c_url.netloc
    ):
        return urlunparse(("", "", c_url.path, c_url.params, c_url.query, ""))
    return current_url

url = expand_login_view('http://localhost:5000/hola')
print(url)
log_url = login_url('hola')
print(log_url)
