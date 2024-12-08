# Ultralytics YOLO 🚀, AGPL-3.0 license

import contextlib
import importlib.metadata
import inspect
import json
import logging.config
import os
import platform
import re
import subprocess
import sys
import threading
import time
import urllib
import uuid
from pathlib import Path
from threading import Lock
from types import SimpleNamespace
from typing import Union

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
import yaml
from tqdm import tqdm as tqdm_original

from ultralytics import __version__
from .plotting import Annotator
from .plotting import Annotator

__all__ = ["Annotator"]

