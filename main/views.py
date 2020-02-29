from main import app


@app.route('/')
def show_entries():
    message = 'Hello, World!'
    return message
