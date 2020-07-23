import glob
import os
import time
from network import Network
import pickle
import threading

import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

import consoleapp.game as game
from consoleapp.cards import *
from consoleapp.player import *

Builder.load_file('design.kv')

net = Network()
