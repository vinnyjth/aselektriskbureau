import threading
import sys
import pygame.mixer
import os.path

from threading import Timer
from modules.RotaryDial import RotaryDial
from pygame.mixer import Sound

class TelephoneDaemon:
    # Number to be dialed
    dial_number = ""

    # On/off hook state
    offHook = False

    # Off hook timeout
    offHookTimeoutTimer = None

    RotaryDial = None

    # config = None

    def __init__(self):
        print "[STARTUP]"

        # Rotary dial
        self.RotaryDial = RotaryDial()
        self.RotaryDial.RegisterCallback(NumberCallback = self.GotDigit, OffHookCallback = self.OffHook, OnHookCallback = self.OnHook, OnVerifyHook = self.OnVerifyHook)
        pygame.mixer.init()

        raw_input("Waiting.\n")

    def OnHook(self):
        print "[PHONE] On hook"
        fname = "sound/%s.wav" % self.dial_number
        if os.path.isfile(fname):
            Sound().play()
        else:
            Sound("sound/default.wav").play()
        self.offHook = False

    def OffHook(self):
        print "[PHONE] Off hook"
        self.offHook = True
        # Reset current number when off hook
        self.dial_number = ""


        self.offHookTimeoutTimer = Timer(5, self.OnOffHookTimeout)
        self.offHookTimeoutTimer.start()

    def OnVerifyHook(self, state):
        if not state:
            self.offHook = False

    def GotDigit(self, digit):
        print "[DIGIT] Got digit: %s" % digit
        # self.Ringtone.stophandset()
        self.dial_number += str(digit)
        print "[NUMBER] We have: %s" % self.dial_number

        # Shutdown command, since our filesystem isn't read only (yet?)
        # This hopefully prevents dataloss.
        # TODO: stop rebooting..
        # if self.dial_number == "0666":
        #     self.Ringtone.playfile(self.config["soundfiles"]["shutdown"])
        #     os.system("halt")
        #
        # if len(self.dial_number) == 8:
        #     if self.offHook:
        #         print "[PHONE] Dialing number: %s" % self.dial_number
        #         self.SipClient.SipCall(self.dial_number)
        #         self.dial_number = ""

    def OnSignal(self, signal, frame):
        print "[SIGNAL] Shutting down on %s" % signal
        sys.exit(0)

def main():
    TDaemon = TelephoneDaemon()

if __name__ == "__main__":
    main()
