import objc, sys, random, inspect, os
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
from datetime import datetime

def find_in(ranges, value):
  for (b,e) in ranges:
    if b <= value <= e:
      return (b,e)


def datetime_to_chime(dt):
  mapping = {(52, 59):0, (0, 8):0,
             (8, 22):1, (23, 37):2, (38, 51):3}
  minute_range = find_in(mapping, dt.minute)
  quarter_hour_chime = mapping[minute_range]
  if quarter_hour_chime == 0:
    return (["Blow", "Purr", "Hero", "Ping", "Glass"],
            int(dt.strftime("%I")))
  else:
    return (["Submarine"], quarter_hour_chime)

def base_url():
  b = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  return NSURL.fileURLWithPath_(b)

def get_volume_down_script():
  nsa = NSAppleScript.alloc()
  s = NSURL.URLWithString_relativeToURL_("volume_down.scpt", base_url()).absoluteURL()
  return nsa.initWithContentsOfURL_error_(s, None)[0]

def get_volume_up_script():
  nsa = NSAppleScript.alloc()
  s = NSURL.URLWithString_relativeToURL_("volume_up.scpt", base_url()).absoluteURL()
  return nsa.initWithContentsOfURL_error_(s, None)[0]

class Chimey(NSObject):
  sound_names = ["Basso", "Blow", "Bottle", "Frog", "Funk", "Glass", "Hero",
                 "Morse", "Ping", "Pop", "Purr", "Sosumi", "Submarine", "Tink"]
  sounds = {}
  
  def applicationDidFinishLaunching_(self, notification):
    get_volume_down_script().executeAndReturnError_(None)
    random.seed()
    for name in self.sound_names:
      self.sounds[name] = NSSound.soundNamed_(name)
      self.sounds[name].setDelegate_(self)
    (self.sequence, self.count) = datetime_to_chime(datetime.now())
    if not self.play(None):
      raise Exception("Error playing sound first time")

  def play(self, previous):
    if len(self.sequence) == 1:
      sound = self.sounds[self.sequence[0]]
    else:
      sound = previous
      while (sound == previous):
        sound = self.sounds[random.choice(self.sequence)]
    return sound.play()

  def sound_didFinishPlaying_(self, sound, finishedPlaying):
    if finishedPlaying:
      self.count -= 1
      if self.count <= 0:
        get_volume_up_script().executeAndReturnError_(None)
        AppHelper.stopEventLoop()
      elif not self.play(sound):
        raise Exception("Error playing sound")
    else:
      raise("sound_didFinishPlaying_ called with finishedPlaying = False")
   
def main():
  try:
    import IPython
    ipython_available = True
  except ImportError as e:
    ipython_available = False
  if ipython_available:
    import threading
    #args=[[]] is very important here, otherwise ipython tries to run things from the commandline
    threading.Thread(target=IPython.start_ipython, args=[[]]).start()
  app = NSApplication.sharedApplication()
  delegate = Chimey.alloc().init()
  app.setDelegate_(delegate)
  AppHelper.runEventLoop()
if __name__ == "__main__":
  main()
