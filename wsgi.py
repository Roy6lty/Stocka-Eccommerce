from src import create_app
from config import config
app = create_app('Base')

if __name__ == '__main__':
    app.run()