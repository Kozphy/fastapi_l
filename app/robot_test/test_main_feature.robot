### test_main_features.robot ###

*** Settings ***
Documentation   A test suite for main
Library         SeleniumLibrary
Library         lib/MainLibrary.py

*** Variables ***
${MAIN_URL}         http://localhost:8080/
${BROWSER}          Firefox
${REMOTE_FIREFOX}   http://localhost:4444/status
# http://172.21.0.3:4444/

*** Test Cases ***
Go to main page
    # Create Webdriver   ${BROWSER}   firefox_binary=${LOCAL_FIREFOX}
    Open Browser       ${MAIN_URL}  ${BROWSER}  remote_url=${REMOTE_FIREFOX}
    Status should be   Success