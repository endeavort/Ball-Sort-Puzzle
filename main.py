# モジュールのインポート
import pygame # pygameモジュール
import random # ランダムモジュール
import copy # コピーモジュール

# ============ 定数 ============
WIDTH = 500 # ウィンドウの横の長さ
HEIGHT = 650 # ウィンドウの縦の長さ
FPS = 10 # フレームレート

pygame.init() # pygameの初期化処理
pygame.display.set_caption("Ball Sort Puzzle")  # 枠上部に表示されるタイトル

surface = pygame.display.set_mode([WIDTH ,HEIGHT]) # ゲーム画面の枠
clock = pygame.time.Clock() # プログラム内の時間管理処理の簡略化
# フォントの設定
# ファイル情報から読み込む:pygame.font.Fontpygame(ファイル名, フォントサイズ)
# ※ 「freesansbold.ttf」はpygameのデフォルトフォントのため、ファイルを用意する必要がない
small_font = pygame.font.Font('freesansbold.ttf', 24) 
large_font = pygame.font.Font('freesansbold.ttf', 60) 

# イベントチェック処理
def check_event():
    # イベント処理ループ
    for event in pygame.event.get():
        # 終了処理:右上の「×」を押したらpygame終了
        if event.type == pygame.QUIT: 
            pygame.quit()

# メイン関数
def main():
    while True:
        surface.fill("black")  # 背景を黒にする

        check_event() # イベントチェック処理（終了、マウス入力）を実行

        pygame.display.flip() # 画面更新処理
        clock.tick(FPS) # フレームレートの設定

# ファイルを実行した時に、メイン関数を呼び出す
if __name__ == '__main__':
    main()