# -*- coding: utf-8 -*-
from flib.FTaskCenter import FTask, FTaskCenter

class FileTask(FTask):
    def __init__(self, publisher = None):
        super(FileTask, self).__init__(publisher)
        self.success = False
        self.result = {}
    def __work__(self):
        for x in range(1,1000):
            self.result[x] = 1
    def getResult(self):
        return self.result


def main():
    mgr = FTaskCenter()
    mgr.addTask(FileTask(mgr))
    mgr.addTask(FileTask(mgr))
    mgr.run(True)
    pass

if __name__ == "__main__":
    main()