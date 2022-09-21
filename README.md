# Proposals
My ideas for my final project are...

1. I would like to create a simple COVID Protocol Violation Detection System. 
It will help officials to detect people without face masks.
It will also help officials to detect people not maintaining physical distance,thereby controlling the crowds.
I will use the OpenCy library to build this system.
For the project, I will highlight the people without masks or people not maintaining social distance in the video.


2.Implementing 2-Factor Authentication using Python. 
There will be a login and register functionalities for this which I will execute using Postman.
If the register method is executed, users will be asked to enter basic details like name, email and password. I will check the password strength and if it's valid, then I’ll store the data in a csv file.
Passwords will be encrypted using any of the encryption algorithms and any cryptography libraries of python like Fernet.
If the login method is executed, the user authenticates themselves using email and password which is already stored in the csv file. The platform confirms user information and asks for second authentication through an OTP sent to email.  
I will use the PyOTP library for the OTP authentication and this authentication will be time-based.


3. Segregate/Move files to respective folders based on their type.
The code will continuously monitor a folder where random files are being added/created like the Download Folder.
Whenever a file is added to the folder, the program will get triggered and will read the file type and move the file to its correct folder
For example, if an image file is downloaded, then I will move the file to the ‘Pictures’ folder and if a document is downloaded, then I will move it to the ‘Documents’ folder.


Execution Plan :
Week 4: I'll install all the required libraries for my project and start off the project with reading and writing user data from postman.
Week 5: I'll learn how to do the encryption and decryption of passwords and validating password strength and start to implement them in my project. 
Week 6: Implementation of 2-factor authentication (sending OTP and validating it using python libraries). 
Week 7: Testing all functionalities including login,registration and 2-factor authentication.
Week 8: I'll keep this week as buffer and if time permits, I'll develop a UI for my project and integrate it with already developed functionalities.


Requirements for/Steps to run the Project:
1. Google Authenticator App is required on your smartphone.
2. Python libraries used in the project are to be installed (I have included a subprocess method to install the libraries in my python code so the libraries should get automatically installed when the code is run).
3. sqlite3 is a inbuilt module for python3 and hence I did not include a install command for it.
4. When the main python file is run (app.py), system will check and install libraries that are not already installed and hence the url for the host is lost in the command line. Please scroll up a little to get the host URL ( Here is the host link in case you don't find it : http://127.0.0.1:5000/)
5. Please use 'python3 app.py' command to run the python file. Using 'python app.py' might throw a error.

