### test_main_features.robot ###

*** Settings ***
Documentation   A test suite for main
Library         SeleniumLibrary
Library         RequestsLibrary
Library         lib/MainLibrary.py

*** Variables ***
${MAIN_URL}         http://localhost:8080/
${BROWSER}          Firefox
${REMOTE_FIREFOX}   http://host.docker.internal:4444


*** Test Cases ***
Test main page api
    # Open Browser       ${BROWSER}  remote_url=${REMOTE_FIREFOX}
    request_main        /
    # ${response}=        GET     ${MAIN_URL}
    MainLibrary.Status Should Be    200
# Go to main page
    # Open Browser       ${BROWSER}  remote_url=${REMOTE_FIREFOX}
    # Go to              ${MAIN_URL}
    # Status should be   Success
    # CLose Browser