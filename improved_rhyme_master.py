import pygame
import sys
import random
import time
import os
from rhyme_data import english_rhyme_pairs
from sound_manager import SoundManager

# Pygameの初期化
pygame.init()
pygame.mixer.init()  # サウンド用の初期化

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dr.sibitt")  # タイトルを変更

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# フォント設定
try:
    title_font = pygame.font.SysFont("Arial", 72)
    main_font = pygame.font.SysFont("Arial", 48)
    button_font = pygame.font.SysFont("Arial", 36)
except:
    title_font = pygame.font.Font(None, 72)
    main_font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 36)

# サウンドマネージャーの初期化
sound_manager = SoundManager()

# ゲーム状態
class GameState:
    def __init__(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.current_word = None
        self.options = []
        self.correct_options = []  # 複数の正解を格納
        self.time_left = 5.0  # 制限時間（秒）
        self.start_time = 0
        self.level = 1
        self.words_cleared = 0
        self.game_active = False
        self.game_over = False
        self.current_pair = None
        
    def new_word(self):
        # ランダムに単語ペアを選択
        self.current_pair = random.choice(english_rhyme_pairs)
        self.current_word = self.current_pair["word"]
        
        # 選択肢を作成（韻を踏む単語と踏まない単語）
        rhyme_words = [rhyme["word"] for rhyme in self.current_pair["rhymes"]]
        non_rhymes = self.current_pair["non_rhymes"]
        
        # 韻を踏む単語から2つ、踏まない単語から2つ選ぶ
        selected_rhymes = random.sample(rhyme_words, min(2, len(rhyme_words)))
        selected_non_rhymes = random.sample(non_rhymes, min(2, len(non_rhymes)))
        
        self.options = selected_rhymes + selected_non_rhymes
        random.shuffle(self.options)  # 選択肢をシャッフル
        
        # 正解の選択肢のインデックスを記録
        self.correct_options = [i for i, option in enumerate(self.options) if option in rhyme_words]
        
        self.start_time = time.time()
        self.time_left = max(5.0 - (self.level * 0.5), 2.0)  # レベルに応じて制限時間を短くする
        
    def check_answer(self, selected_index):
        if selected_index in self.correct_options:
            selected_word = self.options[selected_index]
            
            # 選んだ単語の得点を計算
            points = 100  # デフォルト
            rhyme_type = "perfect"
            
            # 現在の単語ペアから選んだ単語の情報を取得
            for rhyme in self.current_pair["rhymes"]:
                if rhyme["word"] == selected_word:
                    points = rhyme["points"]
                    rhyme_type = rhyme["type"]
                    break
            
            # 韻のタイプに応じたボーナス
            if rhyme_type == "alliteration":  # 頭韻
                points *= 1.5
            elif rhyme_type == "perfect":  # 完全韻
                points *= 1.2
            
            # コンボボーナス
            points *= (1 + self.combo * 0.1)
            
            self.score += points
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            self.words_cleared += 1
            
            # レベルアップ条件
            if self.words_cleared % 5 == 0:
                self.level += 1
                
            return True
        else:
            self.combo = 0
            return False

# アニメーション効果用のクラス
class AnimationEffect:
    def __init__(self, x, y, text, color, size, duration=1.0):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size = size
        self.start_time = time.time()
        self.duration = duration
        self.active = True
        
    def update(self):
        elapsed = time.time() - self.start_time
        if elapsed > self.duration:
            self.active = False
            return
        
        # アニメーション効果（上に浮かび上がりながら消える）
        progress = elapsed / self.duration
        self.y -= 1
        alpha = 255 * (1 - progress)
        
        return self.active
        
    def draw(self):
        if not self.active:
            return
            
        font = pygame.font.SysFont(None, self.size)
        text_surf = font.render(self.text, True, self.color)
        text_surf.set_alpha(int(255 * (1 - (time.time() - self.start_time) / self.duration)))
        screen.blit(text_surf, (self.x, self.y))

# ボタンクラス
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        self.is_hovered = False
        self.animation_offset = 0
        self.animation_direction = 1
        
    def update(self):
        # シンプルなアニメーション効果
        self.animation_offset += 0.2 * self.animation_direction
        if abs(self.animation_offset) > 3:
            self.animation_direction *= -1
        
    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        
        # アニメーション効果を適用した矩形を描画
        animated_rect = self.rect.copy()
        if self.is_hovered:
            animated_rect.y += int(self.animation_offset)
        
        pygame.draw.rect(screen, color, animated_rect)
        pygame.draw.rect(screen, BLACK, animated_rect, 2)  # 枠線
        
        text_surf = button_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=animated_rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

# タイトル画面の描画
def draw_title_screen():
    screen.fill(BLACK)
    
    # タイトル
    title_text = title_font.render("Dr.sibitt", True, YELLOW)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title_text, title_rect)
    
    # サブタイトル
    subtitle_text = main_font.render("Test your rhyming skills!", True, WHITE)
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 60))
    screen.blit(subtitle_text, subtitle_rect)
    
    # スタートボタン
    start_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "START", GREEN)
    start_button.draw()
    
    # 説明
    instruction_text = button_font.render("Select words that rhyme with the given word", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT*3//4))
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()
    return start_button

# ゲーム画面の描画
def draw_game_screen(game_state, animations):
    screen.fill(BLACK)
    
    # スコアとコンボの表示
    score_text = main_font.render(f"Score: {int(game_state.score)}", True, WHITE)
    combo_text = main_font.render(f"Combo: {game_state.combo}", True, WHITE)
    level_text = main_font.render(f"Level: {game_state.level}", True, WHITE)
    
    screen.blit(score_text, (20, 20))
    screen.blit(combo_text, (20, 70))
    screen.blit(level_text, (WIDTH - 150, 20))
    
    # 現在の単語
    word_font = title_font
    
    word_text = word_font.render(game_state.current_word, True, YELLOW)
    word_rect = word_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(word_text, word_rect)
    
    # 制限時間バー
    time_passed = time.time() - game_state.start_time
    time_ratio = max(0, 1 - (time_passed / game_state.time_left))
    bar_width = WIDTH * 0.6 * time_ratio
    pygame.draw.rect(screen, RED, (WIDTH*0.2, HEIGHT//3, WIDTH*0.6, 20))
    pygame.draw.rect(screen, GREEN, (WIDTH*0.2, HEIGHT//3, bar_width, 20))
    
    # 選択肢ボタン
    option_buttons = []
    for i, option in enumerate(game_state.options):
        button = Button(WIDTH//2 - 100, HEIGHT//2 + i*70, 200, 50, option, BLUE)
        button.update()  # アニメーション更新
        button.draw()
        option_buttons.append(button)
    
    # アニメーション効果の描画
    for anim in animations[:]:
        if not anim.update():
            animations.remove(anim)
        else:
            anim.draw()
    
    pygame.display.flip()
    return option_buttons

# ゲームオーバー画面の描画
def draw_game_over_screen(game_state):
    screen.fill(BLACK)
    
    # ゲームオーバーテキスト
    game_over_text = title_font.render("GAME OVER", True, RED)
    score_text = main_font.render(f"Final Score: {int(game_state.score)}", True, WHITE)
    combo_text = main_font.render(f"Max Combo: {game_state.max_combo}", True, WHITE)
    retry_text = "RETRY"
    quit_text = "QUIT"
    
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(game_over_text, game_over_rect)
    
    # 最終スコア
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(score_text, score_rect)
    
    # 最大コンボ
    combo_rect = combo_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(combo_text, combo_rect)
    
    # リトライボタン
    retry_button = Button(WIDTH//2 - 100, HEIGHT*3//4 - 60, 200, 50, retry_text, GREEN)
    retry_button.update()
    retry_button.draw()
    
    # 終了ボタン
    quit_button = Button(WIDTH//2 - 100, HEIGHT*3//4, 200, 50, quit_text, RED)
    quit_button.update()
    quit_button.draw()
    
    pygame.display.flip()
    return retry_button, quit_button

# メインゲームループ
def main():
    clock = pygame.time.Clock()
    game_state = GameState()
    running = True
    animations = []
    
    # BGMを再生
    sound_manager.play_bgm("title")
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # タイトル画面
        if not game_state.game_active and not game_state.game_over:
            start_button = draw_title_screen()
            start_button.check_hover(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.check_click(mouse_pos):
                        sound_manager.play_sound("click")
                        sound_manager.play_bgm("gameplay")
                        game_state.game_active = True
                        game_state.new_word()
        
        # ゲームオーバー画面
        elif game_state.game_over:
            retry_button, quit_button = draw_game_over_screen(game_state)
            retry_button.check_hover(mouse_pos)
            quit_button.check_hover(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.check_click(mouse_pos):
                        sound_manager.play_sound("click")
                        sound_manager.play_bgm("gameplay")
                        # ゲームをリセット
                        game_state = GameState()
                        game_state.game_active = True
                        game_state.new_word()
                        animations = []
                    elif quit_button.check_click(mouse_pos):
                        sound_manager.play_sound("click")
                        running = False
        
        # ゲームプレイ画面
        else:
            option_buttons = draw_game_screen(game_state, animations)
            
            # ボタンのホバー状態を更新
            for button in option_buttons:
                button.check_hover(mouse_pos)
            
            # 時間切れチェック
            time_passed = time.time() - game_state.start_time
            if time_passed >= game_state.time_left:
                sound_manager.play_sound("wrong")
                sound_manager.play_bgm("game_over")
                game_state.game_over = True
                continue
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(option_buttons):
                        if button.check_click(mouse_pos):
                            if game_state.check_answer(i):
                                sound_manager.play_sound("correct")
                                # レベルアップ時に効果音を再生
                                if game_state.words_cleared % 5 == 0:
                                    sound_manager.play_sound("level_up")
                                
                                # 正解の場合、アニメーション効果を追加
                                text = "Correct!"
                                animations.append(
                                    AnimationEffect(
                                        button.rect.centerx, 
                                        button.rect.centery, 
                                        text, 
                                        GREEN, 
                                        48, 
                                        1.0
                                    )
                                )
                                # 次の単語へ
                                game_state.new_word()
                            else:
                                sound_manager.play_sound("wrong")
                                sound_manager.play_bgm("game_over")
                                
                                # 不正解の場合、ゲームオーバー
                                text = "Wrong!"
                                animations.append(
                                    AnimationEffect(
                                        button.rect.centerx, 
                                        button.rect.centery, 
                                        text, 
                                        RED, 
                                        48, 
                                        1.0
                                    )
                                )
                                game_state.game_over = True
        
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
