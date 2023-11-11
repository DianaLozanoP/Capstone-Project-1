## Capstone 1 Proposal 

Step Two of your first capstone is all about fleshing out your project idea.  

For this step,please write a proposal based on the project idea you agreed on with your mentor. This
proposal should be a 1-2 page document that answers the following questions:  

1. What goal will your website be designed to achieve?  

2. What kind of users will visit your site? In other words, what is the demographic of
your users?  

3. What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.  

4. In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). Answer questions like the ones below, but feel free to add more information:
   
   a. What does your database schema look like?
   b. What kinds of issues might you run into with your API?
   c. Is there any sensitive information you need to secure?  
   d. What functionality will your app include?
   e. What will the user flow look like?  

### MY CAPSTONE PROJECT IS A BUDGET-TAX CALCULATOR

The goal of the website is to help users with their personal finances by creating budgets and also by calculating their net income after taxes (Canadian provinces only for now). It will have a simple design that is visually attractive so the user feels motivated to keep track of their finances. The demographics for this project is anyone who is looking to keep track of their finances in a simple way to achieve their goals. 

The plan is to retrieve data from a tax API called [salestaxapi](https://salestaxapi.ca) . This API will provide all the data related to currenlty salary/wage deductions taking place in Canada. The idea is to show users how much will be deducted from their paycheque. Then, to show deatils about the amounts that are going to Federal Tax, Canadian Pension Plan, Employment Insurance, etc. The website will also have an option to add extra deductions (i.e. Extra health benefits,  Register Retirement Pension Plan, Deferred Profit Sharing Plan). The main focus of the project is actually to create a personalized budget, but the taxes API option will be there for any users interested in using both tools at the time. 

The database will be structured around the users. Possible tables for the data base will be:
*Users Table
*Budgets Table
*Wallets Table
*Net Incomes Table  

The possible issues I might run into my API is to get the wrong tax information for the specific users. Also I have to make sure to handle the API response appropriately, if I get JSON then make sure to handle that answer before it goes back to the User on the website.
In this case, since we are taking about finances, the information is sensitive and it is important to make sure that passwords are encrypted.

The user experience is supposed to be something like this: 
1. Allow user to sign up or sign in.
2. Dashboard will be displayed. Amount spend and amount remaining will be showed on the main page, also couple of graphs which will make the experience visually easier. The graphs will be for current monthly expenses (pie chart), tracking of the year expenses month by month(bar graph) and then an extra optional graph, a compound interest and monthly contribution growth based on SP500 investing for a 15-20 years period (linear graph). This last graph is supposed to motivate the user to keep saving and investing every month.
3. Net Income page. This is where the API calls take place. There will be a form to be filled by user. Then the API call will take place, and net income will be given back. Options to include extra deductions will appear on the page. As well as, options to include extra side incomes. At the bottom there will be a total net income amount for that month or biweekly.
4. Budgets page. In this section user will be able to create new budgets through a form adding their category and amount to be spent.
 


