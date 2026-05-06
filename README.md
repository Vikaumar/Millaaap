# Milaap

It is a web application that use to obtain the details of family of a lost child using face recognition with 2 step authentication system.
It is built using **Django, OpenCV and Sqlite3 Database** for storing the information of the family.
The webcam is used for scanning the image of the lost child which then search for the similar image in the database.  
When the image of the lost child is found in the database it sends a request to the head of the family member to whether to show the information of the child or not.  
If the head accepts the request, all the information of the child like address, phone nmber etc. will be visible to the person who found the child and  that person's coordinates will also be send to the head of the family for safety purposes.  
This project does not only helps in founding the information of the lost child but also helps in recognizing the information of the people who are caught in any accident or in natural calamity.
