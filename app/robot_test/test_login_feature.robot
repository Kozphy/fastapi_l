### test_login_features.robot ###

*** Settings ***
Documentation   A test suite for login
Library         lib/LoginLibrary.py

*** Variable ***
${EMAIL}        test@gmail.com
${PASSWORD}     123456


*** Test Cases ***
User create account
    Create user  Valid User  ${EMAIL}  ${PASSWORD}
    Status should be    Success

User Login
    Input   email       ${EMAIL} 
    Input   password    ${PASSWORD}
    Status should be   Logged In
