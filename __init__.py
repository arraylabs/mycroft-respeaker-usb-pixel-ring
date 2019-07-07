# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

import time
from pixel_ring import pixel_ring
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message
from mycroft.util.log import LOG

class PixelRingSkill(MycroftSkill):

    def __init__(self):
        super(PixelRingSkill, self).__init__(name="PixelRingSkill")

    def initialize(self):
        #LOG.debug("initialising")

        pixel_ring.set_brightness(10)

        self.add_event('recognizer_loop:record_begin',
                       self.handle_listener_wakeup)
        self.add_event('recognizer_loop:record_end', self.handle_listener_off)
        self.add_event('recognizer_loop:audio_output_start',
                       self.handle_listener_speak)
        self.add_event('recognizer_loop:audio_output_end',
                       self.handle_listener_off)
        self.add_event('mycroft.skill.handler.start',
                       self.handle_listener_think)
        self.add_event('mycroft.skill.handler.complete',
                       self.handle_listener_off)
        pixel_ring.off()
        pixel_ring.set_vad_led(0)

    def shutdown(self):
        #LOG.debug("shutdown")
        pixel_ring.off()
        self.en.write(1)

    def handle_listener_wakeup(self, message):
        #LOG.debug("listen")
        pixel_ring.set_vad_led()
        pixel_ring.listen()
        

    def handle_listener_think(self, message):
        #LOG.debug("think")
        pixel_ring.think()

    def handle_listener_speak(self, message):
        #LOG.debug("speak")
        pixel_ring.speak()

    def handle_listener_off(self, message):
        #LOG.debug("off")
        pixel_ring.off()
        pixel_ring.set_vad_led()
    
    @intent_handler(IntentBuilder("").require("EnablePixelRing"))
    def handle_enable_pixel_ring_intent(self, message):
        self.speak_dialog("EnablePixelRing")

    @intent_handler(IntentBuilder("").require("DisablePixelRing"))
    def handle_disable_pixel_ring_intent(self, message):
        pixel_ring.trace()
        self.speak_dialog("DisablePixelRing")
        

def create_skill():
    return PixelRingSkill()
