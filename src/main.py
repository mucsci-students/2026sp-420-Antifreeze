from flask import Flask, render_template, url_for, send_from_directory

app = Flask (__name__, template_folder="view/templates", static_folder="view/static")

@app.route ("/")
def index ():
    return render_template ("index.html")

# Custom js path
@app.route('/controller/<path:filename>')
def custom_static (filename):
    return send_from_directory ('controller/',filename)

if __name__ == "__main__":
    app.run (debug=True)
