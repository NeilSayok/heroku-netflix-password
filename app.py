from flask import Flask, request, redirect, url_for
import selenium_netflix as sn

app = Flask(__name__)


@app.route('/')
def index():
    return sn.getCuttentPassword()


@app.route('/change_password')
def get_change_password():
    return sn.sel()


@app.route('/update_password', methods=['GET'])
def update_password():
    set_pass = request.args.get('pass')
    set_num = request.args.get('newId')
    old_num = request.args.get('oldID')
    if set_pass == '' or set_num == '':
        return redirect(url_for('index'))
    else:
        try:
            sn.updateCurrentPasswordFromDB(set_num,set_pass,old_num)
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
    return '''
    <!DOCTYPE html>
<html>
<head>
    <style>
        table {
          font-family: arial, sans-serif;
          border-collapse: collapse;
          width: 100%;
        }
        td, th {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 8px;
        }

        tr:nth-child(even) {
          background-color: #dddddd;
        }
    </style>
</head>
<body style="background:white;">
<br><br><br><br>
<table>
    <tr>
        <th>Use</th>
        <th>Get Fields</th>
        <th>Link</th>
    </tr>
    
  <tr>
    <td>Change the password if changed manually</td>
    <td><b>pass</b>:The New Password<br>
        <b>newId</b>:The Current Password number to be used<br>
        <b>oldID</b>:The Old Password number to being used<br>
    </td>
    <td><a href="https://netflixpassword.herokuapp.com/update_password">Go to update_password</a></td>
  </tr>

<tr>
    <td>Get the current Password and Index</td>
    <td>N/A</td>
    <td><a href="https://netflixpassword.herokuapp.com/get_curr_pass_txt">Go to get_curr_pass_txt</a></td>
  </tr>
      
      
    
    

</table>
</body>
</html>
    
    
    '''




if __name__ == '__main__':
    app.run()
