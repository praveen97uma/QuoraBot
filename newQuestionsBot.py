from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from datetime import datetime

import time
import smtplib
from pyvirtualdisplay import Display
import config

def loginIntoQuora(email, password):
    browser = webdriver.Chrome()
    browser.get("http://www.quora.com")
    elem = browser.find_element_by_name("email")
    elem.send_keys(email)
    elem = browser.find_element_by_name("password")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    time.sleep(1)
    return browser

def sendPageDownPressEvents(browser, no_of_page_downs):
    body = browser.find_element_by_tag_name("body")
    while(no_of_page_downs>0):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        no_of_page_downs-=1
    time.sleep(2)
	
def getNewQuestions(browser):
	questions = []
	question_elems = browser.find_elements_by_class_name("pagedlist_item")
	for q_elem in question_elems:
		question_tip_elem = q_elem.find_element_by_class_name("feed_item_title")
		if "Question added" in question_tip_elem.text:
			ques_link_elem = q_elem.find_element_by_class_name("question_link")
			ques_link = ques_link_elem.get_attribute("href")
			ques_text_elem = q_elem.find_element_by_class_name("link_text")
			ques_text = ques_text_elem.text
			topics = []
			topics_elem = q_elem.find_elements_by_class_name("topic_name")
			for topic_elem in topics_elem:
				topic_link = topic_elem.get_attribute("href")
				topics.append(topic_link)
				print "Topic",topic_link
			questions.append({"link":ques_link, "text": ques_text, 'topics':topics})
	return questions

def prepareEmailBody(data):
	body = ""
	for question_data in data:
		topics = question_data["topics"]
		topics = ['<a href="%s" style="text-decoration:none;font-size:12px;color:#666;font-weight:bold">%s</a>'%(topic, topic.split("/")[-1]) for topic in topics]
		topics = ', '.join(topics) +"<hr>"#+ "<br/><br/>"
		ques_body = '<a href="%s" style="text-decoration:none;color:#19558d;font-weight:bold;font-size:14px">%s</a><br/>'%(question_data["link"], question_data["text"])
		ques_body = ques_body + topics
		body += ques_body
	return body
	
def send_mail(data):
	mail_server = smtplib.SMTP(config.GMAIL_SMTP_HOST, config.GMAIL_SMTP_PORT)
	#mail_server.set_debuglevel(0)
	mail_server.ehlo()
	mail_server.starttls()
	mail_server.login(config.GMAIL_USERNAME, config.GMAIL_PASSWORD)
	
	body = prepareEmailBody(data)
	current_time = "<p><b>Time:</b> %s</p>"%(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	body = current_time + body
	headers = config.EMAIL_HEADERS                   
	email_content = headers + "\r\n\r\n" + body
	print "Sending mail"
	mail_server.sendmail(config.GMAIL_USERNAME, config.RECIPIENT_ADDRESS, email_content)
	mail_server.quit()

def fetchAndMailNewQuestions(disable_display=True):
    if disable_display:
        display = Display(visible=0, size=(1024, 768))
        display.start()
	browser = loginIntoQuora(config.QUORA_USERNAME, config.QUORA_PASSWORD)
	sendPageDownPressEvents(browser, config.NO_OF_PAGEDOWNS)
	questions = getNewQuestions(browser)
	browser.quit()
	send_mail(questions)    
			
if __name__=='__main__':
    fetchAndMailNewQuestions()
