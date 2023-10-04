


class dirBase:
    def __init__(self):
        self.pathList = []
        self.levelList = []
        self.levels = 0
        self.currentLevel = 0

    def addPath(self, vaName, path):
        print(f"Adding volasm {vname} path {path}")
        self.pathList.append({vaName, path})
        if self.levels == self.currentLevel:
            self.levelList.append(level())
        else:
            self.levelList[self.currentLevel].addVolAsm(vaName, path)
        self.currentLevel += 1

class level:
    def __init__(self, vaName, path):
        self.level = 1
        self.volList = [{vaName, path}]
        self.currentLevel = 1

    def addVol(self, volAsm, path):
        self.volList.append({volAsm, path})
        self.level = += 1
