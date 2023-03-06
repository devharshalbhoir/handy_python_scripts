# handy_python_scripts
This repo contains scripts to make my daily life easy and I tend to add scripts to automate any manual work that I've to face on a regular basis


- count_element_occurance_in_string.py

In this version of the script, we first get the user's choice as an integer, and then check if it's less than 1. If it is, we print an error message and exit. Otherwise, we create a dictionary called counts that maps each unique character in the string to its count using a dictionary comprehension.

We then use the sorted() function to sort the dictionary items by their values (i.e., the counts), in descending order. We use a lambda function as the key argument to specify that we want to sort by the values.

Next, we check if the user's choice is greater than the number of unique elements in the string. If it is, we print an error message. Otherwise, we use the sorted list to get the choice-th item (which is the choice-th most repeated element), and print its character and count.

Note that this script assumes that the user will enter a positive integer for the choice. If the user enters a non-integer or a negative number, the program will raise a ValueError exception. You could add error handling code to catch this case and print a more helpful error message.





