def getgrades():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import smtplib
    from email.mime.text import MIMEText
    import datetime
    import time
    from module import passDecode
    gradesrightnow = []
    assignmentnumber = []
    global gradesrightnow
    global assignmentnumber
    username = 'REDACTED'
    password = passDecode('[REDACTED]')
    browser = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
    browser.get("https://focus.pcsb.org")
    browser.find_element_by_name("username").clear()
    browser.find_element_by_name("username").send_keys(username)
    browser.find_element_by_name("password").clear()
    browser.find_element_by_name("password").send_keys(password)
    browser.find_element_by_name("password").send_keys(Keys.RETURN)
    gradeids = ['2018202', '2018185', '2018223', '2018626', '2018473', '2018871', '2018886']
    currentgrades = []
    assignments = []
    global currentgrades
    global assignments
    for x in range(0, len(gradeids)):
        try:
            gradeurl = "https://focus.pcsb.org/focus/Modules.php?modname=Grades/StudentGBGrades.php?course_period_id="
            gradeurl += gradeids[x]
            browser.get(gradeurl)
            grade = browser.find_element_by_id("currentStudentGrade[]").get_attribute('innerHTML').encode('utf8')[0:3]
            if grade[2] != "%":
                grade = browser.find_element_by_id("currentStudentGrade[]").get_attribute('innerHTML').encode('utf8')[0:4]
            if grade[1] == "%":
                grade = browser.find_element_by_id("currentStudentGrade[]").get_attribute('innerHTML').encode('utf8')[0:1]
            currentgrades.append(grade)
            for x in range(8, 12):
                global assignmenttotal
                assignmenttotal = browser.find_element_by_id("lo_controls").get_attribute('innerHTML')[7:x].encode('utf8')
                if assignmenttotal[(len(assignmenttotal) - 1)] == '&':
                    assignmenttotal = browser.find_element_by_id("lo_controls").get_attribute('innerHTML')[7:(x-1)].encode('utf8')
                    break
            assignments.append(assignmenttotal)
        except Exception:
            currentgrades.append('No assignments found')
            continue
    if datetime.datetime.now().hour == 22 and datetime.datetime.now().minute < 10:
        email(1)
        return
    elif gradesrightnow != currentgrades and len(gradesrightnow) == 7:
        email(2)
        return
    elif assignmentnumber != assignments and len(assignmentnumber) == 7:
        email(2)
        return
    else:
        gradesrightnow = currentgrades
        assignmentnumber = assignments
        return

def email(oneortwo):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import smtplib
    from email.mime.text import MIMEText
    import datetime
    import time
    English = "English: " + currentgrades[0]
    Algebra = "Algebra 2: " + currentgrades[1]
    History = "US History Honors: " + currentgrades[2]
    Spanish = "Spanish 2: " + currentgrades[3]
    Human = "AP Human Geography: " + currentgrades[4]
    Biology = "Biology 1: " + currentgrades[5]
    Inquiry = "Inquiry Skills: " + currentgrades[6]
    if oneortwo == 1 or oneortwo == 2:
        if oneortwo == 1:
            msg = "Hello, {name}!\n\nHere are your current grades:\n\n" + English + "\n" + Algebra + "\n" + History + "\n" + Spanish + "\n" + Human + "\n" + Biology + "\n" + Inquiry + "\n\n" + "If you have any concerns, please note that this is just you talking to yourself (because I'm that cool), so you may want to contact a teacher or just anybody else."
        if oneortwo == 2:
            msg = "Hello, {name}!\n\nYour grades have changed!  It is absolutely incumbent upon you (if you're still on the first vocab list, you just got to practice a vocab word, yay) to check Focus immediately (https://focus.pcsb.org).  However, because there's no way you can wait for it to load before you see numbers, here are your current grades:\n\n" + English + "\n" + Algebra + "\n" + History + "\n" + Spanish + "\n" + Human + "\n" + Biology + "\n" + Inquiry + "\n\n" + "If you have any concerns, please note that this is just you talking to yourself (because I'm that cool), so you may want to contact a teacher or just anybody else."
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.ehlo()
        server.login('[REDACTED]', passDecode('[REDACTED]'))
        server.sendmail('[REDACTED]', '[REDACTED]', msg)
        if oneortwo == 1:
            time.sleep(660)

def main():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import smtplib
    from email.mime.text import MIMEText
    import datetime
    import time
    while True:
        getgrades()
        time.sleep(600)
