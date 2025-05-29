import pygame
import os

class SoundManager:
    def __init__(self):
        # サウンドファイルのパス
        self.sound_dir = os.path.join(os.path.dirname(__file__), "assets", "sounds")
        
        # 効果音の初期化
        self.sounds = {
            "correct": self._create_dummy_sound(),
            "wrong": self._create_dummy_sound(),
            "click": self._create_dummy_sound(),
            "game_over": self._create_dummy_sound(),
            "level_up": self._create_dummy_sound()
        }
        
        # BGMの初期化
        self.bgm = {
            "title": self._create_dummy_sound(),
            "gameplay": self._create_dummy_sound(),
            "game_over": self._create_dummy_sound()
        }
        
        # BGMの状態
        self.current_bgm = None
        
        # 実際のサウンドファイルを読み込む
        self.load_real_sounds()
        
    def _create_dummy_sound(self):
        """ダミーのサウンドオブジェクトを作成"""
        # 1秒間の無音を作成
        buffer = bytearray(44100 * 2)  # 44.1kHz, 16-bit mono
        dummy_sound = pygame.mixer.Sound(buffer=buffer)
        dummy_sound.set_volume(0.0)  # 音量を0に設定
        return dummy_sound
    
    def load_real_sounds(self):
        """実際のサウンドファイルを読み込む"""
        try:
            # 効果音の読み込み
            sound_files = {
                "correct": "success.mp3",
                "wrong": "fail.mp3",
                "click": "click.mp3",
                "game_over": "game-over.mp3",
                "level_up": "level-up.mp3"
            }
            
            for sound_name, file_name in sound_files.items():
                file_path = os.path.join(self.sound_dir, file_name)
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    # 音量調整
                    if sound_name == "correct":
                        self.sounds[sound_name].set_volume(0.7)
                    elif sound_name == "wrong":
                        self.sounds[sound_name].set_volume(0.7)
                    elif sound_name == "click":
                        self.sounds[sound_name].set_volume(0.5)
                    elif sound_name == "level_up":
                        self.sounds[sound_name].set_volume(0.8)
                    else:
                        self.sounds[sound_name].set_volume(0.7)
            
            # BGMの読み込み
            bgm_files = {
                "title": "title.mp3",
                "gameplay": "main.mp3",
                "game_over": "game_over.mp3"
            }
            
            for bgm_name, file_name in bgm_files.items():
                file_path = os.path.join(self.sound_dir, file_name)
                if os.path.exists(file_path):
                    self.bgm[bgm_name] = pygame.mixer.Sound(file_path)
                    # BGMの音量は少し小さめに設定
                    self.bgm[bgm_name].set_volume(0.4)
                    
            print("Sound files loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading sounds: {e}")
            return False
    
    def play_sound(self, sound_name):
        """効果音を再生"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_bgm(self, bgm_name, loop=True):
        """BGMを再生"""
        if bgm_name in self.bgm:
            # 現在のBGMを停止
            if self.current_bgm:
                self.bgm[self.current_bgm].stop()
            
            # 新しいBGMを再生
            self.current_bgm = bgm_name
            if loop:
                self.bgm[bgm_name].play(-1)  # -1はループ再生
            else:
                self.bgm[bgm_name].play()
    
    def stop_bgm(self):
        """BGMを停止"""
        if self.current_bgm:
            self.bgm[self.current_bgm].stop()
            self.current_bgm = None
    
    def set_volume(self, volume):
        """全体の音量を設定"""
        for sound in self.sounds.values():
            sound.set_volume(volume)
        
        for bgm in self.bgm.values():
            bgm.set_volume(volume * 0.7)  # BGMは少し小さめに
