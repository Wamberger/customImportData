
from prop import prop
from util.lists_of_data_labels import propNames


class Prompts():
    def __init__(self, args):
        self.importFile = args.importFile

    def compilePrompsWithAppProp(self):
        for p in propNames:
            if p in prop:
                setattr(self, p, prop[p])
            else:
                setattr(self, p, '')
        # Bool cannot be add in properties
        self.dictReader = True if self.dictReader == 'J' else False
        self.testRun = True if self.testRun == 'J' else False

