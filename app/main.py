from flask import Flask
from flask import request,flash
from flask import render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

app= Flask(__name__)
app.secret_key = b'_5#y2L"f4Q8z\n\xec]/'

participantDict = {}

NUMBER_OF_CANDIDATES = 8

senderNameToReceiverEmailDict = {}

senderNameToReceiverNameDict = {}

def sendEmailToParticipants():
	for senderName, receiverEmail in senderNameToReceiverEmailDict.items():
		#gmail works
		botAddress = 'yourmail'
		botPassword = 'mailPassword'

		mail_content = ''' Sevgili ''' + senderNameToReceiverNameDict[senderName] + ''', 
		Bu yıl '''+ senderName+ '''  na hediye alacaksin!.

		En fazla alabileceğin hediye limiti 50 liradır. 

		Sevgilerimle en sevdiğiniz arkadaşınız'''

		# english part 
		# mail_content = ''' Dear ''' + senderNameToReceiverNameDict[senderName] + ''', 
		# This year you will buy gift to '''+ senderName+ '''  !.

		# Maximum cost of present limited to 50 dollars . 

		# Sincerly your best friend''' 
		message = MIMEMultipart()
		message['From'] = botAddress
		message['To'] = receiverEmail
		message['Subject'] = 'Yılbaşı Çekilişi Hk.'  
		message.attach(MIMEText(mail_content, 'plain'))
		session = smtplib.SMTP('smtp.gmail.com', 587)
		session.starttls() 
		session.login(botAddress, botPassword)
		session.sendmail(botAddress, receiverEmail, str(message))
		session.quit()
		print('Succesfully Sent')


def matchPeople():
	# for each member in the gift pool assign possible candidates and select someone to give present 

	receiverList = []
	for senderName, senderEmail in participantDict.items():
		candidateList = []
		for name, email in participantDict.items():
			candidateList.append(name)

		candidateList.remove(senderName)
		
		for name in receiverList:
			print(name) 
			try:
				candidateList.remove(name)
			except:
				continue

		receiverName = random.choice(candidateList)
		senderNameToReceiverEmailDict[senderName] = participantDict[receiverName]
		senderNameToReceiverNameDict[senderName] = receiverName
		receiverList.append(receiverName) 
	
	# debug if all candidates matched correctly i.e no duplicates,self-assign etc.
	for senderName, receiverEmail in senderNameToReceiverEmailDict.items():
		print("sender name: "+senderName+ " receiver email: " + receiverEmail )



#check whether exact number of candidates submit their name-mail combinations
#if all people sent their name-mail combinations match people and send results to them  
@app.route('/',methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		name = request.form.get("inputName")
		email = request.form.get("inputEmail")
		if participantDict.get(name) is None :
			participantDict[name] = email 
		if(len(participantDict) == NUMBER_OF_CANDIDATES):
			matchPeople()
			sendEmailToParticipants()
			flash( "Tüm katılımcılar basarı ile katıldı, mailleriniz gönderildi")
			return render_template('index.html')
		elif(len(participantDict) > NUMBER_OF_CANDIDATES):
			flash( "Tüm katılımcılar basarı ile katıldı, mailleriniz gönderildi")
			return render_template('index.html')
		else:
			print("name " + name +" email " +  participantDict[name]  )
			flash ("Emailiniz alındı tüm katılımcılar maillerini girdikten sonra kime hediye alacağınız mailinize gönderilecektir.") 
			return render_template('index.html')
	else:
		return render_template('index.html')


