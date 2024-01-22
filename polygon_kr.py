from flask import Flask, render_template

# Flask 애플리케이션 생성
app = Flask(__name__, template_folder='templates')


@app.route('/polygon')
def city():
    return render_template('polygon.html')


if __name__ == '__main__':
    app.run(debug=True)
