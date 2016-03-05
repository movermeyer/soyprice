from application import app
import config
import admin
import api
import scheduler
import os


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = os.getenv('PORT', 5000)
    scheduler.init_app(app)
    app.run(host=host, port=port, threaded=True)
