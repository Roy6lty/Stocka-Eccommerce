from src import create_app
from config import config
app, celery = create_app('Base')
app.app_context().push()


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port = 5000)



    