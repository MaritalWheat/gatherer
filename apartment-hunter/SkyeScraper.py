from selenium import webdriver
from twilio.rest import TwilioRestClient
import time

path_to_chromedriver = '/Users/emanuelrosu/Downloads/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

url = 'http://skyeatbelltownapts.prospectportal.com/?module=property_info&amp;property[id]=95872&amp;is_responsive_snippet=1&amp;snippet_type=website&amp;is_collapsed=1&amp;host_domain=www.millcreekplaces.com'
browser.get(url)

browser.find_element_by_xpath('//*[@id="fp-tab-1"]').click()
time.sleep(5)
browser.find_element_by_xpath('//*[@id="floorplans-1"]/li/div/div[6]/a[1]').click()
time.sleep(5)
browser.save_screenshot('seleniumscreenshot.png')
prices = browser.find_elements_by_xpath('//span[@class="unit-col-text"]')

index = 0
apartment = ""
for price in prices:
    if (index == 0 or index == 1 or index == 5):
        apartment += price.text + " "
    index += 1
    if (index == 6):
        apartment += "\n"
        index = 0
print apartment

account_sid = twilioAccountSid #redacted for GitHub
auth_token  = twilioAuthToken #redacted for GitHub
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(body=apartment,
    to=recepientPhoneNum,    # Replace with your phone number
    from_=senderPhoneNum") # Replace with your Twilio number
print message.sid
