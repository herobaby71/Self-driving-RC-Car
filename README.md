# Self-driving-RC-Car
![car](https://user-images.githubusercontent.com/26393308/29645509-0d6d2002-884c-11e7-8429-4c4056190753.jpg)

What I needed:
1) Raspberry pi, picamera, SD card, monitor, external mouse, female-male jumper wires.
2) External battery pack
3) A GOOD RC Car (The project will be VERY troublesome if you have a mediocre RC Car with mediocre servo). Make sure that the car is controllable in both speed and direction. A fast car will make it hard to control in general. An inconsistent servo will make it hard to predict the angle to which the car moves when turn. Do Not make the same mistake as me.

The goal of this project is to:
1) Learn how Raspberry Pi GPIOs and PiCamera works
2) Learn how to create interactive GUI with pygame
3) Use Intel OpenCV to detect lanes.
4) Apply previously learned NN models to something more fun and practical

The Project can be divided into 5 steps:
1) Setting up the Raspberry Pi and the RC Car
2) Use Socketing to feed images from the Raspberry Pi to the Computer 
3) Train a model (Feel free to use other libraries such as Keras or Tensorflow)

Step 1) Setting up the Raspberry Pi and the RC Car:
1) Install Raspian, set up wifi, remote desktop, WinSCP for sharing file. Tutorials: https://pythonprogramming.net/introduction-raspberry-pi-tutorials/
2) I need a way to send signal to the RC Car from the Raspberry Pi. In order to do so, I use bskari lib: https://github.com/bskari/pi-rc. Basically, run his programs on the raspberry pi will iterate through all the possible frequencies, burst micro sec, and spacing to find the correct frequencies that move your car (my freq is 26.995). Afterward, test all the repeats from 0 -> ~155 signal to find the appropriate commands (forward, backward, left, right, forward left, etc). -> Export to a JavaScripe Object Notation (JSON) file.


Step 2) Use Socketing to feed images from the Raspberry Pi to the Computer 
1) Set up a socket connection between your computer and the raspberry pi for image streaming: http://picamera.readthedocs.io/en/release-1.10/recipes1.html. Or you can use multithreading as well to stream more fps.
2) Create a GUI and connect command signals to keyboard buttons. See control.py and pygameContol.py
3) Read stream images, preprocess it, and save the data before feeding it through the NN (resizing and normalizing are important, convert to gray scale is optional). See LaptopServerDataCollection.py

Step 2.5) Putting everything together:
1) Remote desktop to your RaspPi, start bskari pi_pcm so that control.py able to send signal command to the RaspPi.
2) Another Remote desktop to your RaspPi, start RaspSensorClientInput.py
3) On your Desktop, run LaptopServerDataCollection.py, you will see a pygame window with piCamera vision that will take arrow inputs from your keyboard. Press 's' to start collecting data and 'p' to pause. Quit pygame window if done collecting. The program will save the collected data to an .npy file.

Step 3) Train a model (Feel free to use other libraries such as Keras or Tensorflow)
1) I created my own Neuronetwork from scratch using numpy and sklearn for second order l-bfgs optimizing method. However, my model only have sigmoid activation function, which cannot avoid gradient vanishing problem. ELU or ReLU activation functions probably works better.
1.5) Balance your data
2) Any furthur from this point, I cannot say because the dataset I collected is so bad that the car is doing random moves. However, if you got a good car, you can take one step furthur than me and build a great self-driving RC car :). Side Note: if possible, you can use Tensorflow on Google Cloud compute engine with GPU to train even a better, deeper conv model.

Extra) Recognizing lanes (white papers) using OpenCV. See Lane-Finding.py based on a tutorial on PythonProgramming.net
