from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/report')
def success():
   return 'welcome hello world'

@app.route('/report',methods = ['POST', 'GET'])
def report():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success'))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success'))

if __name__ == '__main__':
   app.run(debug = True)

