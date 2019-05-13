# -*- coding: utf-8 -*-
from taobao import app,db
from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app=ProxyFix(app.wsgi_app)



if __name__ == '__main__':
    app.run(debug=False)
    db.create_all()
