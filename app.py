from flask import Flask, render_template, request  # pip install Flask
from import_tweets import streaming
# from event_detection import get_events
# from sentiment_analysis import sentiment_analysis
# Pass in name to determine root path, then Flask can find other files easier

app = Flask(__name__)


# Route - mapping (connecting) a URL to Python function
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        t = streaming(request.form.get('keywords'))
    return render_template("index.html")
# @app.route('/events.html')
# def events():
#      ev=get_events()
#      size=len(ev)-1
#      return render_template("events.html",x=0, ev=ev, len=size)
#
# @app.route('/sentiment.html')
# def sentiment():
#     list = sentiment_analysis()
#     return render_template("sentiment.html", list = list)

#
# @app.route('/enotoriety.html')
# def events():
#
#     return render_template("enotoriety.html")
#

# Runs app only when we run this script directly, not if we import this somewhere else
if __name__ == "__main__":
    app.run(debug=True)
