from selenium import webdriver
import os


def find_file(base="C:\\", name=None):
    for root, dirs, filename in os.walk(base):
        if name in filename:
            return os.path.join(root, name)


def open_file(filepath):
    with open(filepath, "r") as js:
        return js.read()


# Solution from http://elementalselenium.com/tips/39-drag-and-drop
js_path = find_file(name="dnd.js")
js_script1 = open_file(js_path)
js_script2 = """
$('#column-a').simulateDragDrop({ dropTarget: '#column-b'});
"""
driver = webdriver.Firefox(executable_path=find_file(name="geckodriver.exe"))
driver.get('https://the-internet.herokuapp.com/drag_and_drop')
driver.execute_script(js_script1 + js_script2)
