import musicbrainzngs


def musicbrainzngs_setup():
    musicbrainzngs.set_useragent(
        "AnChain",
        "0.1",
        "https://github.com/GiovanniGabbolini/",
    )
    # musicbrainzngs.set_hostname('192.168.1.4:5000')
    musicbrainzngs.set_rate_limit(limit_or_interval=False)
    # musicbrainzngs.set_hostname('localhost:5000')
