from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from files.states import states
from CaptchaSolver import CaptchaSolver, saveData, sizeOfImagesFolder
import urllib.request
from PIL import Image
import time
import json
from files.CaptchaWords import captchawords
import ReadData
from Errors import CaptchaError, LoadCaptchaError, CheckOutError, ImageError, XPathError
from FilePaths import SITES_FILE, FIREFOX_WEB_DRIVER_PATH

#Todo
#Finish CaptchaHandler()
#More Error Catching or None to be more efficient????
#Train NN
#Make it compatible with other footsites
#Go to Footsite.buy() and Footsite.captchahandler()
#BUG FIXING
#Sold out Error
#Read through comments to fix issues
#Comments and Clean Up

class FootSite:
    def __init__(self,driver = None):
        """
        :param driver: selenium webdriver, default is None
        """

        ffprofile = FirefoxProfile()
        ffprofile.set_preference("dom.webdriver.enabled",False)
        #https://stackoverflow.com/questions/43908995/how-to-disabling-notification-using-selenium-for-firefox-browser
        # Set up driver
        self.driver = driver if driver else webdriver.Firefox(executable_path= FIREFOX_WEB_DRIVER_PATH,firefox_profile=ffprofile)
        self.driver.maximize_window()

        self.captcha_solver = CaptchaSolver()

    def getLink(self,site):
        """
        :param site: name of site(string)
        :return: link to website, the link contains <product_num> token that needs to be replaced with createURL()
        """

        with open(SITES_FILE,'r') as data:
            sites = json.load(data)
            if site in sites:
                return sites[site]
            else:
                return None

    def createURL(self,site,product_num):
        """
        :param site: name of site(string)
        :param product_num: product number(string)
        :return: link to product
        """

        site = self.getLink(site)
        return site.replace("<product_num>",str(product_num))

    #Returns account_info of account.json[account_name]
    def getAccountInfo(self,account_name):
        accounts = ReadData.getAccountsData()

        return accounts[account_name]

    def getAvailableSizes(self):
        """
        Searches div list and checks which child is not enabled
        :return: Returns available sizes in dict and position ex: [XS:div[1],S:div[2],M:div[3],...]
        """

        size_xpath = '// *[ @ id = "ProductDetails"] / div[5] / fieldset / div'

        try:
            size_available = self.driver.find_element_by_xpath(size_xpath)
        except:
            raise XPathError("Sizes XPath needs to be updated")
        avail = {}
        temp = []
        for i,size in enumerate(size_available.text.split('\n')):
            size = size.replace('.','')
            avail[size] = 'div[{}]'.format(i + 1) # i + 1 because div starts at 1
            temp.append(size)

        for size in temp:
            inner_child_xpath = '// *[ @ id = "ProductDetails_radio_size_{}"]'.format(size.lower())
            inner_child = self.driver.find_element_by_xpath(inner_child_xpath)
            in_stock = inner_child.is_enabled()
            if not in_stock:
                avail.pop(size)

        return avail

    #May have to change the check
    def checkCaptcha(self):
        """
        :return: returns if html/body is clickable
        """

        try:
            self.driver.find_element_by_xpath('//*[@id="dataDomeCaptcha"]')
            return True
        except:
            return False

    def closePopups(self):
        """
        Popup that are closed:
        - cookies tracker popup on top of screen
        - policy updates popup on bottom right
        - intro mailing lists in the middle
        :return: None

        Can change try/except blocks to if find driver or driver.exists() -> then close -> might be less costly
        """

        try:
            policy_updates = self.driver.find_element_by_xpath('//*[@id="touAgreeBtn"]')
            policy_updates.click()
        except:
            pass

        try:
            cookies_popup = self.driver.find_element_by_xpath('//*[@id="ccpaClose"]')
            cookies_popup.click()
        except:
            pass

        try:
            """
            if site == "footlocker": #Need to be more adaptive -> PLS UNHARDCODE T.T
                WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located
                                                     ((By.XPATH, '//*[@id="bluecoreEmailCaptureForm"]')))
            """

            mailing_list = self.driver.find_element_by_xpath(
                '//*[@id="bluecoreEmailCaptureForm"]/div/div[2]/div[11]/button/img')
            mailing_list.click()
        except:
            pass



    ### OUTDATED ###
    # TODO
    # Test with other sites
    # Train NN for better accuracy
    # Add boxes in between the points for 4x4
    # Check if click next button works
    # -> It will not work if not enough images were selected that match the target
    # -> ie. There are more pictures that match the target or if No pictures were selected
    def captchaHandler(self):
        """
        Hardcoded Captcha Handler for footsites
        Saves and Solves Captcha by sending images to CaptchaSolver to classify
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable
                                             ((By.XPATH, '//*[@id="dataDomeCaptcha"]')))

        ### One click
        # Add switch to one click iframe for more consistency -> Not sure if it will work
        try:
            self.driver.switch_to.frame("dataDomeCaptcha")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable
                                                 ((By.XPATH, '//*[@id="captcha-submit"]')))
        except:
            raise LoadCaptchaError("Failed to switch to Captcha IFrame")

        one_click_button = self.driver.find_element_by_xpath('//*[@id="captcha-submit"]')
        one_click_button.click()

        #### Selection Captcha
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located
                                                 ((By.XPATH, '/html/body/div[2]/div[4]/iframe')))
            captcha_challenge_iframe = self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/iframe')
            self.driver.switch_to.frame(captcha_challenge_iframe)
        except:
            raise LoadCaptchaError("Failed to switch to captcha challenge iframe")

        # Repeat until captcha is closed
        # One loop with loop until there are no more pictures that match the target_field
        # The loop is needed to grab the changing target_field
        while True:
            if not self.checkCaptcha():
                break

            # Get target field
            # Sometimes does not work
            try:
                WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located
                                                     ((By.XPATH,
                                                       '//*[@id="rc-imageselect"]/div[2]/div[1]/div[1]/div/strong')))
            except:
                print("Could not get target word error")
                raise LoadCaptchaError("Failed to get target word")
                break


            target_object = self.driver.find_element_by_xpath(
                '//*[@id="rc-imageselect"]/div[2]/div[1]/div[1]/div/strong')
            print(target_object.text)
            target = target_object.text
            if target in captchawords:
                target = captchawords[target]

            if target == 'crosswalks': #ImageAI does not know what a cross walk is
                print("CROSSWALKS >:(")
                break

            # Open initial image
            img_num = sizeOfImagesFolder()
            self.saveImages(target)
            img = Image.open('Images/{num}_{target}.png'.format(num=img_num,target=target))

            row_amt = len(self.driver.find_elements_by_xpath('.//*[@id="rc-imageselect-target"]/table/tbody/*'))

            new_size = (390, 390) if row_amt == 3 else (
            380, 380)  # Change to be more adaptive -> Get info from containers
            img = img.resize(new_size)
            ### Shape is wrong?
            print(img)

            captchas_to_click = self.captcha_solver.classify(img,target,new_size[0],row_amt)

            init_image_src = self.driver.find_element_by_xpath(
                '//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[1]/div/div[1]/img').get_attribute("src")
            possible_squares = []

            # Add boxes inbetween the points for 4x4

            for captcha_coords in captchas_to_click:
                row,col = captcha_coords
                captcha_picture = self.driver.find_element_by_xpath(
                    '//*[@id="rc-imageselect-target"]/table/tbody/tr[{row}]/td[{col}]/div'.format(row=row, col=col))
                captcha_picture.click()
                print("Clicked")
                if row_amt == 3:
                    possible_squares.append((row, col,init_image_src))


            # Waiting to click on captchas 3x3 Captcha
            while len(possible_squares) != 0:
                print("New Captcha")

                row, col, old_captcha_src = possible_squares.pop(0)
                print(row,col,old_captcha_src)

                new_captcha = self.driver.find_element_by_xpath(
                     '//*[@id="rc-imageselect-target"]/table/tbody/tr[{row}]/td[{col}]/div/div[1]/img'.format(
                         row=row, col=col))
                new_captcha_src = new_captcha.get_attribute('src')


                while (new_captcha_src == old_captcha_src): #Wait for new img to load
                    print('waiting')
                    WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located
                                                         ((By.XPATH, '//*[@id="rc-imageselect-target"]/table/tbody/tr[{row}]/td[{col}]/div/div[1]/img'.format(row=row, col=col))))

                    new_captcha = self.driver.find_element_by_xpath(
                        '//*[@id="rc-imageselect-target"]/table/tbody/tr[{row}]/td[{col}]/div/div[1]/img'.format(
                            row=row, col=col))
                    new_captcha_src = new_captcha.get_attribute('src')
                    if new_captcha_src == old_captcha_src:
                        time.sleep(1)

                response = urllib.request.urlopen(new_captcha_src)
                image = response.read()
                saveData(image, "image")
                image = Image.open('Images/{num}_image.png'.format(num = sizeOfImagesFolder()-1))

                pred = self.captcha_solver.classify(image,target,new_size[0]//row_amt,1)

                if len(pred):
                    captcha_picture = self.driver.find_element_by_xpath(
                        '// *[ @ id = "rc-imageselect-target"] / table / tbody / tr[{row}] / td[{col}]'.format(
                            row=row, col=col))
                    captcha_picture.click()
                    if row_amt == 3:
                        possible_squares.append((row, col,new_captcha_src))


            next_captcha = self.driver.find_element_by_xpath('//*[@id="recaptcha-verify-button"]')
            next_captcha.click()

            time.sleep(1)


        # Go back to main page/content
        self.driver.switch_to.default_content()

        # Manually Solve Captcha b/c AutoCaptcha broken :(
        print("MANUEL")
        self.manualCaptchaHandler()

    #Calls and fills out part 1-4 of checkout
    #Add try/catch for each to output errors for log
    def checkout(self,account_name):
        account_info = self.getAccountInfo(account_name)

        self.contactinfo(account_info)  # Part 1
        self.packageoptions(account_info)  # Part2
        self.payment(account_info)  # Part3
        self.review()  # Part4

    #Part 1 of checkout
    def contactinfo(self,autofill_data):
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="ContactInfo_text_firstName"]')))
        first_name = self.driver.find_element_by_xpath('//*[@id="ContactInfo_text_firstName"]')
        first_name.send_keys(autofill_data['first_name'])

        last_name = self.driver.find_element_by_xpath('//*[@id="ContactInfo_text_lastName"]')
        last_name.send_keys(autofill_data['last_name'])

        email_address = self.driver.find_element_by_xpath('//*[@id="ContactInfo_email_email"]')
        email_address.send_keys(autofill_data['email'])

        phone_number = self.driver.find_element_by_xpath('//*[@id="ContactInfo_tel_phone"]')
        phone_number.send_keys(autofill_data['phone'])

        save_and_continue1 = self.driver.find_element_by_xpath('//*[@id="ContactInfo"]/div[6]/button')
        save_and_continue1.submit()

    #Part 2 of checkout
    def packageoptions(self,autofill_data):
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="ShippingAddress_text_line1"]')))
        street_address = self.driver.find_element_by_xpath('//*[@id="ShippingAddress_text_line1"]')
        street_address.send_keys(autofill_data['address']['street'])

        apt_num = self.driver.find_element_by_xpath('//*[@id="ShippingAddress_text_line2"]')
        apt_num.send_keys(autofill_data['address']['apt'])

        zipcode = self.driver.find_element_by_xpath('//*[@id="ShippingAddress_text_postalCode"]')
        zipcode.send_keys(autofill_data['address']['zip_code'])

        city = self.driver.find_element_by_xpath('//*[@id="ShippingAddress_text_town"]')
        city.send_keys(autofill_data['address']['city'])

        try:  # Abbreviation - NY
            state = Select(self.driver.find_element_by_xpath('//*[@id="ShippingAddress_select_region"]'))
            state.select_by_visible_text(autofill_data['address']['state'])
        except:  # Not Abbreviated - New York
            state = Select(self.driver.find_element_by_xpath('//*[@id="ShippingAddress_select_region"]'))
            state.select_by_visible_text(states[autofill_data['address']['state']])

        # Delivery Option:
        # Footlocker gives option
        ### Need to work on this
        try:
            shipping_status = Select(self.driver.find_element_by_xpath(''))
        except:
            pass

        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="step2"]/div[2]/div[2]/button')))
        except:
            raise CheckOutError("Save and Continue button for part 2 did not load")

        save_and_continue2 = self.driver.find_element_by_xpath('//*[@id="step2"]/div[2]/div[2]/button')
        ActionChains(self.driver).move_to_element(save_and_continue2).click().perform()

        # Refers to Verify address
        if self.checkCaptcha():  # Can change to: if(react modal is there) / try catch
            print("Verify Address")

            try:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable
                                                     ((By.XPATH, '//*[@id="AddressLookup"]/div[4]/button'))).click()
            except:
                raise CheckOutError("Verify Address popup bugged out")

    #Part 3 of checkout
    def payment(self,autofill_data):

        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located
                                                 ((By.XPATH, '//*[@id="adyenContainer"]/div/div[1]/div[1]/span/iframe')))
        except:
            raise CheckOutError("Payment Option did not load(Part 3 of checkout)")

        secure_card_iframe = self.driver.find_element_by_xpath(
            '//*[@id="adyenContainer"]/div/div[1]/div[1]/span/iframe')
        self.driver.switch_to.frame(secure_card_iframe)

        credit_card_number = self.driver.find_element_by_xpath('//*[@id="encryptedCardNumber"]')
        credit_card_number.send_keys(autofill_data['payment']['card_number'])
        self.driver.switch_to.default_content()

        secure_month_iframe = self.driver.find_element_by_xpath(
            '//*[@id="adyenContainer"]/div/div[1]/div[2]/div[1]/span/iframe')
        self.driver.switch_to.frame(secure_month_iframe)

        credit_card_month = self.driver.find_element_by_xpath('//*[@id="encryptedExpiryMonth"]')
        credit_card_month.send_keys(autofill_data['payment']['mm'])
        self.driver.switch_to.default_content()

        secure_year_iframe = self.driver.find_element_by_xpath(
            '//*[@id="adyenContainer"]/div/div[1]/div[2]/div[2]/span/iframe')
        self.driver.switch_to.frame(secure_year_iframe)

        credit_card_year = self.driver.find_element_by_xpath('//*[@id="encryptedExpiryYear"]')
        credit_card_year.send_keys(autofill_data['payment']['yy'])
        self.driver.switch_to.default_content()

        secure_csc_iframe = self.driver.find_element_by_xpath(
            '//*[@id="adyenContainer"]/div/div[1]/div[2]/div[3]/span/iframe')
        self.driver.switch_to.frame(secure_csc_iframe)

        credit_card_csc = self.driver.find_element_by_xpath('//*[@id="encryptedSecurityCode"]')
        credit_card_csc.send_keys(autofill_data['payment']['csc'])
        self.driver.switch_to.default_content()

    #Part 4 of checkout
    #Does not click submit button yet
    def review(self):

        place_order = self.driver.find_element_by_xpath(
            '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div[2]/button')
        # place_order.submit()
        print(place_order.text)

    ### OUTDATED ###
    # Save images
    def saveImages(self,target):

        try:
            WebDriverWait(self.driver, 10).until \
                    (expected_conditions.visibility_of_element_located(
                    (By.XPATH, '//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[1]/div/div[1]/img')))
        except:
            raise ImageError("Unable to grab image to save")

        init_image_src = self.driver.find_element_by_xpath(
            '//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[1]/div/div[1]/img').get_attribute("src")
        response = urllib.request.urlopen(init_image_src)
        image = response.read()

        #Change image size here

        saveData(image,target)

        img_num = sizeOfImagesFolder() - 1
        img = Image.open('Images/{num}_{target}.png'.format(target=target,num=img_num))

        # Split initial image into correct squares and clicks on correct squares
        row_amt = len(self.driver.find_elements_by_xpath('.//*[@id="rc-imageselect-target"]/table/tbody/*'))

        new_size = (390, 390) if row_amt == 3 else (
            380, 380)  # Change to be more adaptive -> Get info from containers
        img = img.resize(new_size)

        for row in range(row_amt):
            for col in range(row_amt):
                img_size = new_size[0] / row_amt  # Height/ Width of squares
                left = col * img_size
                top = row * img_size
                right = (col + 1) * img_size
                bottom = (row + 1) * img_size
                new_img = img.crop((left, top, right, bottom))

                # Save squares into /Pictures to be manually classified
                new_img.save("Images/{}_image.png".format(sizeOfImagesFolder()))

    #Used for manual puzzle slider captca
    def manualPuzzleSolver(self):

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable
                                                 ((By.XPATH, '//*[@id="dataDomeCaptcha"]')))

            link = self.driver.find_element_by_xpath('//*[@id="dataDomeCaptcha"]')
            link = link.get_attribute('src')

        except:
            self.driver.quit()
            raise LoadCaptchaError("Failed to load Manual Puzzle Solver Captcha")
        else:
            print("footsite")
            #self.driver.close()

            raise CaptchaError(message="Manual Puzzle Solver",link=link,driver = self.driver)


    ### OUTDATED ###
    # Save images from Captcha and then manually click Captcha
    # Used for manual choose pictures captcha
    def manualCaptchaHandler(self):
        #There are no raise errors because manualCaptchaHandler() can be called
        # from different steps of bot
        try: #Click buttons to get into Captcha
            # -> Can be passed this step depending on where this function is called.
            # Move driver to Captcha to get images to save
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable
                                                 ((By.XPATH, '//*[@id="dataDomeCaptcha"]')))

            ### One click
            # Add switch to one click iframe for more consistency -> Not sure if it will work
            self.driver.switch_to.frame("dataDomeCaptcha")
            """
            #V1 - Click on Captcha Box
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable
                                                 ((By.XPATH, '//*[@id="captcha-submit"]')))
                                                 
            one_click_button = self.driver.find_element_by_xpath('//*[@id="captcha-submit"]')
            one_click_button.click()
            """

            #V2 New Capctha

            #Grab Link to button -> Dont need to click

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable
                                                 ((By.XPATH, '//*[@id="1e505deed3832c02c96ca5abe70df9ab"]/div/div[2]/div[1]/div[3]'
                                                             '')))

            one_click_button = self.driver.find_element_by_xpath('//*[@id="1e505deed3832c02c96ca5abe70df9ab"]/div/div[2]/div[1]/div[3]')
            one_click_button.click()


            # Add a check incase selection is skipped
            #### Selection Captcha
        except:
            print("No One Click")
            pass


        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located
                                                 ((By.XPATH, '/html/body/div[2]/div[4]/iframe')))
            captcha_challenge_iframe = self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/iframe')
            self.driver.switch_to.frame(captcha_challenge_iframe)

            # Sometimes does not work

            WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located
                                                 ((By.XPATH,
                                                   '//*[@id="rc-imageselect"]/div[2]/div[1]/div[1]/div/strong')))


            target_object = self.driver.find_element_by_xpath(
                '//*[@id="rc-imageselect"]/div[2]/div[1]/div[1]/div/strong')
            print(target_object.text)
            target = target_object.text

            # Save images
            self.saveImages(target)
        except:
            print("Could not get target word error")



        # Manually Solve Captcha
        while True:
            time.sleep(1)
            print('ahh')
            if not self.checkCaptcha():
                break

            try:

                target_object = self.driver.find_element_by_xpath(
                    '//*[@id="rc-imageselect"]/div[2]/div[1]/div[1]/div/strong')

                if target != target_object.text:
                    target = target_object.text
                    self.saveImages(target)
            except:
                pass

    def buy(self,site, product_num, size,account_name,proxy):
        """
        :param site: name of site(string)
        :param product_num: product number(string)
        :param size: size of product(string) input: XS,S,M,...,09.5,10.0,...,
        :param account: account name for autofill info
        :param proxy: The ip name being used for the task(Not used currently)
        :return: no return

        TODO and Notes
        -> Implement proxies
        -> Log into gmail first for easier captcha
            -> Devleop a gmail trainer/ automated gmail account maker
        -> Has explicit time.sleep(1) currently (need to change to more adaptive stall)
        -> Add color/model support
        -> Test other sites:
            -> Footaction works
            -> Need to test: Eastbay, Footlocker, Champs
            -> If site == eastbay close initial popup
        -> Automated Captcha:
            #Currently only saves images and person has to manually solve captcha - manualCaptchaHandler()
            #Need to finish and uncomment self.captchaHandler()
            -> NN for image classification
                -> Train NN on top of pretrained model
        -> Clean up Code
        """


        ### Add log in to Gmail first for easier captcha
        ### -> Likewise create gmail trainer for gmails

        # Go to footsite


        url = self.createURL(site, product_num)
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 10).until(
                expected_conditions.visibility_of_element_located(
                    (By.XPATH, '// *[ @ id = "ProductDetails"] / div[5] / fieldset / div')))  # Wait for sizes options to load
        except:
            #The same XPath is also used in self.getAvailableSizes() and in the error 403 check in this function
            raise XPathError("Sizes XPath needs to be updated")

        time.sleep(1)
        self.closePopups()

        avail = self.getAvailableSizes()

        size = size.replace('.', '')
        if size not in avail:
            print("Size is unavailable") #Use Try Catch/ change to failed cop in GUI
        else:

            self.closePopups()

            ### Find size and Add to cart

            size_xpath = '//*[@id="ProductDetails"]/div[5]/fieldset/div/{}/label'.format(avail[size])
            size_button = self.driver.find_element_by_xpath(size_xpath)

            size_button.click()
            time.sleep(0.5)

            add_to_cart_button = self.driver.find_element_by_xpath('//button[contains(text(),"Add To Cart")]')
            add_to_cart_button.submit()

            time.sleep(1)

            #Captcha Handler
            if self.checkCaptcha():
                print("Captcha :(")

                # Needs work - Doesnt work with eastbay, Sorta catches it with footlocker and footaction
                # Test with other sites
                #self.captchaHandler() #Auto Captchahandler for picture choosing
                #self.manualCaptchaHandler() #Manual Captchahandler for picture choosing
                self.manualPuzzleSolver() #Manual CaptchaHandler for puzzle slider

            print('Finished Captcha')

            #Gets a Error 403/503 after finishing captcha
            error_check = self.driver.find_element_by_xpath('/html/body/h1')
            if error_check.text[:5] == 'Error':
                print("Error 403")

                # Go back and rebuy item
                ### Clean up -> this is same as code above
                self.driver.get(url)

                WebDriverWait(self.driver, 10).until(
                    expected_conditions.visibility_of_element_located(
                        (By.XPATH, '//*[@id="ProductDetails"]')))  # Wait for sizes options to load

                self.closePopups()

                ### Find size and Add to cart

                size_xpath = '//*[@id="ProductDetails"]/div[5]/fieldset/div/{}/label'.format(avail[size])
                size_button = self.driver.find_element_by_xpath(size_xpath)

                size_button.click()
                time.sleep(0.5)

                add_to_cart_button = self.driver.find_element_by_xpath('//button[contains(text(),"Add To Cart")]')
                add_to_cart_button.submit()

                time.sleep(1)



            ### Checkout -> Move to function, Checkout()

            #Maybe check if cart has item for condition
            # or add a successful add to the add_to_carts instead of time.sleep()
            
            time.sleep(1)
            cart_link = "https://www.{}.com/cart".format(site)
            self.driver.get(cart_link)
            WebDriverWait(self.driver, 10).until(
                expected_conditions.visibility_of_element_located(
                    (By.XPATH, '//*[@id="main"]/div/div[3]/div/div')))  # Wait for sizes options to load

            guest_checkout_button = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/div/div/div/div[2]/div[2]/a')
            guest_checkout_button.click()


            # Fill out data
            self.checkout(account_name)

            print('noice')

if __name__ == "__main__":
    test = FootSite()

    #Footsites
    site = "footaction"
    #site = "footlocker"
    #site = "eastbay"
    #site = "champs"

    product = "C0224" #Cargo Pants
    #product = "R4997410" #Nike Embroidered Shirt
    #product = "D5007003" #Nike LeBron 17 Low

    size = "M"
    #size = "08.5"

    test.buy(site,product,size)
