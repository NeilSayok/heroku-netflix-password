from flask import Flask, request, redirect, url_for
import selenium_netflix as sn

app = Flask(__name__)


@app.route('/')
def index():
    return sn.getCuttentPassword()


@app.route('/change_password')
def get_change_password():
    return sn.sel()


@app.route('/getfile')
def get_file():
    with open("file.txt", "r") as fh:
        lines = fh.readlines()
        out = ""
        for l in lines:
            out += l + "\n"
        return out


@app.route('/update_password', methods=['GET'])
def update_password():
    set_pass = request.args.get('pass')
    set_num = request.args.get('newId')
    old_num = request.args.get('oldID')
    if set_pass == '' or set_num == '':
        return redirect(url_for('index'))
    else:
        try:
            sn.updateCurrentPasswordFromDB(set_num, set_pass, old_num)
            return f"Done {set_pass} @line {set_num}"
        except:
            return "Error"


@app.route('/get_curr_pass_txt')
def get_curr_pass_num():
    passTup = sn.getCurrentPasswordFromDB()
    current_pass = passTup[1]
    num = passTup[0]
    return f"{current_pass}<br>{num}"


@app.route('/links')
def get_links():
    passTup = sn.getCurrentPasswordFromDB()
    with open("static/alllinks.html","r") as fh:
        html = fh.read()
        html = html.replace("assets/", "static/")
        html = html.replace("##oldpass##", f"{passTup[1]}")
        html = html.replace("##oldid##", f"{passTup[0]}")  
    return html
 


if __name__ == '__main__':
    app.run()
