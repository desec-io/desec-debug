from socket import getaddrinfo


def _resolve(name):
    try:
        return getaddrinfo(name, 53)[0][4][0]
    except OSError:
        print(f'Unknown server: {name}')
        quit(1)


frontend_servers = {
    _resolve(s): s for s in
    [
        'lhr-1.b.desec.io',
        'vie-1.b.desec.io',
        'fra-1.a.desec.io',
        'ams-1.a.desec.io',
        'lax-1.b.desec.io',
        'nyc-1.b.desec.io',
        'dfw-1.a.desec.io',
        'sao-1.a.desec.io',
        'sao-1.b.desec.io',
        'scl-1.b.desec.io',
        'syd-1.a.desec.io',
        'syd-1.b.desec.io',
        'sin-1.b.desec.io',
        'hkg-1.a.desec.io',
        'jnb-1.a.desec.io',
    ]
}
