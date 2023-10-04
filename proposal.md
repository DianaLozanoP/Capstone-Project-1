# Capstone 1 Proposal 

Step Two of your first capstone is all about fleshing out your project idea.  


For this step,please write a proposal based on the project idea you agreed on with your mentor. This
proposal should be a 1-2 page document that answers the following questions:  

1. What goal will your website be designed to achieve?  
To calculate the net amount of money a person will receive after provincial deductions and federal deductions in Canada.  

2. What kind of users will visit your site? In other words, what is the demographic of
your users?  
Any person who works full-time, who gets paid either hourly or yearly. A person between 18-60, it can either female or male living in Canada.

3. What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.  
The data that will be used is GST (Global sales tax), PST(Provincial sales tax) and HST (Harmonized sales tax).
The API documentation:[salestaxapi](https://salestaxapi.ca)  


4. In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). Answer questions like the ones below, but feel free to add more information:
   a. What does your database schema look like?  
     *Provincial specific taxes table
     *Federal taxes table
     *Users table

b. What kinds of issues might you run into with your API?
I might get discrepancies in the data obtained.

c. Is there any sensitive information you need to secure?  
If user enters its salary, it should be secured.   

d. What functionality will your app include?  
 *Log in, log out. 
 *Gross calculation.
 *Net calculation.
 *List of deductions.

e. What will the user flow look like?
Log in, select province, select multiple variables(i.e. hourly wage or salary, frequency, numbers or hours) to send a form which will break down tax deductions and log out.
