from flask import Flask, render_template, request  # pip install Flask
from import_tweets import streaming
# Pass in name to determine root path, then Flask can find other files easier

app = Flask(__name__)

# Route - mapping (connecting) a URL to Python function
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        t=streaming(request.form.get('keywords'))
    return render_template("index.html")

@app.route('/tweets.html')
def tweets():
    return render_template("tweets.html")
# Runs app only when we run this script directly, not if we import this somewhere else
if __name__ == "__main__":
    app.run(debug=True)
