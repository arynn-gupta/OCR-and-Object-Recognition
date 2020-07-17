# Projekt

Python application for object detection and text recognition using kivy for gui and tensorflow for object recognition .

----------------------------------------

# Install the following modules before running the application 

Upgrade PIP :

python -m pip install --upgrade pip

----------------------------------------

ObjectDetection :

pip install tensorflow-cpu

pip install opencv-python

pip install keras

pip install imageAI

----------------------------------------

Optical Character Recognition :

pip install Pillow

pip install pytesseract

Note:   Download and install tesseract-ocr setup file in the following location :
	C:\Softwares\Tesseract-OCR
	After installing rename the tesseract.exe file within the Tesseract-OCR folder to Tesseract.exe

----------------------------------------

TextToSpeech :

pip install pyttsx3

Note :  If you receive errors such as No module named win32com.client, No module named win32, or No
	module named win32api, you will need to additionally install pypiwin32.
	pip install pypiwin32

----------------------------------------

Gui ( kivy ) :

python -m pip install --upgrade pip wheel setuptools

python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew

python -m pip install kivy.deps.gstreamer

python –m pip install kivy
