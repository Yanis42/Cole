from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from xml.etree import ElementTree as ET

try:
    actorTree = ET.parse("./actorList.xml")
except:
    raise print("[Cole:ERROR]: File not found or malformed!")

actorRoot = actorTree.getroot()

def searchActor(searchInput: str):
    searchResult = None

    for actorNode in actorRoot:
        curID = actorNode.get('ID')
        curName = actorNode.get('Name')
        if curID is not None:
            searchInput = searchInput.lower()
            curID = curID.lower()
            curName = curName.lower()

            if searchInput in curID:
                searchResult = curID

            if searchInput in curName:
                searchResult = curName

            if searchResult is not None:
                print(f"Search result: {searchResult}")
                break

class MainWindow(FloatLayout):
    def actorInputCallback(self):
        actorName = self.ids.actorInput.text
        searchActor(actorName)

class Main(App):
    def build(self):
        return MainWindow()

if __name__ == "__main__":
    Main().run()
