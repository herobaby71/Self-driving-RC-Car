# Self-driving-RC-Car
The goal of this project is to:
1) Learn how Raspberry Pi GPIOs and PiCamera works
2) Understand socketing and concurrency (streaming images)
3) Apply previously learned NN models to something more fun and practical

The Project can be divided into 5 steps:
1) Setting up the Raspberry Pi and the RC Car
2) Use Socketing to feed images from the Raspberry Pi to the Computer 
3) Train a model (Feel free to use other libraries such as Keras or Tensorflow)

Step 1) Setting up the Raspberry Pi and the RC Car:
1) First, I need a way to send signal to the RC Car from the Raspberry Pi. In order to do so, I use bskari lib: https://github.com/bskari/pi-rc
   
ad
