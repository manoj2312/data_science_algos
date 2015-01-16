import smtplib

# Specifying the from and to addresses

fromaddr = 'manoj.gootam@gmail.com'
toaddrs  = 'spidy7012@gmail.com'

# Writing the message (this message will appear in the email)
msg='Hello Manu'

# Gmail Login

username = 'manoj.gootam'
password = 'nklvdszuaaeotwah'

# Sending the mail  

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()