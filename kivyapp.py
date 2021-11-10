from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '650')

import kivy
kivy.require("1.9.1")

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen
from  kivy.uix.filechooser import FileChooserListView

from imageai.Detection import ObjectDetection

import time

import pyttsx3

import cv2

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascPath)

Builder.load_string("""
<SmoothButton@Button>:
    font_size: (self.height+self.width)/11
    background_color: (0,0,0,0)
    background_normal: ''
    back_color: (1,0,1,1)
    border_radius: [18]
    canvas.before:
        Color:
            rgba: self.back_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: self.border_radius
    
<ScreenOne>:
    BoxLayout:
        Button:
            background_normal: 'img\logo.jpg'
            background_down: 'img\logo.jpg'
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 0.5
                root.manager.current = 'screen_two'

<ScreenTwo>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        SmoothButton:
            font_size: (self.height+self.width)/18
            text:"OCR & Object Recognition"
            size_hint:.9,.25
            pos_hint:{"center_x":.5,"center_y":.5}
            back_color: (0.157,0.455,0.953,1.0)
            border_radius: [0,0,18,18]
            on_press:root.info()
        Label:
            id: fps
            font_size: (self.height+self.width)/25 if self.show else 0
            color: (0.157,0.455,0.953,1.0)
            text: 'FPS : ' + camera.fps
            size_hint:1,.15
            show: False
        KivyCamera:
            id: camera
            size_hint:1,1
            resolution: (1280,720)
            detect: False
            green_mode: False
            show_fps: False
            fps: '0'
        TabbedPanel:
            do_default_tab: False
            size_hint:1,.6
            tab_pos:'top_mid'
            background_color: (0, 0, 0, 0)
            tab_width: self.size[0] / 4
            TabbedPanelItem:
                background_normal: 'img\left.png'
                background_down: 'img\left.png'
                BoxLayout:
                    spacing: 10
                    Button:
                        background_normal: 'img\detect.png'
                        background_down: 'img\detect.png'
                        size_hint:.6,.9
                        on_press: camera.detect = not camera.detect
                        on_press: root.face()
                    Button:
                        background_normal: 'img\shutter.png'
                        background_down: 'img\shutter.png'
                        size_hint:.6,.9
                        on_press:root.capture()
                    Button:
                        background_normal: 'img\gallery.png'
                        background_down: 'img\gallery.png'
                        size_hint:.6,.9
                        on_press:root.open_popup()
            TabbedPanelItem:
                background_normal: 'img\_right.png'
                background_down: 'img\_right.png'
                BoxLayout:
                    spacing: 10
                    Button:
                        background_normal: 'img\green.png'
                        background_down: 'img\green.png'
                        size_hint:.6,.9
                        on_press: camera.green_mode = not camera.green_mode
                        on_press: root.night()
                    Button:
                        id: sound
                        size_hint:.6,.9
                        background_normal: 'img\soundon.png'
                        background_down: 'img\soundon.png'
                        on_press: root.sound()
                    Button:
                        background_normal: 'img\count.png'
                        background_down: 'img\count.png'
                        size_hint:.6,.9
                        on_press: fps.show = not fps.show
                        on_press: root.fps()
""")

class ScreenOne(Screen):
    pass

class ScreenTwo(Screen):

    count = 0
    facecount = 0
    nightcount = 0
    fpscount = 0
    soundcount = 0
    
    def info(self):
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        label1 = Label(text="Developed by : ")
        popupBtn = Button(text="Aryan Gupta ",size_hint=(1,.1),background_color=(0,0,0,0),on_press=lambda x:self.easteregg())
        label2 = Label(text="\n      Aryan Porwal\n\n    Ashutosh Singh\n\nAshutosh Choudhary")
        print("Developed by \nAryan Gupta\nAryan Porwal\nAshutosh Singh\nAshutosh Choudhary")
        closeButton = Button(background_normal='img\close.png', background_down='img\close.png',size_hint=(.3,1), pos_hint={"center_x": .5})
        layout.add_widget(label1)
        layout.add_widget(popupBtn)
        layout.add_widget(label2)
        layout.add_widget(closeButton)
        popup = Popup(title='Info', content=layout, size_hint=(.8, .6))
        popup.open()
        closeButton.bind(on_press=popup.dismiss)

    def easteregg(self):
        self.count += 1
        if self.count == 11:
            engine = pyttsx3.init()
            if self.soundcount == 0:
                engine.say("Welcome Aryan .")
            print("Welcome Aryan .")
            engine.runAndWait()

    def open_popup(self):
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        select = BoxLayout(size_hint=(1, .25),spacing=10, padding=10)
        gallery = FileChooserListView(size_hint=(1, 1),path="./")
        object = Button(background_normal= '',background_color=(0.157,0.455,0.753,1.0),text="Object")
        text = Button(background_normal= '',background_color=(0.157,0.455,0.753,1.0), text="Text")
        closeButton = Button(background_normal='img\close.png', background_down='img\close.png', size_hint=(.38, .4),
                             pos_hint={"center_x": .5})

        layout.add_widget(gallery)
        select.add_widget(object)
        select.add_widget(text)
        layout.add_widget(select)
        layout.add_widget(closeButton)
        popup = Popup(title='Filemanager', content=layout, size_hint=(.8, .9))
        popup.open()
        object.bind(on_release=lambda x:self.object(gallery.selection))
        text.bind(on_release=lambda x: self.text(gallery.selection))
        closeButton.bind(on_press=popup.dismiss)

    def object(self, selection):
        if selection == []:
            layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
            popupLabel = Label(text="No file is selected .")
            print("No file is selected .")
            closeButton = Button(background_normal='img\close.png', background_down='img\close.png',
                                 size_hint=(.38, .6), pos_hint={"center_x": .5})
            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)
            popup = Popup(title='Error', content=layout, size_hint=(.8, .6))
            popup.open()
            closeButton.bind(on_press=popup.dismiss)
            engine = pyttsx3.init()
            print("No file is selected .")
            if self.soundcount == 0 :
                engine.say("No file is selected .")
            engine.runAndWait()
        else :
            engine = pyttsx3.init()
            print("Please Wait .")
            if self.soundcount == 0:
                engine.say("Please Wait .")
            engine.runAndWait()
            detector = ObjectDetection()
            model_path = "./model/yolo-tiny.h5"
            input_path = selection[0]
            output_path = "{} obj.png".format(selection[0])
            detector.setModelTypeAsTinyYOLOv3()
            detector.setModelPath(model_path)
            detector.loadModel()
            detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)
            engine = pyttsx3.init()
            print("Input Path : {}".format(input_path))
            print("Output Path : {}".format(output_path))
            if self.soundcount == 0:
                engine.say("There are ")
            print("There are ")
            flag = 0
            temp=""
            items=""
            for eachItem in detection:
                print(eachItem["name"], " : ", eachItem["percentage_probability"])
                if self.soundcount == 0:
                    if eachItem["name"] != temp:
                        engine.say(eachItem["name"])
                        temp = eachItem["name"]
                        items = items + temp + ", "
                flag = flag + 1
            if flag == 0:
                if self.soundcount == 0:
                    engine.say("no object's in the image .")
                print("no object's in the image .")
            else:
                if self.soundcount == 0:
                    engine.say("in the image .")
                print("in the image .")
            layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
            popupImage = Image(source = output_path)
            closeButton = Button(background_normal='img\close.png', background_down='img\close.png', size_hint=(.38, .31),
                                 pos_hint={"center_x": .5})
            layout.add_widget(popupImage)
            layout.add_widget(closeButton)
            popup = Popup(title=items, content=layout, size_hint=(.8, .9))
            popup.open()
            closeButton.bind(on_press=popup.dismiss)
            engine.runAndWait()

    def text(self,selection):
        if selection==[]:
            layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
            popupLabel = Label(text="No file is selected .")
            print("No file is selected .")
            closeButton = Button(background_normal='img\close.png', background_down='img\close.png',
                                 size_hint=(.38, .6), pos_hint={"center_x": .5})
            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)
            popup = Popup(title='Error', content=layout, size_hint=(.8, .6))
            popup.open()
            closeButton.bind(on_press=popup.dismiss)
            engine = pyttsx3.init()
            if self.soundcount == 0:
                engine.say("No file is selected .")
            print("No file is selected .")
            engine.runAndWait()
        else :
            print("Input Path : {}".format(selection[0]))
            try:
                from PIL import Image
            except ImportError:
                import Image
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = 'C:\Softwares\Tesseract-OCR\Tesseract.exe'
            text = pytesseract.image_to_string(Image.open(selection[0]))
            if text=="":
                text="There is no text in the image ."
            layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
            popupLabel = Label(text=text)
            closeButton = Button(background_normal='img\close.png', background_down='img\close.png',
                                 size_hint=(.38, .31), pos_hint={"center_x": .5})
            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)
            popup = Popup(title='Text Recognition', content=layout, size_hint=(.8, .9))
            popup.open()
            closeButton.bind(on_press=popup.dismiss)
            print(text)
            engine = pyttsx3.init()
            if self.soundcount == 0:
                engine.say(text)
            engine.runAndWait()

    def sound(self):
        engine = pyttsx3.init()
        if self.soundcount == 0:
            self.ids['sound'].background_normal='img\soundoff.png'
            self.ids['sound'].background_down = 'img\soundoff.png'
            engine.say("Sound is OFF")
            print("Sound is OFF")
            self.soundcount += 1
        else:
            self.ids['sound'].background_normal = 'img\soundon.png'
            self.ids['sound'].background_down = 'img\soundon.png'
            engine.say("Sound is ON")
            print("Sound is ON")
            self.soundcount = 0
        engine.runAndWait()

    def face(self):
        engine = pyttsx3.init()
        if self.facecount == 0:
            if self.soundcount == 0:
                engine.say("Face Detection is ON")
            print("Face Detection is ON")
            self.facecount += 1
        else:
            if self.soundcount == 0:
                engine.say("Face Detection is OFF")
            print("Face Detection is OFF")
            self.facecount = 0
        engine.runAndWait()

    def night(self):
        engine = pyttsx3.init()
        if self.nightcount == 0:
            if self.soundcount == 0:
                engine.say("Night Mode is ON")
            print("Night Mode is ON")
            self.nightcount += 1
        else:
            if self.soundcount == 0:
                engine.say("Night Mode is OFF")
            print("Night Mode is OFF")
            self.nightcount = 0
        engine.runAndWait()

    def fps(self):
        engine = pyttsx3.init()
        if self.fpscount == 0:
            if self.soundcount == 0:
                engine.say("FPS Counter is ON")
            print("FPS Counter is ON")
            self.fpscount += 1
        else:
            if self.soundcount == 0:
                engine.say("FPS Counter is OFF")
            print("FPS Counter is OFF")
            self.fpscount = 0
        engine.runAndWait()

    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = "camera\IMG_{}.png".format(timestr)
        camera.export_to_png(filename)
        engine = pyttsx3.init()
        print("Captured")
        if self.soundcount == 0:
            engine.say("Captured")
        engine.runAndWait()
        print("Input Path : {}".format(filename))

class KivyCamera(Image):
    def __init__(self, fps=30, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / fps)
        self.actual_fps = []
    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return frame

    def frame_to_texture(self, frame):
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return image_texture

    def update_fps(self):
        self.actual_fps.append(Clock.get_fps())
        self.fps = str(self.actual_fps[-1])

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            return
        if self.detect:
            self.detect_faces(frame)
        if self.green_mode:
            frame[:, :, 2] = 0
            frame[:, :, 0] = 0
        self.update_fps()
        self.texture = self.frame_to_texture(frame)

screen_manager = ScreenManager()
screen_manager.add_widget(ScreenOne(name="screen_one"))
screen_manager.add_widget(ScreenTwo(name="screen_two"))

class kivyapp(App):
    def build(self):
        return screen_manager

obj = kivyapp()
obj.run()