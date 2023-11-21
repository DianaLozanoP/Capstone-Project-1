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

The goal of the website is to help users with their personal finances by creating budgets and also by showing suggestions of Mutual Funds and ETFs for the user to consider start investing. It will have a simple design that is visually attractive to motivate the user to keep track of their finances. The demographics for this project is anyone who is looking to keep track of their finances and is also comfortable with technology. 

The plan is to retrieve data from a financial API called [FMP: Financial Modeling Prep](https://site.financialmodelingprep.com/) . This API will provide data about ETFs and Mutual Funds available. The idea is to store a list of ETFs and Mutual Funds inside the database, alongside some basic data for each ETF/MutualFund. Then the user can filter ETFs and MutualFunds based on certain parameters. User will have the option to check updated information. The main idea for this project is to create a budget app with additional financial tools.

The database will be structured around the users. Possible tables for the data base will be:  

 * Users Table
 * Budgets Table
 * Wallets Table
 * ETFs table
 * Mutual Funds Table  

The possible issues I might run into my API is to handle the information incorrectly, when I call for a list of ETFs and Mutual Funds, it will be a long list and it needs to be handled correctly. Also I have to make sure to not overuse the API since its free version it's limited. 
As for security concerns, since we are taking about finances, the personal information from users is sensitive and it is important to make sure that passwords are encrypted, routes are authenticated and database are sanitized. 

The user experience is supposed to be something like this: 
1. Allow user to sign up or sign in.
2. Dashboard will be displayed. Amount spend and amount remaining will be showed on the main page, also couple of graphs which will make the experience visually easier. The graphs will be for the current month expenses (pie chart), tracking of the year expenses month by month(bar graph) and then an extra optional graph, a compound interest and monthly contribution growth based on SP500 investing for a 15-20 years period (linear graph). This last graph is supposed to motivate the user to keep saving and investing every month.
3. Budgets page. In this section user will be able to create new budgets through a form adding their category and amount to be spent.
4. Investing Search. In this section the user will have accces to a list of ETFs and Mutual Funds. The user will be able to filter based on certain criteria, and check specific information about ETFs and Mutual Funds.
 


