import os

app_options = dict(
    port=int(os.environ.get("PORT", 80)),
    debug=True,
    static_path="static",
    template_path="templates",
    xsrf_cookies=True,
    gzip=True,
    cookie_secret="g{.<]Zq6:<D@Qt8E}k4.<62_~BsBMT^6ukc7d2-Zck@^HF_H=R*;S#bvLs_qs[tw7#u&",
    login_url="/login"
)