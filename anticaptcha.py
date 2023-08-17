import csv
import re
import traceback

from anticaptchaofficial.recaptchav2proxyless import *
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class AntiCaptcha:
    def __init__(self,bot_driver,taskid,basefilepath):
        super(AntiCaptcha, self).__init__()
        self.bot_driver=bot_driver
        self.captchasolved=False
        self.taskid=taskid
        self.basefilepath=basefilepath
        self.todaydate=date.today()
        print("Anti Captcha for Daily Task")
    def callanticaptcha(self):
        try:
            if self.taskid==2:
                self.bot_driver.execute_script(
                    'var element=document.getElementById("g-recaptcha-response"); element.style.display="block";')
                time.sleep(5)
                sitekey = self.bot_driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
        #sitekey_clean = sitekey.split('" data-callback')[0].split('data-sitekey="')[1]
                print(sitekey)
        #print(os.environ["anticaptcha_api_key"])
                solver = recaptchaV2Proxyless()
                solver.set_verbose(1)
                solver.set_key("621a03ed9c3b95634e84600766063251")
                balance = solver.get_balance()
                print("AntiCaptcha Balance:{balance}".format(balance=balance))
                if balance <= 0:
                    print("Current balance is {balance} too low balance!".format(balance=balance))
                    return
                solver.set_website_url(self.bot_driver.current_url)
                solver.set_website_key(sitekey)
                g_response = solver.solve_and_return_solution()
                if g_response != 0:
                    self.captchasolved = True
                    print("g_response:" + g_response)
                else:
                    self.captchasolved = False
                    print("task finished with error" + solver.error_code)
                '''print("Trying to paste the response")
                self.bot_driver.execute_script("""document.getElementById("g-captcha-response").innerHTML = arguments[0]""", g_response)
                time.sleep(10)
                self.bot_driver.execute_script('var element=document.getElementById("g-captcha-response"); element.style.display="none";')'''
                print("submitting the response ")
                time.sleep(10)
                script = f"""
                var response = '{g_response}';
                (function(response) {{
                    console.log(response);

                    $.ajax({{
                        type: 'POST',
                        url: 'https://timebucks.com/publishers/lib/scripts/php/action_clicks_verify.php',
                        data: {{
                            action: 'VerifyPushClicksCaptchaInstant',
                            response: response,
                            token: ''
                        }},
                        success: function(resp) {{
                            resp = JSON.parse(resp);
                            if (resp.result == 1) {{
                                window.location = resp.url;
                            }}
                        }}
                    }});
                }})(response);
                """
                self.bot_driver.execute_script(script)
                time.sleep(5)
                self.captchasolved = True
                with open(self.basefilepath + "\\anticaptcha.csv", 'a', encoding='utf-8', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([str(self.todaydate),"2","1"])
            elif self.taskid==3:
                time.sleep(5)
                sitekey = self.bot_driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
                # sitekey_clean = sitekey.split('" data-callback')[0].split('data-sitekey="')[1]
                print(sitekey)
                # print(os.environ["anticaptcha_api_key"])
                solver = recaptchaV2Proxyless()
                solver.set_verbose(1)
                solver.set_key("621a03ed9c3b95634e84600766063251")
                solver.set_website_url(self.bot_driver.current_url)
                solver.set_website_key(sitekey)
                g_response = solver.solve_and_return_solution()
                if g_response != 0:
                    self.captchasolved = True
                    print("g_response:" + g_response)
                else:
                    self.captchasolved = False
                    print("task finished with error" + solver.error_code)
                print("Trying to paste the response")
                time.sleep(10)
                script_element = self.bot_driver.find_element(By.XPATH, '/html/body/script')
                script_content = self.bot_driver.execute_script("return arguments[0].innerHTML;", script_element)
                print(script_content)
                token_match = re.search(r"token:\s*'([^']*)'", script_content)
                token_value = ""
                if token_match:
                    token_value = token_match.group(1)
                    print(f"Token value: {token_value}")
                modified_script = f"""
                                    var response = '{g_response}';
                                    (function(response) {{
                                        console.log(response);
                                        $.ajax({{
                                            type: 'POST',
                                            url: '../publishers/lib/scripts/php/clicks/Users.php',
                                            data: {{
                                                action: 'VerifyClicksCaptcha',
                                                response: response,
                                                IsSlideshow: 1,
                                                token: '{token_value}'
                                            }},
                                            success: function(resp) {{
                                                 window.location = window.location;

                                            }}
                                        }});
                                    }})(response);
                                """
                self.bot_driver.execute_script(modified_script)
                time.sleep(5)
                self.captchasolved = True
                with open(self.basefilepath + "\\anticaptcha.csv", 'a', encoding='utf-8', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([str(self.todaydate), "3", "1"])
            elif self.taskid in [1,6]:
                self.bot_driver.execute_script(
                    'var element=document.getElementById("g-recaptcha-response"); element.style.display="block";')
                time.sleep(5)
                sitekey = self.bot_driver.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
                # sitekey_clean = sitekey.split('" data-callback')[0].split('data-sitekey="')[1]
                print(sitekey)
                # print(os.environ["anticaptcha_api_key"])
                solver = recaptchaV2Proxyless()
                solver.set_verbose(1)
                solver.set_key("621a03ed9c3b95634e84600766063251")
                solver.set_website_url(self.bot_driver.current_url)
                solver.set_website_key(sitekey)
                g_response = solver.solve_and_return_solution()
                if g_response != 0:
                    self.captchasolved = True
                    print("g_response:" + g_response)
                else:
                    self.captchasolved = False
                    print("task finished with error" + solver.error_code)
                print("Trying to paste the response")
                self.bot_driver.execute_script(
                    """document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", g_response)
                time.sleep(10)
                self.bot_driver.execute_script(
                    'var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
                print("submitting the response ")
                time.sleep(10)
                self.bot_driver.execute_script("SubmitBuyTaskCaptcha();")
                time.sleep(5)
                self.captchasolved = True
                with open(self.basefilepath + "\\anticaptcha.csv", 'a', encoding='utf-8', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([str(self.todaydate),str(self.taskid),"1"])

        except Exception as e:
            print(repr(e))
        return self.captchasolved


