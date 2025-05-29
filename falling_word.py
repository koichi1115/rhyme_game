import pygame
import random

class FallingWord:
    """落下する単語を表すクラス"""
    
    def __init__(self, word, x, width, is_correct, speed=1.0, color=(255, 255, 255)):
        self.word = word
        self.x = x
        self.y = 0  # 画面上部から開始
        self.width = width
        self.height = 40
        self.is_correct = is_correct  # 正解の単語かどうか
        self.speed = speed  # 落下速度
        self.color = color
        self.rect = pygame.Rect(x, self.y, self.width, self.height)
        self.active = True
        self.clicked = False
        self.explosion_time = 0
        self.explosion_duration = 0.5  # 爆発エフェクトの持続時間（秒）
        self.explosion_radius = 0
        self.explosion_max_radius = 50
        self.explosion_color = (255, 255, 0) if is_correct else (255, 0, 0)
        
    def update(self, dt):
        """単語の位置を更新"""
        if not self.active:
            return False
            
        if self.clicked:
            # 爆発エフェクト中
            self.explosion_time += dt
            self.explosion_radius = int(self.explosion_max_radius * (self.explosion_time / self.explosion_duration))
            if self.explosion_time >= self.explosion_duration:
                self.active = False
            return True
            
        # 通常の落下
        self.y += self.speed * dt * 100  # 速度に応じて落下
        self.rect.y = int(self.y)
        return True
        
    def draw(self, screen, font):
        """単語を描画"""
        if not self.active:
            return
            
        if self.clicked:
            # 爆発エフェクトを描画
            pygame.draw.circle(screen, self.explosion_color, 
                              (self.rect.centerx, self.rect.centery), 
                              self.explosion_radius)
            return
            
        # 単語の背景を描画
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        
        # 単語テキストを描画
        text_surf = font.render(self.word, True, self.color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_click(self, pos):
        """クリック判定"""
        if not self.active or self.clicked:
            return False
        return self.rect.collidepoint(pos)
        
    def explode(self):
        """爆発エフェクトを開始"""
        self.clicked = True
        self.explosion_time = 0
        
    def is_below_line(self, line_y):
        """指定したラインより下に落ちたかどうか"""
        return self.rect.top > line_y
