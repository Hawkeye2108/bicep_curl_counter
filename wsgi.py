# from server import app

# if __name__ == "__main__":
#     app.run()



from server import app
from waitress import serve

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
