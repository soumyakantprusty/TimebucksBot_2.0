import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By





class Xpath_Util:
    def __init__(self, driver):
        self.elements = None
        self.guessable_elements = ['input', 'button', 'select','table','textarea','ul']
        self.known_attribute_list = ['id', 'name', 'placeholder', 'value', 'title', 'type', 'class']
        self.variable_names = []
        self.button_text_lists = []
        self.language_counter = 1
        self.elementsxpath = []

        self.driver = driver
    def __locatorvalidation(self,element,guessable_element):
        validlocatorfound = False
        validlocator=""
        useparentoflocator=False
        attributevalue=""
        for attr in self.known_attribute_list:
            if element.has_attr(attr):
                locator, attributevalue = self.guess_xpath(guessable_element, attr, element)
                print(locator, attributevalue)
                try:
                    element_to_test = self.driver.find_element(by=By.XPATH, value=locator)
                    #element_to_test.click()
                    validlocatorfound = True
                    validlocator = locator
                    print("Valid XPATH Found")
                    break
                except Exception as e:
                    print(repr(e))



        if not validlocatorfound:
            print("Checking for parent of the locator")
            for attr in self.known_attribute_list:
                if element.has_attr(attr):
                    locator, attributevalue = self.guess_xpath(guessable_element, attr, element)
                    try:
                       elementxpath = self.driver.find_element(by=By.XPATH, value=locator)
                       parentofelement = elementxpath.find_element(by=By.XPATH, value="..")
                       useparentoflocator=True
                       validlocator = locator
                       break
                    except Exception as e:
                        print(repr(e))
        print(validlocator,useparentoflocator,attributevalue,attr)
        return validlocator,useparentoflocator,attributevalue,attr


    def generate_xpath(self, soup):
        webpagedictlist = []
        multiplebtn = []
        submitbuttonxpath = {}
        print("generate the xpath and assign the variable names")
        result_flag = False

        for guessable_element in self.guessable_elements:
            self.elements = soup.find_all(guessable_element)
            #print("#########All Elements######")
            #print(guessable_element)
            #print(len(self.elements))

            elementxpath = " "
            element_type = ""
            parentelementinfo = " "
            for element in self.elements:
                #print("#########Element type and type present######")
                #print(element.tag_name)
                #print(element.has_attr("type"))
                if (not element.has_attr("type")  ) or (element.has_attr("type") and element['type'] != "hidden" and guessable_element !='button' and guessable_element !='table' ):
                    print("##########Check for valid xpath#################")
                    validlocator,useparentoflocator,attributevalue,attr=self.__locatorvalidation(element,guessable_element)
                    #print(validlocator)
                    elementlist=self.driver.find_elements(by=By.XPATH,value=validlocator)
                    #print(len(elementlist))
                    if len(elementlist) == 1:
                        webpagedict = {}
                        webpagedict["elementtype"] = self.driver.find_element(by=By.XPATH,value=validlocator).tag_name
                        if self.driver.find_element(by=By.XPATH,value=validlocator).tag_name=='select':
                            parent_element=self.driver.find_element(by=By.XPATH,value=validlocator)
                            childlements=parent_element.find_elements(by=By.TAG_NAME,value='option')
                            webpagedict["childelements"]=childlements
                        else:
                            webpagedict["childelements"]="NA"
                        webpagedict["attr"]=attr
                        try:
                            webpagedict["attr_type"] = element['type']
                        except:
                            webpagedict["attr_type"]="Not Found"
                        webpagedict["attributevalue"] = attributevalue
                        webpagedict["elementxpath"] = validlocator
                        elementxpath = self.driver.find_element(by=By.XPATH, value=validlocator)
                        parentofelement = elementxpath.find_element(by=By.XPATH, value="..")
                        grandparentofelement = parentofelement.find_element(by=By.XPATH, value="..")
                        try:
                            siblingofelement=self.driver.find_element(by=By.XPATH, value=validlocator+"//following-sibling::*")
                        except:
                            siblingofelement="NA"
                        webpagedict["siblingofelement"]=siblingofelement
                        try:
                            webpagedict["siblingofelementvalue"]=siblingofelement.text
                        except:
                            webpagedict["siblingofelementvalue"]="NA"
                        webpagedict["parentelementinfo"] = parentofelement
                        webpagedict["grandparentofelement"]=grandparentofelement
                        #print(webpagedict)
                        webpagedictlist.append(webpagedict)


                elif guessable_element in ('button'):
                    button_text = element.getText()

                    if element.getText().strip() == button_text.strip():
                        locator = self.guess_xpath_button(guessable_element, "text()", element.getText())
                        submitbuttonxpath["submitbtnxpath"] = locator
                        multiplebtn.append(locator)
                    else:
                        locator = self.guess_xpath_using_contains(guessable_element, "text()",
                                                                      button_text.strip())
                        submitbuttonxpath["submitbtnxpath"] = locator
                        multiplebtn.append(locator)

                    if len(self.driver.find_elements(by=By.XPATH, value=locator)) == 1:
                        result_flag = True
                            # Check for utf-8 characters in the button_text
                        matches = re.search(r"[^\x00-\x7F]", button_text)
                        if button_text.lower() not in self.button_text_lists:
                            self.button_text_lists.append(button_text.lower())
                            if not matches:
                                    # Striping and replacing characters before printing the variable name

                                    '''  print("%s_%s = %s" % (guessable_element,
                                                            button_text.strip().strip("!?.").encode('utf-8').decode(
                                                                'latin-1').lower().replace(" + ", "_").replace(" & ",
                                                                                                               "_").replace(
                                                                " ", "_"), locator.encode('utf-8').decode('latin-1')))
                                  '''
                            else:
                                    # printing the variable name with utf-8 characters along with language counter
                                webpagedict["submitbtbxpath"] = locator.encode('utf-8').decode('latin-1')
                                self.language_counter += 1
                        else:
                                # if the variable name is already taken
                            print(locator.encode('utf-8').decode(
                                    'latin-1') + "----> Couldn't generate appropriate variable name for this xpath")
                        break
                elif not guessable_element in self.guessable_elements:
                   print("We are not supporting this gussable element")
                elif element == 'table':
                        print("Table found in the page")
                        # print(webpagedictlist)
        return result_flag, webpagedictlist, submitbuttonxpath,multiplebtn




    def get_variable_names(self, element):
        "generate the variable names for the xpath"

        # condition to check the length of the 'id' attribute and ignore if there are numerics in the 'id' attribute. Also ingnoring id values having "input" and "button" strings.
        try:
            print(bool(re.search(r'([\d]{1,}([/-]|\s|[.])?)+(\D+)?([/-]|\s|[.])?[[\d]{1,}', element['value'])))
        except:
            self.variable_name = element['id']

        if (element.has_attr('id') and len(element['id']) > 2 and bool(re.search(r'\d', element['id']))) == False and (
                "input" not in element['id'].lower() and "button" not in element['id'].lower()):
            self.variable_name = element['id'].strip("_")
        # condition to check if the 'value' attribute exists and not having date and time values in it.
        elif element.has_attr('value') and element['value'] != '' and bool(
                re.search(r'([\d]{1,}([/-]|\s|[.])?)+(\D+)?([/-]|\s|[.])?[[\d]{1,}',
                          element['value'])) == False and bool(
                re.search(r'\d{1,2}[:]\d{1,2}\s+((am|AM|pm|PM)?)', element['value'])) == False:
            # condition to check if the 'type' attribute exists
            # getting the text() value if the 'type' attribute value is in 'radio','submit','checkbox','search'
            # if the text() is not '', getting the getText() value else getting the 'value' attribute
            # for the rest of the type attributes printing the 'type'+'value' attribute values. Doing a check to see if 'value' and 'type' attributes values are matching.
            if (element.has_attr('type')) and (element['type'] in ('radio', 'submit', 'checkbox', 'search')):
                if element.getText() != '':
                    self.variable_name = element['type'] + "_" + element.getText().strip().strip("_.")
                else:
                    self.variable_name = element['type'] + "_" + element['value'].strip("_.")
            else:
                if element['type'].lower() == element['value'].lower():
                    self.variable_name = element['value'].strip("_.")
                else:
                    self.variable_name = element['type'] + "_" + element['value'].strip("_.")
        # condition to check if the "name" attribute exists and if the length of "name" attribute is more than 2 printing variable name
        elif element.has_attr('name') and len(element['name']) > 1:
            self.variable_name = element['name'].strip("_")
        # condition to check if the "placeholder" attribute exists and is not having any numerics in it.
        elif element.has_attr('placeholder') and bool(re.search(r'\d', element['placeholder'])) == False:
            self.variable_name = element['placeholder']
        # condition to check if the "type" attribute exists and not in text','radio','button','checkbox','search'
        # and printing the variable name
        elif (element.has_attr('type')) and (element['type'] not in ('text', 'button', 'radio', 'checkbox', 'search')):
            self.variable_name = element['type']
        # condition to check if the "title" attribute exists
        elif element.has_attr('title'):
            self.variable_name = element['title']
        # condition to check if the "role" attribute exists
        elif element.has_attr('role') and element['role'] != "button":
            self.variable_name = element['role']
        else:
            self.variable_name = element['id']

        return self.variable_name.lower().replace("+/- ", "").replace("| ", "").replace(" / ", "_").replace("/",
                                                                                                            "_").replace(
            " - ", "_").replace(" ", "_").replace("&", "").replace("-", "_").replace("[", "_").replace("]", "").replace(
            ",", "").replace("__", "_").replace(".com", "").strip("_")

    def guess_xpath(self, tag, attr, element):
        "Guess the xpath based on the tag,attr,element[attr]"
        # Class attribute returned as a unicodeded list, so removing 'u from the list and joining back
        if type(element[attr]) is list:
            element[attr] = [i.encode('utf-8').decode('latin-1') for i in element[attr]]
            element[attr] = ' '.join(element[attr])
        self.xpath = "//%s[@%s='%s']" % (tag, attr, element[attr])

        return self.xpath,element[attr]

    def guess_xpath_button(self, tag, attr, element):
        "Guess the xpath for button tag"
        self.button_xpath = "//%s[%s='%s']" % (tag, attr, element)

        return self.button_xpath

    def guess_xpath_using_contains(self, tag, attr, element):
        "Guess the xpath using contains function"
        self.button_contains_xpath = "//%s[contains(%s,'%s')]" % (tag, attr, element)

        return self.button_contains_xpath

    def parseUrl(self, url):
        time.sleep(10)
        page = self.driver.execute_script("return document.body.innerHTML").encode('utf-8').decode(
            'latin-1')  # returns the inner HTML as a string
        soup = BeautifulSoup(page, 'html.parser')
        result_flag, webpagedictlist, submitbuttonxpath,multiplebtn=self.generate_xpath(soup)
        return result_flag, webpagedictlist, submitbuttonxpath,multiplebtn
        #if self.generate_xpath(soup) is False:
            #print("No XPaths generated for the URL:%s" % url)
        #print(self.elementsxpath)
