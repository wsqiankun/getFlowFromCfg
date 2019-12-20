import os
import sys
import time
import configparser

class CfgParser:
    def __init__(self,cfgPath):
        self.conf = configparser.ConfigParser()
        self.conf.read(cfgPath)

    def get_test_cfg(self):
        test_type = self.conf.get("TEST_CONFIG", "test_type")
        loop = self.conf.getint("TEST_CONFIG", "loop")
        first_step = self.conf.get("TEST_CONFIG", "first_step")

        return {"test_type":test_type, "loop":loop, "first_step":first_step}

    def get_mysql_conf(self):
        host = self.conf.get("mysql", "host")
        user = self.conf.get("mysql", "user")
        passwd = self.conf.get("mysql", "passwd")
        database = self.conf.get("mysql", "database")
        
        return {"host":host, "user":user, "passwd":passwd, "database":database}

    def get_next_test_cfg(self, next_step):
        if next_step == "end":
            return {"test_type": "end"}

        test_type = self.conf.get(next_step, "test_type")
        first_step = self.conf.get(next_step, "first_step")
        test_name = self.conf.get(next_step, "test_name")
        test_loop = self.conf.getint(next_step, "test_loop")
        new_next_step = self.conf.get(next_step, "next_step")

        return {"test_type":test_type, "first_step":first_step, \
            "test_name":test_name, "test_loop":test_loop, \
            "next_step":new_next_step}          

class BaseItem:
    def __init__(self, test_type, test_name, test_label, test_loop, next_step, cfgParser, indent):
        self.testType = test_type
        self.testName = test_name
        self.testLabel = test_label
        self.testLoop = test_loop
        self.nextStep = next_step
        self.cfgParser = cfgParser
        self.indent  = indent
    
    def run(self):
        pass

    def getItem(self, itemName, indent):
        itemDict = self.cfgParser.get_next_test_cfg(itemName)
        item = None
        if itemDict["test_type"] == "single":
            item = SingleCaseItem(itemDict["test_type"], itemDict["test_name"], itemName, \
                itemDict["test_loop"], itemDict["next_step"], self.cfgParser, indent)
        elif itemDict["test_type"] == "group":
            item = GroupItem(itemDict["test_type"], itemDict["first_step"], itemDict["test_name"], itemName, \
                itemDict["test_loop"], itemDict["next_step"], self.cfgParser, indent)
        else:
            pass
            # if self.testType == "group":
            #     print(" " * indent + "last item of group {0}".format(self.testName))
            # else:
            #     print(" " * indent + "last item  of test")
        
        return item
    def getNextItem(self, indent):
        return self.getItem(self.nextStep, indent)
        

class SingleCaseItem(BaseItem):
    def __init__(self, test_type, test_name, test_label, test_loop, next_step, cfgParser, indent):
        super(SingleCaseItem, self).__init__(test_type, test_name, test_label, test_loop, next_step, cfgParser, indent)
    
    def run(self):
        for i in range(self.testLoop):
            print("    "*self.indent + "testname:{0}  testtype:{1}  testlabel:{2} nextstep:{3} loop:{4}".format( \
                self.testName, self.testType, self.testLabel, self.nextStep, i))

        

class GroupItem(BaseItem):
    def __init__(self, test_type, first_step, test_name, test_label, test_loop, next_step, cfgParser, indent):
        super(GroupItem, self).__init__(test_type, test_name, test_label, test_loop, next_step, cfgParser, indent)
        self.firstStep = first_step
    
    def run(self):
        for i in range(self.testLoop):
            print("    "*self.indent + "testname:{0} firststep:{1} testtype:{2} testlabel:{3} nextstep:{4} loop:{5}".format( \
                self.testType, self.firstStep, self.testName, self.testLabel, self.nextStep, i))
            item = self.getItem(self.firstStep, self.indent + 1)
            while item is not None:
                item.run()
                item = item.getNextItem(self.indent + 1)


class Test:
    def __init__(self, cfgPath):
        self.cfgParser = CfgParser(cfgPath)
        self.testType = self.getTestType()
        self.testLoop = self.getTestLoop()
        self.firstItemName = self.getFirstTestItemName()
    
    def getTestType(self):
        return self.cfgParser.get_test_cfg()["test_type"]

    def getTestLoop(self):
        return self.cfgParser.get_test_cfg()["loop"]

    def getFirstTestItemName(self):
        return self.cfgParser.get_test_cfg()["first_step"]

    def getItemType(self, nextItemName):
        itemDict = self.cfgParser.get_next_test_cfg(nextItemName)
        return itemDict["test_type"]
    
    def getFirstItem(self):
        item = None
        itemDict = self.cfgParser.get_next_test_cfg(self.firstItemName)
        if itemDict["test_type"] == "single":
            item = SingleCaseItem(itemDict["test_type"], itemDict["test_name"], self.firstItemName, \
                itemDict["test_loop"], itemDict["next_step"], self.cfgParser, 1)
        elif itemDict["test_type"] == "group":
            item = GroupItem(itemDict["test_type"], itemDict["first_step"], itemDict["test_name"], self.firstItemName, \
                itemDict["test_loop"], itemDict["next_step"], self.cfgParser, 1)
        else:
            print("last item  of test")
        
        return item

    def run(self):
        for i in range(self.testLoop):
            print("test main loop {0}".format(i))
            item = self.getFirstItem()
            while item is not None:
                item.run()
                item = item.getNextItem(1)

if __name__ == "__main__":
    test = Test("./example.cfg")
    test.run()
