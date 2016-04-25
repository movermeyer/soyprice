from application import app
import admin
import api
import scheduler
import os


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = os.getenv('PORT', 4000)
    scheduler.init_app(app)
    app.run(host=host, port=port, threaded=True)
