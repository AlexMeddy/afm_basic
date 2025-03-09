from CMessage import CMessage

msg_test = CMessage()
msg = msg_test.encrypt()
file = open("enc_ff_test.txt","w")
file.write(msg)          
file.close()