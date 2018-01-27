#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import app
# app.run(host = '127.0.0.1', port = 9800, debug = True)
# app.run(host = '127.0.0.1', port = 9800, debug = False)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug = False)