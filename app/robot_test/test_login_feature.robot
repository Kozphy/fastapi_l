### test_login_features.robot ###

*** Settings ***
Documentation   A test suite for login
Library         lib/LoginLibrary

*** Variable ***
${EMAIL}        test@gmail.com
${PASSWORD}     123456


*** Test Cases ***
User create account
    Create  Valid User  ${EMAIL}  ${PASSWORD}
    Status should Be    Success

User Login
    Input   email       ${EMAIL} 
    Input   password    ${PASSWORD}
    Status should Be   Logged In
