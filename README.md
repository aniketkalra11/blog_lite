# blog_lite
Stuend id: 21f3002102@student.iitm.ac.in
blog lite application development for project september tearm
Requirements:- 
1. Flask, Jinja2, Flask_session and BootStrep Minimal css precompiled file for basic aesthtics
(please refer requirement.txt for more details)


*** Before Running the application Please ensure that Following Files Must exists
1. app.py in root directory
2. Model/user_model_controller.py & post_model_controller.py in model directory
3.Controller/user_controller & post_controller in controller folder

######You must in the same directory in which app.py is placed

Plese Follow instruction for start application
1. python3 app.py
# Application by default we be activated for machine pc and can be accessed via 'http://localhost:5000/'

2. now open any web browser ('Google Chrome or Firefox prefered') and type following address in the urlbar 'http://localhost:5000/'
#Now application login page should be visible to you if not, Please check app.py is running properly or you entered the correct address

3. If you are new, please select signup otherwise enter your login credential and click on signin
# if your credential are correct then you will be redirected to dashboard otherwise a proper alert message will published

4. If your are new Please click on signup then click on signup
#A new signup form will be displayed

5. Enter your basic details and like name, userid, password, dob etc..
# if user form validation success the you will be redirected to signin page for login 

6. After Successful signup Please enter your userid and password
# if your user id and password is correct then you will be redirected to Dashboard otherwise prompted with proper error

7. Your Dashboard will contain all the posts in cronological order 
# You can like dislike and comment on post And If your Dashboard is empty then you are prompted with Message to Follow Users 

8. In the Navigation Bar you can search for users 
# It supports string matching which means if you are trying to search for 'Aniket' then Simply 'Ani' will provide you same results
  #On Search result Page 
  8.1 You can Follow/UnFollow user
  8.2 Your dashboard will be updated on the basis of your following list

9. In the profile section you can manage your posts
# ACTIONS WHICH ARE PERMITTED
 #1. Edit your post
 #2. Delete your post
 #3. Add profile photo

10. In profile Section you can view your follower list Following list and can update your profile details like:
  #Name, city, Profession

11. An 'ADMIN' User can Watch all the posts delete the posts and delete the user 

#12. CRUD Api on user and posts
  12.1 A user can me made admin only via API command there is not gui provided for user conversion
    Once use become ADMIN he/she can able to delete use update user and delete the entire post but cannot update the post
  12.2 Using Api we can retrive list of blogs made by an user
  12.3 retrive any posts details and url of image
  12.4 Comment, Like and Delete Blog. // UnderConstruction
  12.5 Please refer Api.yaml file for futhre details
 
  
  
  
    
  


