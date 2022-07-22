# About
This is a game I made from python in April/May 2020 with the pygame library.  
The game is simply the well-known Snake game.
If you have never played it, then where have you been, caveman?😉  
Nevertheless, I added a new item so that the snake can consume it to reduce its body length.  
</br>

# Playing the game
### Steps to run the game through python
1. Locate the Code folder.
    - In the folder contains a data folder which stores data required for visuals, sfx and highscore.
    - The SnakeGame.py file contains python code for the menus, game mechanics, etc.
2. Since I have little knowledge on virtual environments at that time, I didn't create one. The modules you need are:
    - python v3.7.4
    - pygame v1.9.2
3. Once you have these libraries installed, you can run the code with the said python version in step 2.
4. Enjoy!

### Steps to run the game through application
1. Extract the Hisssss.zip folder to anywhere you'd like. (Extract in a new directory is recommended)
2. Run the SneakySnake.exe application. (Make sure the data folder is in the same directory as the application)
3. Enjoy!
</br>

# Additional notes
- If you feel like you can't immediately turn directions, it's because of how the code is setup.
  - The game runs on a fps (frames per second) basis, and initially the fps of the game is quite low and the time taken for one frame to go to the next will take much longer. 
  - So when an input is given, it will have to wait until the frame is called and then the commands can be called.
  - As the snake consume more coins, the fps will increase to give a sense of speed (since the frames are called much frequently).
- I have referenced the snake movement script from some youtube videos (I forgot which videos I have referenced from)
