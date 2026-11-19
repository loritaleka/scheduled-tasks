import os
import datetime as dt
import pandas
import random
import smtplib


MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

# 1. Get today's month and day as a tuple, e.g. (11, 19)
today = dt.datetime.now()
today_tuple = (today.month, today.day)

# 2. Read birthdays.csv into a pandas DataFrame
data = pandas.read_csv("birthdays.csv")

# 3. Build a dictionary: {(month, day): whole row}
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

# 4. If today matches a birthday, write and send the email
if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    # Pick a random letter template (letter_1.txt, letter_2.txt or letter_3.txt)
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
    # Open the letter and replace [NAME] with the person's real name
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])
    
    # Connect to the email server, secure the connection, log in and send
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=birthday_person["email"], msg=f"Subject: Happy Birthday!\n\n{contents}.")
