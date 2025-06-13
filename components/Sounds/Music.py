import flet as ft
class Music:
    def __init__(self, src, page, volume = 0.5, to_be_invoked = False, replay = False):
        self.page = page
        self.is_playing = False
        self.audio = ft.Audio(src=src,volume=volume,on_state_changed=lambda e: self.__audio_state_changed(e, replay))
        self.page.add(self.audio)
        
        if to_be_invoked:
            self.audio.play()
            self.page.update()

    def __audio_state_changed(self,e,replay):
        if replay and e.data == "completed":
            self.audio.play()
            self.page.update()

    def play(self):
        self.is_playing = True
        self.page.overlay.append(self.audio)
        self.audio.play()
        self.page.update()
    
    def call(self):
        self.audio.play()
        self.page.update()

    def stop(self):
        self.is_playing = False
        self.audio.pause()
        self.page.update()

    def resume(self):
        self.is_playing = True
        self.audio.resume()
        self.page.update()
        