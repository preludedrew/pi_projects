#!/usr/bin/python

import spidev
import time
import os
import RPi.GPIO as GPIO
import web, threading

# Define sensor channels
LIGHT_CHANNEL = 0

# Define delay between readings
READ_DELAY = .01

# Our buzzer GPIO pin
BUZZ_PIN = 18

LIGHT_THRESHOLD = 300

# Scoring buzz time
SCORE_BUZZ = .50

# End of game buzzer
EOG_BUZZ = 3 

#File to write the current score to
SCORE_FILE = 'score.cur'

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Setup our buzzer
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(18, False)

# Variable used to check if we scored the last iteration
scored = 0

# Scoring
userScore = 0

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
    global LIGHT_THRESHOLD
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
  
    delay = .6

    newScore = 0

    global scored

    if data > LIGHT_THRESHOLD:
        newScore = 1
    else:
        scored = 0
        newScore = 0

    # If we scored ( data > 100) and the last iteration was not counted, return True for scoring
    if newScore == 1 and scored == 0:
        scored = 1
        return True

    return False

# Function to delay the game a number of seconds
def delayGame(count):
    print "Starting gaming in..." 
    while count > 0:
        time.sleep(1)
	Buzz(.2)
        print count, "..."
        count -= 1
    print "Go!!!" 

def Buzz(length):
    GPIO.output(BUZZ_PIN, True)
    time.sleep(length)
    GPIO.output(BUZZ_PIN, False)

def StartGame():
    global userScore
    start_time = time.time()
    print "Welcome, you have 60 seconds to be scored. Good luck!"
    delayGame(5)
    while (time.time() - start_time < 60):
        # Read the light sensor data and score accordingly
        score = ReadChannel(LIGHT_CHANNEL)
        if score == True:
            userScore += 1
            Buzz(.3)
            print "Score == ", userScore
            writeScore(userScore)
        # Wait before repeating loop
        time.sleep(READ_DELAY)

def rating(score):
    if score == 0:
        print("Bad Job")
    elif score >= 1 and score < 4:
        print("Keep practicing")
    elif score >= 4 and score < 8:
        print("Not bad!")
    elif score >= 8 and score < 12:
        print("Good job!")
    else:
        print("You are the BEST!")

def writeScore(score):
    handle = open(SCORE_FILE, "w")
    handle.write(str(score))
    handle.close

def delScoreFile():
    os.remove(SCORE_FILE)

StartGame()
Buzz(EOG_BUZZ)
print "Your score: ", userScore
rating(userScore)
