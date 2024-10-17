from flask import Flask, render_template
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
