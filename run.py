from waitress import serve
from app import app

if __name__ == "__main__":
    print(f'Running on port {8000}')
    serve(app, host="127.0.0.1", port=8000)
    
