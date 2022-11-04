# Weather checker

### Video Demo:  [https://youtu.be/DKPiaEyKfbs](https://youtu.be/DKPiaEyKfbs)

## Description:

The project is a simple `flask web application` which allows a user to check the current weather in the chosen  city.

The app sends an http-request to the site “[api.openweathermap.org]()” to get the information of the temperature.

![](image/README/1651653010717.png)

## Structure of the project

(made for educational purposes)


The main web-page has:

- a form to ask a user for the name of the city 
- the table from sqlite database with last requests from the user
- the background image (changing depending on the weather)

#### Files:

**1. views.py.**

The view of the main page checks if there were used methods `Get` or `Post`.

The Method “post” calls the function 'check_posted_request' to get new information about the weather. The method "get" checks if there was a new successful request from a user, selects rows of last requests from the database, renders the index.html template with new data as parameters "args".

**2. request_check.py**

It has functions which help to get input from a user from the form, check the correctness of the symbols of that request and send a request to a site which provides information about the weather. User's input is checked of being constructed only from english letters, replaces spaces and dashes to a plus sign as some cities as (Nizhny+Novgorod) contain several words in the title.

Last input of a user is inserted into a database if it’s a correct request.

**3. db_editor.py**

class DatabaseEditor provides a connection to the sqlite database, methods to create a main table with weather, insert values, delete rows of old requests, select requests to show them in a table on the web page. Old rows are deleted when the number of inserted rows becomes equal to 10.

It is written in a separated file as all methods are dedicated to work with a database, it's possible to use the same structure for other projects with similar purposes to work with databases.

**4. last_weather.db**

Database which contains last requests from a user and weather in that city.

**5. templates:**

-index.html

Contains form to get input from a user, table with last checks of the weather.

`Jinja2` statements checks the condition if the last request was successful, and changes the template to several cases: “cold” weather’s picture, “warm” weather’s picture, gray background in case the request hasn't been found.

**6. static:**

-pictures

-styles.css
