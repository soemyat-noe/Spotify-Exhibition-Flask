from flask import Flask, render_template, request
from gallery_spotify.py import get_songs


app = Flask(__name__)
