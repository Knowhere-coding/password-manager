# Password Manager 

![wasp](https://user-images.githubusercontent.com/92861465/157727427-47ff6b26-c532-4d40-a496-e002abfeb4aa.png)
<!-- WASP -->

This is a simple *terminal based* **password manager**.

![UI_screenshot](https://user-images.githubusercontent.com/92861465/157726142-f6b4735e-cf28-4f48-bcbf-4baec714bd46.PNG)
<!-- UI Screenshot -->

## Features:
### Store any account in an AES encrypted database

First of all, you have to provide a ***category***, ***siteName***, ***url***, ***username*** and ***email*** for your account to store it in the database.
In addition, for the *password* you can either provide ***your own password***, or let an algorithmen create a ***strong password*** for you.
After the password creation you can specify the ***expiration period*** of your password and every time you want to access that
password when it's expired you will get asked to change it.

### Access your account data

You can search for your accounts by providing any field value and the manager will display all matched accounts. You then can
select an account and the password is copied immediately to the ***clipboard*** for further use. Moreover, you can decide to open the 
provided ***url*** in the browser.

### Changing/Deleting account data

Of course you are able to ***change***/***delete*** any provided information later on.

### Create backup

To create a *backup* you can specify a ***backup location*** or go with the default location (***\backup***). Furthermore, the backup can be used
to ***restore*** lost data or for data ***transfers***.

### Create print layout

You can create a *print layout* with all your account data which you can print out to store physically.
![print_layout](https://user-images.githubusercontent.com/92861465/157727111-61c18561-3817-49ef-a5d9-777a0ae2a10e.PNG)
<!-- print_layout -->

## Technical Parts

**AES Encryption**
  - encrypted files
  - access only with AES Key
  - AES Key generated from master password

**CSV database**
  - all data stored in a .cvs file
  - simple access
  - easy to encrypt

## The whole Password Manager can be stored locally on a USB Thumb Drive

## Requirements
**Python 3.10**

See [requirements.txt](https://github.com/Knowhere-coding/password_manager/blob/main/requirements.txt)
<!-- requirements.txt file -->

External libraries:
  - art~=5.3
  - colorama~=0.4.4
  - termcolor~=1.1.0
  - sympy~=1.8
  - pwinput~=1.0.2
  - prettytable~=2.2.1
  - pycryptodome~=3.11.0
  - pyperclip~=1.8.2
  - pip~=22.0.3
  - wheel~=0.37.1
  - cryptography~=35.0.0
  - lxml~=4.7.1
  - setuptools~=58.1.0
  - future~=0.18.2
  - xlwings~=0.26.3


        ©Copyright 2021 by Knowhere-coding

