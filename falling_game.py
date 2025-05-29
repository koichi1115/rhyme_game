import pygame
import sys
import random
import time
import os
from rhyme_data import english_rhyme_pairs, famous_lyrics
from advanced_rhymes import multi_word_rhymes, long_word_rhymes
from sound_manager import SoundManager
from falling_word import FallingWord

# Pygameの初期化
pygame.init()
pygame.mixer.init()  # サウンド用の初期化

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dr.sibitt")

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
    word_font = pygame.font.SysFont("Arial", 28)
except:
    title_font = pygame.font.Font(None, 72)
    main_font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 36)
    word_font = pygame.font.Font(None, 28)

# サウンドマネージャーの初期化
sound_manager = SoundManager()

# ゲーム状態
class GameState:
    def __init__(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.current_word = None
        self.current_pair = None
        self.falling_words = []
        self.time_left = 60.0  # ゲーム時間（秒）
        self.start_time = 0
        self.level = 1
        self.words_cleared = 0
        self.game_active = False
        self.game_over = False
        self.danger_line_y = HEIGHT - 100  # 危険ライン
        self.spawn_timer = 0
        self.spawn_interval = 2.0  # 単語生成間隔（秒）
        self.last_update_time = 0
        self.word_change_counter = 0  # お題の単語を変更するためのカウンター
        self.word_change_threshold = 5  # この数だけ単語を消したらお題が変わる
        self.difficulty_mode = "normal"  # 難易度モード: "normal", "multi", "long", "lyric"
        self.current_lyric = None  # 現在のリリック
        
    def new_word(self):
        # 難易度に応じたデータセットを選択
        if self.combo >= 20:
            # コンボが20以上なら著名なリリックを使用
            self.difficulty_mode = "lyric"
            self.current_lyric = random.choice(famous_lyrics)
            self.current_word = self.current_lyric["line"]
            self.current_pair = {
                "word": self.current_word,
                "rhymes": [{"word": "APPLAUSE", "type": "perfect", "points": 300}],
                "non_rhymes": ["WRONG", "INCORRECT", "MISS"]
            }
        elif self.combo >= 15:
            # コンボが15以上なら長い単語を使用
            self.difficulty_mode = "long"
            self.current_pair = random.choice(long_word_rhymes)
            self.current_word = self.current_pair["word"]
        elif self.combo >= 10:
            # コンボが10以上なら複数単語を使用
            self.difficulty_mode = "multi"
            self.current_pair = random.choice(multi_word_rhymes)
            self.current_word = self.current_pair["word"]
        else:
            # 通常の単語
            self.difficulty_mode = "normal"
            self.current_pair = random.choice(english_rhyme_pairs)
            self.current_word = self.current_pair["word"]
        
    def spawn_falling_word(self):
        """新しい落下単語を生成"""
        if not self.current_pair:
            return
            
        # 正解の単語を生成する確率
        correct_chance = 0.4
        
        if self.difficulty_mode == "lyric" and random.random() < 0.2:
            # リリックモードでは「APPLAUSE」ボタンを生成
            word = "APPLAUSE"
            is_correct = True
            color = YELLOW  # 特別な色
        elif random.random() < correct_chance:
            # 正解の単語を選択
            rhyme_words = [rhyme["word"] for rhyme in self.current_pair["rhymes"]]
            word = random.choice(rhyme_words)
            is_correct = True
            color = WHITE  # 色を白に統一
        else:
            # 不正解の単語を選択
            non_rhymes = self.current_pair["non_rhymes"]
            word = random.choice(non_rhymes)
            is_correct = False
            color = WHITE  # 色を白に統一
            
        # 画面内のランダムな位置に生成
        x = random.randint(50, WIDTH - 150)
        
        # 速度はレベルに応じて調整
        speed = 1.0 + (self.level * 0.1)
        
        # 単語の幅を計算
        word_width = len(word) * 15 + 20
        
        # 落下単語を生成
        falling_word = FallingWord(word, x, word_width, is_correct, speed, color)
        self.falling_words.append(falling_word)
        
    def update(self, dt):
        """ゲーム状態を更新"""
        current_time = time.time()
        
        # 単語生成タイマー更新
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_falling_word()
            
        # 落下単語の更新
        for word in self.falling_words[:]:
            if not word.update(dt):
                self.falling_words.remove(word)
                
            # 危険ラインを超えた正解単語があればゲームオーバー
            if word.is_correct and word.is_below_line(self.danger_line_y) and not word.clicked:
                self.game_over = True
                sound_manager.play_sound("wrong")
                sound_manager.play_bgm("game_over")
                
        # 残り時間の更新
        elapsed = current_time - self.start_time
        if elapsed >= self.time_left:
            self.game_over = True
            sound_manager.play_sound("game_over")
            sound_manager.play_bgm("game_over")
            
        # レベルアップ条件
        if self.words_cleared >= self.level * 5:
            self.level += 1
            sound_manager.play_sound("level_up")
            # レベルアップ時に単語生成間隔を短くする
            self.spawn_interval = max(0.5, self.spawn_interval - 0.2)
            
    def check_word_click(self, pos):
        """単語クリック判定"""
        for word in self.falling_words:
            if word.check_click(pos):
                word.explode()
                
                if word.is_correct:
                    # 正解の場合
                    
                    # リリックモードで「APPLAUSE」をクリックした場合は特別ボーナス
                    if self.difficulty_mode == "lyric" and word.word == "APPLAUSE":
                        self.score += 500  # 特別ボーナス
                    else:
                        # 通常の得点計算
                        points = 100
                        
                        # 難易度に応じたボーナス
                        if self.difficulty_mode == "multi":
                            points = 150
                        elif self.difficulty_mode == "long":
                            points = 200
                        elif self.difficulty_mode == "lyric":
                            points = 300
                            
                        self.score += points * (1 + self.combo * 0.1)
                    
                    self.combo += 1
                    self.max_combo = max(self.max_combo, self.combo)
                    self.words_cleared += 1
                    
                    # 単語変更カウンターを更新
                    self.word_change_counter += 1
                    if self.word_change_counter >= self.word_change_threshold:
                        self.word_change_counter = 0
                        self.new_word()  # お題の単語を変更
                    
                    sound_manager.play_sound("correct")
                    return True
                else:
                    # 不正解の場合
                    self.combo = 0
                    sound_manager.play_sound("wrong")
                    return False
        return None

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
            return False
        
        # アニメーション効果（上に浮かび上がりながら消える）
        progress = elapsed / self.duration
        self.y -= 1
        alpha = 255 * (1 - progress)
        
        return True
        
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
    subtitle_text = main_font.render("Falling Rhymes Edition", True, WHITE)
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 60))
    screen.blit(subtitle_text, subtitle_rect)
    
    # スタートボタン
    start_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "START", GREEN)
    start_button.draw()
    
    # 説明
    instruction_text = button_font.render("Click on words that rhyme with the given word", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT*3//4))
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()
    return start_button

# ゲーム画面の描画
def draw_game_screen(game_state, animations, dt):
    screen.fill(BLACK)
    
    # スコアとコンボの表示
    score_text = main_font.render(f"Score: {int(game_state.score)}", True, WHITE)
    combo_text = main_font.render(f"Combo: {game_state.combo}", True, WHITE)
    level_text = main_font.render(f"Level: {game_state.level}", True, WHITE)
    
    screen.blit(score_text, (20, 20))
    screen.blit(combo_text, (20, 70))
    screen.blit(level_text, (WIDTH - 150, 20))
    
    # 残り時間の表示
    elapsed = time.time() - game_state.start_time
    time_left = max(0, game_state.time_left - elapsed)
    time_text = main_font.render(f"Time: {int(time_left)}", True, WHITE)
    screen.blit(time_text, (WIDTH - 150, 70))
    
    # 現在の単語（お題）
    if game_state.difficulty_mode == "lyric":
        # リリックモードの場合はアーティスト名と曲名も表示
        word_text = main_font.render(game_state.current_word, True, YELLOW)
        word_rect = word_text.get_rect(center=(WIDTH//2, 30))
        screen.blit(word_text, word_rect)
        
        artist_text = button_font.render(f"{game_state.current_lyric['artist']} - {game_state.current_lyric['song']}", True, CYAN)
        artist_rect = artist_text.get_rect(center=(WIDTH//2, 70))
        screen.blit(artist_text, artist_rect)
    else:
        # 通常モード
        word_text = title_font.render(game_state.current_word, True, YELLOW)
        word_rect = word_text.get_rect(center=(WIDTH//2, 50))
        screen.blit(word_text, word_rect)
    
    # 難易度モードの表示
    mode_colors = {
        "normal": WHITE,
        "multi": GREEN,
        "long": ORANGE,
        "lyric": PURPLE
    }
    mode_text = button_font.render(f"Mode: {game_state.difficulty_mode.upper()}", True, mode_colors[game_state.difficulty_mode])
    screen.blit(mode_text, (WIDTH//2 - 50, 100))
    
    # 危険ラインの描画
    pygame.draw.line(screen, RED, (0, game_state.danger_line_y), (WIDTH, game_state.danger_line_y), 3)
    
    # 落下単語の描画
    for word in game_state.falling_words:
        word.draw(screen, word_font)
    
    # アニメーション効果の描画
    for anim in animations[:]:
        if not anim.update():
            animations.remove(anim)
        else:
            anim.draw()
    
    pygame.display.flip()

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
    
    last_time = time.time()
    
    while running:
        # デルタタイム計算（フレームレート非依存の動き）
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
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
                        game_state.start_time = time.time()
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
                        game_state.start_time = time.time()
                        game_state.new_word()
                        animations = []
                    elif quit_button.check_click(mouse_pos):
                        sound_manager.play_sound("click")
                        running = False
        
        # ゲームプレイ画面
        else:
            # ゲーム状態の更新
            game_state.update(dt)
            
            # 画面描画
            draw_game_screen(game_state, animations, dt)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    result = game_state.check_word_click(event.pos)
                    if result is True:
                        # 正解の場合、アニメーション効果を追加
                        animations.append(
                            AnimationEffect(
                                event.pos[0], 
                                event.pos[1], 
                                "Correct!", 
                                GREEN, 
                                48, 
                                1.0
                            )
                        )
                    elif result is False:
                        # 不正解の場合、アニメーション効果を追加
                        animations.append(
                            AnimationEffect(
                                event.pos[0], 
                                event.pos[1], 
                                "Wrong!", 
                                RED, 
                                48, 
                                1.0
                            )
                        )
        
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
