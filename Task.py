from FootSite import FootSite

class Task:
    def __init__(self,site,product_num,size,account,proxy):

        #Add which profile and billings to use

        self.site = site
        self.product_num = product_num
        self.size = size
        self.account = account
        self.proxy = proxy


        self.bot(site,product_num,size,account,proxy)


    def bot(self,site,product_num,size,account,proxy):
        """
        :param site: name of site(string)
        :param product_num: product number(string)
        :param size: size of product(string)
        :return: no return
        """


        if site == "footaction" or site == "eastbay" or site == "champs" or site == "footlocker":
            task = FootSite()
            task.buy(site, product_num, size, account, proxy)
        if site == "supreme":
            pass
        if site == "yeezysupply":
            pass
        if site == "addidas":
            pass
        if site == "nike":
            pass
        if site == "shopify":  # Probably have to create separate if statement for each shopify site
            pass
        #Shopify list:
        if site == "kith":
            pass



