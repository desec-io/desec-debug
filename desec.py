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
        # 'gru-1.a.desec.io',  # TODO see what's the true name of this server
        # 'gru-1.b.desec.io',  # TODO see what's the true name of this server
        'scl-1.b.desec.io',
        'syd-1.a.desec.io',
        'syd-1.b.desec.io',
        'sin-1.b.desec.io',
        'hkg-1.a.desec.io',
        'jnb-1.a.desec.io',
    ]
}
