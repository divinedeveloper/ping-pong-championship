# ping-pong-championship
A Microservices based virtual Ping-Pong championship which features 8 players and 1 referee (all 9 implemented as distinct applications). The 8 players will be instances of the same app, with different attributes, defined in an external file

Core Requirements:-

    - Ubuntu 14.04, Python 2.7.9, git 1.9.1, Mysql 5.6, Jenkins 2.74, pip and virtual env 

    - Postman for running API's
    
#MySql Database Setup:-

#Login using 

    - mysql -u root -proot 

#Create Database

    - create database ping_pong

#Project Setup

#Clone GitHub repository

    - git clone https://github.com/divinedeveloper/ping-pong-championship.git

#Create virtual env for first time only

    - cd ping-pong-championship/

    - virtualenv env


#Activate virtual env from second time

    - source env/bin/activate


#Install requirements 

    - pip install -r requirements.txt
    
#Run Migrations

    - cd referee_service
    
    - python manage.py makemigrations
    
    - python manage.py migrate

#Free Ports for servers
      
      - If ports 8000 and 8001 are used free them using commands kill $(lsof -t -i:8000) and kill $(lsof -t -i:8001)
    
#Installing Jenkins CI

    - sudo sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
    
    - wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
    
    - sudo apt-get update
    
    - sudo apt-get install jenkins
    
    - sudo service jenkins status
    
    - Go to localhost:8080
    
    - After pasting password, select install plugins manually & select Github plugin in addition to other preselected plugin
    
    - Create Admin user with username and password

#Jenkins CI setup after logging in as admin

#make Jenkins user owner of project directory to execute job

    - sudo chown -R jenkins . 
    
     - From Jenkins dashboard click on create new jobs

     - item name as Ping Pong Championship and select the “Freestyle project” option
     
     - On the next page, select the “Discard Old Builds” option
     
     - Click on Advance -> Select Use custom workspace -> paste in directory -> full path till project directory (eg. /home/devuser/projects/ping-pong-championship/)
     
     - In soure code Mgmt select -> git -> repo Url -> https://github.com/divinedeveloper/ping-pong-championship.git ->      Add -> enter credentials. In Branches to build use -> */master
     
    - In Build -> Add Build step -> Select Execute Shell -> Paste following script
          
          #!/bin/bash

          #activate virtual env
    
          source env/bin/activate

          #install requirements

          pip install -r requirements.txt

          #project directory

          cd player_service/

          #run server
          BUILD_ID=dontKillMe python manage.py runserver 8001 &

          cd ../referee_service 
          BUILD_ID=dontKillMe python manage.py runserver &

    - Save the Project configuration
    
    - Click Build Now to manually trigger job and start servers for both microservices
    
#Access REST API's through Postman

    - https://www.getpostman.com/collections/e5dcfd1082fd305b7595
   
#Play Game
        
    - On successful build Play the Game by importing Postman API collection
    
    - Game flow is defined by the order of API's in Postman collection
    
    - If you feel stuck or what to do next Run Get Referee Instructions Api
   







