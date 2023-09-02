from flask_app import app
from flask_app.controllers import user_route, tree_route

if __name__ == "__main__":
  app.run(debug=True)