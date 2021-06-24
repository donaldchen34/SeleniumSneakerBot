class Error(Exception):
    pass

#Make all the Errors under TaskErrors
class CaptchaError(Error):
    """
    Raised when a captcha appears
    Used for manual captcha handler to pass captcha links
    """
    def __init__(self,message,link,driver):
        self.message = message
        self.link = link
        self.driver = driver

class LoadCaptchaError(Error):
    """
    Raised when there is an issue during the Captcha phase
    """

    def __init__(self,message):
        self.message = message

class CheckOutError(Error):
    """
    Raised when there is an issue during the Checkout Phase
    """

    def __init__(self,message):
        self.message = message

class ImageError(Error):
    """
    Raised when there is an issue during the image loading and saving
    """

    def __init__(self,message):
        self.message = message

class XPathError(Error):
    """
    Raised when there is an update to an Xpath
    """

    def __init__(self,message):
        self.message= message