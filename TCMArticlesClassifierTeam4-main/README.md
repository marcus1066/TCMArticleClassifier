# TCMArticlesClassifier

This repository contains the the source code to build a Chinese traditional articles classifier. Keras is used to build a machine learning model with 99% accuracy.

**Capacity**

Python 3.7

tensorflow 2.4



How to  make the project works in pc:

firstly the project runs wirh react as front end and flask as back end.

Front-end :

To config the react automatically using the creat-react-app scaffold by running

                                      npm creat-react-app myapp     

 (note that npm should  be installed in your pc to perform npm command) in the directory you want to run on.

  And then add the page folder in our git system.web/src folder to the src folder of my-app which creact-react-app created, cause it includes the upload page and display page for main viewing and main_home.js to manage the logic to choose the page to display. and substitue the defalut app.js file below src folder  with the app.js in git system.web/src folder

  Connecting of front-end and back-end:

  Setup the proxy:

 adding the SetupProxy file under git src folder to creacting my-app src folder to specifed the router to send


  So that the front-end and back-end are connected because of the setting of router

  Additionally:
    The redis folder and celery is needed for flask to run the task asychronously. Redis as the broker and record the states and info of the current progress of task       celery run the tasks in background thread which is different form the main thread.

  So to start the project:

  You need to go to the redis directory first and input:

                                    redis-server
                                  
 (to reboot redis)
             
  create a new terminal and input: 

                    celery -A app.celery worker -P threads  
                    
( to get celery connecting to redis and prepare to recieve task)


 And then run the back-end flask in a new terminal by:
  
                                    python app.py
                      
(note: the celeryconfig.py contain the config for celery with redis)
              
Finally using :

                                      npm start
                                                        
          
 ( let browzer to render the page and user can upload their csv files to let classifier to classify the articles.)

