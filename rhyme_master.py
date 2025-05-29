import pygame
import sys
import random
import time

# Pygameの初期化
pygame.init()
pygame.mixer.init()  # サウンド用の初期化

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhyme Master")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# フォント設定
title_font = pygame.font.SysFont(None, 72)
main_font = pygame.font.SysFont(None, 48)
button_font = pygame.font.SysFont(None, 36)

# 韻を踏む単語のペアのリスト（簡易版）
rhyme_pairs = [
    {"word": "cat", "rhymes": ["hat", "bat", "rat"], "non_rhymes": ["dog", "fish", "bird"]},
    {"word": "light", "rhymes": ["night", "sight", "fight"], "non_rhymes": ["dark", "day", "sun"]},
    {"word": "game", "rhymes": ["fame", "name", "same"], "non_rhymes": ["play", "fun", "joy"]},
    {"word": "cool", "rhymes": ["pool", "rule", "fool"], "non_rhymes": ["hot", "warm", "heat"]},
    {"word": "beat", "rhymes": ["feet", "heat", "seat"], "non_rhymes": ["rhythm", "sound", "noise"]},
    {"word": "flow", "rhymes": ["go", "show", "know"], "non_rhymes": ["stop", "halt", "end"]},
    {"word": "rhyme", "rhymes": ["time", "climb", "dime"], "non_rhymes": ["verse", "word", "line"]},
    {"word": "star", "rhymes": ["far", "car", "bar"], "non_rhymes": ["sky", "night", "space"]},
    {"word": "high", "rhymes": ["sky", "fly", "try"], "non_rhymes": ["low", "down", "bottom"]},
    {"word": "dream", "rhymes": ["team", "stream", "beam"], "non_rhymes": ["sleep", "night", "rest"]}
]

# ゲーム状態
class GameState:
    def __init__(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.current_word = None
        self.options = []
        self.correct_option = None
        self.time_left = 5.0  # 制限時間（秒）
        self.start_time = 0
        self.level = 1
        self.words_cleared = 0
        self.game_active = False
        self.game_over = False
        
    def new_word(self):
        # ランダムに単語ペアを選択
        pair = random.choice(rhyme_pairs)
        self.current_word = pair["word"]
        
        # 選択肢を作成（韻を踏む単語1つと踏まない単語2つ）
        rhyme_word = random.choice(pair["rhymes"])
        non_rhymes = random.sample(pair["non_rhymes"], 2)
        
        self.options = [rhyme_word] + non_rhymes
        random.shuffle(self.options)  # 選択肢をシャッフル
        
        self.correct_option = self.options.index(rhyme_word)
        self.start_time = time.time()
        self.time_left = max(5.0 - (self.level * 0.5), 2.0)  # レベルに応じて制限時間を短くする
        
    def check_answer(self, selected_index):
        if selected_index == self.correct_option:
            self.score += 100 * (1 + self.combo * 0.1)  # コンボボーナス
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

# ボタンクラス
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        self.is_hovered = False
        
    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # 枠線
        
        text_surf = button_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
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
    title_text = title_font.render("RHYME MASTER", True, YELLOW)
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
def draw_game_screen(game_state):
    screen.fill(BLACK)
    
    # スコアとコンボの表示
    score_text = main_font.render(f"Score: {int(game_state.score)}", True, WHITE)
    screen.blit(score_text, (20, 20))
    
    combo_text = main_font.render(f"Combo: {game_state.combo}", True, WHITE)
    screen.blit(combo_text, (20, 70))
    
    level_text = main_font.render(f"Level: {game_state.level}", True, WHITE)
    screen.blit(level_text, (WIDTH - 150, 20))
    
    # 現在の単語
    word_text = title_font.render(game_state.current_word, True, YELLOW)
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
        button.draw()
        option_buttons.append(button)
    
    pygame.display.flip()
    return option_buttons

# ゲームオーバー画面の描画
def draw_game_over_screen(game_state):
    screen.fill(BLACK)
    
    # ゲームオーバーテキスト
    game_over_text = title_font.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(game_over_text, game_over_rect)
    
    # 最終スコア
    score_text = main_font.render(f"Final Score: {int(game_state.score)}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(score_text, score_rect)
    
    # 最大コンボ
    combo_text = main_font.render(f"Max Combo: {game_state.max_combo}", True, WHITE)
    combo_rect = combo_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(combo_text, combo_rect)
    
    # リトライボタン
    retry_button = Button(WIDTH//2 - 100, HEIGHT*3//4 - 60, 200, 50, "RETRY", GREEN)
    retry_button.draw()
    
    # 終了ボタン
    quit_button = Button(WIDTH//2 - 100, HEIGHT*3//4, 200, 50, "QUIT", RED)
    quit_button.draw()
    
    pygame.display.flip()
    return retry_button, quit_button

# メインゲームループ
def main():
    clock = pygame.time.Clock()
    game_state = GameState()
    running = True
    
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
                        # ゲームをリセット
                        game_state = GameState()
                        game_state.game_active = True
                        game_state.new_word()
                    elif quit_button.check_click(mouse_pos):
                        running = False
        
        # ゲームプレイ画面
        else:
            option_buttons = draw_game_screen(game_state)
            
            # ボタンのホバー状態を更新
            for button in option_buttons:
                button.check_hover(mouse_pos)
            
            # 時間切れチェック
            time_passed = time.time() - game_state.start_time
            if time_passed >= game_state.time_left:
                game_state.game_over = True
                continue
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(option_buttons):
                        if button.check_click(mouse_pos):
                            if game_state.check_answer(i):
                                # 正解の場合、次の単語へ
                                game_state.new_word()
                            else:
                                # 不正解の場合、ゲームオーバー
                                game_state.game_over = True
        
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
