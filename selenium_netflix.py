from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import sys
from flask import redirect, url_for
import smtplib
from socket import gaierror
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import psycopg2
from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as SeleniumException
from datetime import datetime
from selenium.webdriver.common.by import By
from inspect import currentframe


port = 587
smtp_server = "smtp-relay.sendinblue.com"
login = "sdmsdm1998@gmail.com"
password = "T0Hn89ZkyYUP5s3E"
sender = "sdmsdm1998@gmail.com"
receiver = "sayokdeymajumder1998@gmail.com"


def write_to_file(driver):
    with open("file.html", "w", encoding="utf-8") as fh:
          now = datetime.now().strftime("%B %d, %Y %H:%M:%S")
          fh.write(f"<p style='display:block;color:red;'>{now}</p>\n")
          fh.write(driver.page_source)

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno


def sendMail(nf_password):
    message = f"""\
       Netflix password has been changed the current password is:\n{nf_password}"""

    msg = MIMEMultipart()

    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Current Password : " + nf_password

    msg.attach(MIMEText(message, 'plain'))

    try:
        # send your message with credentials specified above
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(login, password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())

        # tell the script to report if your message was sent or which errors need to be fixed
        print('Sent')
    except (gaierror, ConnectionRefusedError):
        print('Failed to connect to the server. Bad connection settings?')
    except smtplib.SMTPServerDisconnected:
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))


def getDriver():
    if sys.platform == 'win32':
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1200x600')
        options.add_argument('--disable-notifications')

        # options.add_argument("--headless")
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--example-flag")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-notifications")

        return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


def getCurrentPasswordFromDB():
    conn = psycopg2.connect(database="dd2nqu4a7q86gk",
                            user="mbadltkqhsmdjk",
                            password="c8028c42ec3eab6b75d3555b439ce1dfcb3798031965ff0ca4ae249a2a30a36f",
                            host="ec2-50-19-26-235.compute-1.amazonaws.com",
                            port="5432")
    cur = conn.cursor()
    cur.execute(f"SELECT * from currentpassword")
    record = cur.fetchall()
    conn.commit()
    conn.close()
    return record[0]


def updateCurrentPasswordFromDB(newID, newPass, oldID):
    conn = psycopg2.connect(database="dd2nqu4a7q86gk",
                            user="mbadltkqhsmdjk",
                            password="c8028c42ec3eab6b75d3555b439ce1dfcb3798031965ff0ca4ae249a2a30a36f",
                            host="ec2-50-19-26-235.compute-1.amazonaws.com",
                            port="5432")
    cur = conn.cursor()
    cur.execute(f"UPDATE currentpassword SET id = '{newID}',password='{newPass}' WHERE id = {oldID}")
    conn.commit()
    conn.close()

def getNewPasswordFromDB(id=1):
    conn = psycopg2.connect(database="dd2nqu4a7q86gk",
                            user="mbadltkqhsmdjk",
                            password="c8028c42ec3eab6b75d3555b439ce1dfcb3798031965ff0ca4ae249a2a30a36f",
                            host="ec2-50-19-26-235.compute-1.amazonaws.com",
                            port="5432")
    cur = conn.cursor()
    cur.execute(f"SELECT password from allpasswords where id = '{id}'")
    rec = cur.fetchall()
    conn.commit()
    conn.close()
    return rec[0][0]


def getCuttentPassword():
    current_pass = getCurrentPasswordFromDB()[1]
    with open("static/home.html", "r") as index:
        html = index.read()
        html = html.replace("%%##PASS##%%", current_pass)
        html = html.replace("assets/", "static/")
    return html



def sel():
    passTup = getCurrentPasswordFromDB()

    current_pass = passTup[1]
    num = int(passTup[0])

    new_pass = getNewPasswordFromDB(num).strip()

    driver = getDriver()
    driver.delete_all_cookies()
    driver.get("https://www.netflix.com/clearcookies")
    driver.get("https://www.netflix.com/login")
    wait = WebDriverWait(driver, 600)
    # id_userLoginId

    write_to_file(driver)

    print(f"Line:{get_linenumber()} Link:{driver.current_url}")
    try:
        id_box = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[1]/div/div/label/input')
    except SeleniumException.NoSuchElementException:
        try:
            id_box = driver.find_element_by_id("id_userLoginId")
        except:
            id_box = driver.find_element_by_id("userLoginId")
            write_to_file(driver)
    
    print(f"Line:{get_linenumber()} Link:{driver.current_url}")
    try:
        pass_box = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div/div/label/input')
    except SeleniumException.NoSuchElementException:
        try:
            pass_box = driver.find_element_by_id("id_password")
        except:
            pass_box = driver.find_element_by_id("password_toggle")
            write_to_file(driver)

    id_box.send_keys("cloud.iot98@gmail.com")
    pass_box.send_keys(current_pass)

    # login-button
    print(f"Line:{get_linenumber()} Link:{driver.current_url}")
    try:
        login_btn = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/div[1]/form/button")
    except SeleniumException.NoSuchElementException:
        login_btn = driver.find_element_by_class_name("login-button")
        write_to_file(driver)

    login_btn.click()

    print(f"Password: {current_pass} ")
    print(f"Line:{get_linenumber()} Link:{driver.current_url}")

    try:
        wait = WebDriverWait(driver,1200)
        wait.until(lambda d: d.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/span/a'))
    except Exception as e:
        write_to_file(driver)
        print(e)


    # driver.execute_script("window.open('');")
    # driver.switch_to.window(driver.window_handles[1])

    # driver.get("https://www.netflix.com/password")
    print(f"Line:{get_linenumber()} Link:{driver.current_url}")

    while True:
        try:
            driver.get('https://www.netflix.com/password')
            driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/form/ul/li[4]/div/label")
            break
        except Exception as e:
            write_to_file(driver)
            print(e)
            pass
    WebDriverWait(driver, 600)
    WebDriverWait(driver, 600)
    # print(driver.page_source)
    # return (driver.page_source)

    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/form/ul/li[4]/div/label").click()

    old_pass_inp = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div/form/ul/li[1]/div/div/label/input')
    new_pass_inp = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div/form/ul/li[2]/div/div/label/input')
    renew_pass_inp = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div/form/ul/li[3]/div/div/label/input')

    old_pass_inp.send_keys(current_pass)
    new_pass_inp.send_keys(new_pass)
    renew_pass_inp.send_keys(new_pass)

    print(f"Line:{get_linenumber()} Link:{driver.current_url}")

    for _ in range(0, 5):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div[1]/button[1]").click()
            break
        except Exception as e:
            print(e)
            write_to_file(driver)

    print(f"Line:{get_linenumber()} Link:{driver.current_url}")

    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/form/div/button[1]').click()

    if num >= 5000:
        newID = 1
    else:
        newID = num + 1
    updateCurrentPasswordFromDB(newID=newID, newPass=new_pass, oldID=num)
    num += 1

    try:
        sendMail(new_pass)
    except:
        pass

    return redirect(url_for('index'))
