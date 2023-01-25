# モジュールのインポート
import pygame # pygameモジュール
import random # ランダムモジュール
import copy # コピーモジュール

# ============ 定数 ============
WIDTH = 500 # ウィンドウの横の長さ
HEIGHT = 650 # ウィンドウの縦の長さ
FPS = 10 # フレームレート
# ============ 変数 ============
tubes_num = 14   # 試験管の数
tubes_list = [] # 試験管ごとの中身リスト
origin_tube_list = None # ゲーム開始時の試験管ごとの中身リスト(リスタート用）

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
            
# ゲーム情報の初期化処理
def init_game_info():
    global tubes_list, origin_tube_list
    
    divide_list = [] # ボールを振り分ける用のリスト
    
    for i in range(tubes_num):
        # 試験管の数だけ空のリストを作成
        tubes_list.append([]) 
        # ボールの種類 × 4回分を振り分けリストに追加
        # ※2つの試験管は空にするので、ボールの種類数 = 総試験管数 - 2）
        if i < tubes_num - 2:
            for _ in range(4):
                divide_list.append(i)

    # 試験管にボールをランダムに振り分ける
    for i in range(tubes_num - 2):
        for _ in range(4):
            ball = random.choice(divide_list) # ランダムに選択
            tubes_list[i].append(ball) # ボールを試験管に追加
            divide_list.remove(ball) # 振り分けリストから取り除く
    
    # 初期状態を保存するためにコピーを作成
    origin_tube_list = copy.deepcopy(tubes_list)

# メイン関数
def main():
    
    init_game_info() # ゲーム初期化処理
    print(tubes_list)
    print(origin_tube_list)
    
    
    while True:
        surface.fill("black")  # 背景を黒にする

        check_event() # イベントチェック処理（終了、マウス入力）を実行

        pygame.display.flip() # 画面更新処理
        clock.tick(FPS) # フレームレートの設定

# ファイルを実行した時に、メイン関数を呼び出す
if __name__ == '__main__':
    main()