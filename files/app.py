#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle

import util

app = application = bottle.Bottle()


@bottle.post('/')
def index_post():
    email = bottle.request.forms.get("email")

    util.send_system_state(email)
    return bottle.template("index")

@bottle.get('/')
def index_get():
    return bottle.template("index")

class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

if __name__ == "__main__":
    bottle.run(host='0.0.0.0', port=8081, debug=True)
