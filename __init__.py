# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

from pixel_ring import pixel_ring
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message
from mycroft.util.log import LOG

class PixelRingSkill(MycroftSkill):

    def __init__(self):
        super(PixelRingSkill, self).__init__(name="PixelRingSkill")

    def initialize(self):
        pixel_ring.set_brightness(10)
        pixel_ring.off()
        pixel_ring.set_vad_led(0)

    def shutdown(self):
        pixel_ring.off()

    def handle_listener_wakeup(self, message):
        pixel_ring.listen()
        pixel_ring.set_vad_led(2)

    def handle_listener_think(self, message):
        pixel_ring.think()

    def handle_listener_speak(self, message):
        pixel_ring.speak()

    def handle_listener_off(self, message):
        pixel_ring.off()
        pixel_ring.set_vad_led(0)
    
    @intent_handler(IntentBuilder("").require("EnablePixelRing"))
    def handle_enable_pixel_ring_intent(self, message):
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
        self.speak_dialog("EnablePixelRing")

    @intent_handler(IntentBuilder("").require("DisablePixelRing"))
    def handle_disable_pixel_ring_intent(self, message):
        self.remove_event('recognizer_loop:record_begin')
        self.remove_event('recognizer_loop:record_end')
        self.remove_event('recognizer_loop:audio_output_start')
        self.remove_event('recognizer_loop:audio_output_end')
        self.remove_event('mycroft.skill.handler.start')
        self.remove_event('mycroft.skill.handler.complete')
        self.speak_dialog("DisablePixelRing")
        ## set back to normal function
        pixel_ring.trace()
        pixel_ring.set_vad_led(2)
        

def create_skill():
    return PixelRingSkill()
