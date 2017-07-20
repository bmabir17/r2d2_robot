import picamera
from time import sleep
#Create a instance of the camera
camera = picamera.PiCamera()
cmd_file=open('command.txt','r+')

def detectPipeLine():
	print('Continueous detection')

	while(True):
		
		#print(c)
		## The raspi will wait for command from the client raspberry.
		## It acts as a socket server
		
		cmd_string=cmd_file.readline() ##for testing#######Remove when in production
		print (cmd_string)
		#print(cmd_string)
		if(cmd_string=="find_object"):
			c=0
			while(c<9):
				## take images for 9 times, rotating the head
				img_name='cap'+str(c)+'.jpg'
				print(img_name)
				camera.capture(img_name)
				c+=1
			cmd_file.write('done')
		#print('idle')
			
			
detectPipeLine()			


#view a preview
#camera.start_preview()
#sleep(5)
#Take a picture
#camera.capture('cap1.jpg')
#sleep(4)
#stop preview
#camera.stop_preview()
