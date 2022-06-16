### test_main_features.robot ###

*** Settings ***
Documentation   A test suite for main
Library         SeleniumLibrary
Library         lib/MainLibrary.py

*** Variables ***
${MAIN_URL}     http://localhost:8080/
${BROWSER}      Firefox

*** Test Cases ***
Go to main page
    Create Webdriver   ${BROWSER}   
    Open Browser       ${MAIN_URL}
    Status should be   Success