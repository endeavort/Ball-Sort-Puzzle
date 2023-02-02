# モジュールのインポート
import pygame  # pygameモジュール
import random  # ランダムモジュール
import copy  # コピーモジュール

# ============ 定数 ============
WIDTH = 500  # ウィンドウの横の長さ
HEIGHT = 650  # ウィンドウの縦の長さ
FPS = 10  # フレームレート
COLOR_LIST = [
    "blue",
    "yellow",
    "red",
    "green",
    "purple",
    "orange",
    "gray",
    "olive",
    "deeppink",
    "brown",
    "aqua",
    "greenyellow",
]  # ボールの色リスト
BACK_BUTTON = pygame.Rect(410, 10, 80, 40)  # BACK（NEXT）ボタンの座標
LEVEL_BUTTON = [
    pygame.Rect(50 + 100 * i, 200 + 110 * j, 80, 80) for j in range(4) for i in range(4)
]  # Levelボタンの座標
SELECT_LEVEL_BUTTON = pygame.Rect(140, 260, 220, 50)  # SELECT LEVELボタンの座標
MENU_BITTON = pygame.Rect(10, 10, 80, 40)  # MENUボタンの座標
RESTART_BUTTON = pygame.Rect(140, 170, 220, 50)  # RESTARTボタンの座標
CLOSE_BUTTON = pygame.Rect(360, 100, 40, 40)  # ×ボタンの座標
START_BUTTON = pygame.Rect(140, 460, 220, 70)  # STARTボタンの座標

# ============ 変数 ============
tubes_num = 14  # 試験管の数
tubes_list = []  # 試験管ごとの中身リスト
origin_tube_list = None  # ゲーム開始時の試験管ごとの中身リスト(リスタート用）
adjust = 0  # 偶奇用調整数字
line = 2  # 1列の試験管の数
tube_x = 250  # 1本ごとの幅
tube_rects = []  # 試験管ごとの四角座標リスト
selected = False  # ボール選択中フラグ
select_tube = None  # 選択中の試験管のナンバー
select_ball = None  # 選択したボール
tubes_history = []  # 試験管ごとの中身のリスト記録（BACKボタン用）
clear_list = []  # 試験管ごとに同じ色が4つあるか確認するフラグのリスト

# フェーズ
phase = 0
# 0:タイトル
# 1:ルール説明1
# 2:ルール説明2
# 3:レベル選択
# 4:ゲーム画面
# 5:メニュー画面
# 6:クリア画面

pygame.init()  # pygameの初期化処理
pygame.display.set_caption("Ball Sort Puzzle")  # 枠上部に表示されるタイトル

surface = pygame.display.set_mode([WIDTH, HEIGHT])  # ゲーム画面の枠
clock = pygame.time.Clock()  # プログラム内の時間管理処理の簡略化
# フォントの設定
# ファイル情報から読み込む:pygame.font.Fontpygame(ファイル名, フォントサイズ)
# ※ 「freesansbold.ttf」はpygameのデフォルトフォントのため、ファイルを用意する必要がない
small_font = pygame.font.Font("freesansbold.ttf", 24)
large_font = pygame.font.Font("freesansbold.ttf", 60)

# イベントチェック処理
def check_event():
    # イベント処理ループ
    for event in pygame.event.get():
        # 終了処理:右上の「×」を押したらpygame終了
        if event.type == pygame.QUIT:
            pygame.quit()
        # クリック処理:クリックしたらその座標で処理を行う
        if event.type == pygame.MOUSEBUTTONDOWN:
            click(event.pos)


# 　クリック処理
def click(pos):
    global selected, select_tube, select_ball, tubes_list, phase, tubes_num, tubes_history
    # タイトル画面
    if phase == 0:
        # マウスの選択座標とスタートの座標が重なったら
        if START_BUTTON.collidepoint(pos):
            phase = 1  # ルール説明画面1へ

    # ルール説明1画面
    elif phase == 1:
        # マウスのクリック時の座標とNEXTボタンの座標が重なったら
        if BACK_BUTTON.collidepoint(pos):
            phase = 2  # ルール説明画面2へ

    # ルール説明2画面
    elif phase == 2:
        # マウスのクリック時の座標とNEXTボタンの座標が重なったら
        if BACK_BUTTON.collidepoint(pos):
            phase = 3  # レベル選択画面へ

    # レベル選択画面
    elif phase == 3:
        # 初期値処理
        reset()
        for i in range(len(LEVEL_BUTTON) - 1):
            # マウスのクリック時の座標とLevelボタンの座標が重なったら
            if LEVEL_BUTTON[i].collidepoint(pos):
                tubes_num = 4 + i  # レベルに応じて試験管の数を設定
                init_game_info()  # ゲーム初期化
                phase = 4  # ゲーム画面へ
                pygame.draw.rect(surface, "black", (0, 0, WIDTH, HEIGHT))  # 残像バグ用
    # ゲーム画面
    elif phase == 4:
        # マウスのクリック時の座標とBACKボタンが重なって、直前の記録があるとき
        # ※ゲーム開始時以外の時
        if BACK_BUTTON.collidepoint(pos) and tubes_history:
            # 1つ前の試験管リストを呼び出し
            tubes_list = tubes_history.pop(-1)
            # 選択中フラグをFalseに
            selected = False
            # 選択中の試験管のナンバーを消す
            select_tube = None
            # 選択中のボールを消す
            select_ball = None

        # マウスのクリック時の座標とMENUボタンの座標が重なったら
        if MENU_BITTON.collidepoint(pos):
            phase = 5  # メニュー画面へ

        # もしボールを選択中の時
        if selected:
            for i in range(len(tube_rects)):
                # マウスのクリック時の座標と試験管が重なって、その中のボールが3つ以下だったら
                if tube_rects[i].collidepoint(pos) and len(tubes_list[i]) != 4:
                    # 同じ試験管に戻す or 空の試験管 or 同じ色のボールの上だったら
                    if (
                        i == select_tube
                        or len(tubes_list[i]) == 0
                        or tubes_list[i][-1] == select_ball
                    ):
                        # 戻す時は直前の記録を取り消し
                        if i == select_tube:
                            tubes_history.pop(-1)
                        # 選択したボールをクリックした試験管の中に入れる
                        tubes_list[i].append(select_ball)
                        # 選択中フラグをFalseに
                        selected = False
                        # 選択中の試験管のナンバーを消す
                        select_tube = None
                        # 選択中のボールを消す
                        select_ball = None
        # 何も選択していない時
        else:
            for i in range(len(tube_rects)):
                # マウスのクリック時の座標と試験管が重なったら
                if tube_rects[i].collidepoint(pos):
                    # 試験管の中にボールがある時 and 同じ色が4つ揃ってなかったら
                    if 0 < len(tubes_list[i]) and not (
                        len(set(tubes_list[i])) == 1 and len(tubes_list[i]) == 4
                    ):
                        # 選択中フラグをTrueに
                        selected = True
                        # 選択中の試験管のナンバーを記録
                        select_tube = i
                        # 現在の試験管リストを記録
                        tubes_history.append(copy.deepcopy(tubes_list))
                        # 一番上のボールを取り出す
                        select_ball = tubes_list[i].pop(-1)
    # メニュー画面
    elif phase == 5:
        # マウスのクリック時の座標とRESTARTボタンの座標が重なったら
        if RESTART_BUTTON.collidepoint(pos):
            # 試験管リストを最初に戻す
            tubes_list = copy.deepcopy(origin_tube_list)
            # 試験管リストを削除
            tubes_history = []
            # プレイ画面へ
            phase = 4
        # マウスのクリック時の座標とSELECT LEVELボタンの座標が重なったら
        elif SELECT_LEVEL_BUTTON.collidepoint(pos):
            # レベル選択画面へ
            phase = 3
        # マウスのクリック時の座標と×ボタンの座標が重なったら
        elif CLOSE_BUTTON.collidepoint(pos):
            # プレイ画面へ
            phase = 4

    # クリア画面
    elif phase == 6:
        # マウスのクリック時の座標とSELECT LEVELボタンの座標が重なったら
        if SELECT_LEVEL_BUTTON.collidepoint(pos):
            phase = 3  # レベル選択画面へ


def start():
    # 背景
    # ボールの描画
    for i in range(13):
        for j in range(14):
            pygame.draw.circle(surface, random.choice(COLOR_LIST), (50 * i, 50 * j), 25)

    # ゲームタイトル
    # 四角の描画
    pygame.draw.rect(surface, "white", (50, 100, 400, 180), 0, 50)
    pygame.draw.rect(surface, "black", (50, 100, 400, 180), 10, 50)
    # 文字の設定
    BALL_text = large_font.render("Ball", True, "black")
    SORT_text = large_font.render("Sort", True, "black")
    PUZZLE_text = large_font.render("Puzzle", True, "black")
    # 文字の描画
    surface.blit(BALL_text, (115, 130))
    surface.blit(SORT_text, (265, 130))
    surface.blit(PUZZLE_text, (150, 200))

    # STARTボタン
    # 四角の描画
    pygame.draw.rect(surface, "white", (130, 450, 240, 90))
    pygame.draw.rect(surface, "red", START_BUTTON)
    # 文字の設定
    START_text = large_font.render("START", True, "white")
    # 文字の描画
    surface.blit(START_text, (150, 470))


# ルール説明処理
def rule():
    # 1ページ目
    if phase == 1:
        # 文字の設定
        rule1text = "Move the ball to line up "
        rule2text = "4 balls of the same color"
        # 画像の設定
        rule_image = pygame.image.load("image/rule1.png")
    # 2ページ目
    elif phase == 2:
        # 文字の設定
        rule1text = "you can only move on empty boxes"
        rule2text = "or over the same color ball"
        # 画像の設定
        rule_image = pygame.image.load("image/rule2.png")

    # 文字の描画
    rule1 = small_font.render(rule1text, True, "white")
    rule2 = small_font.render(rule2text, True, "white")
    surface.blit(rule1, (50, 100))
    surface.blit(rule2, (50, 150))

    # 画像の描画
    surface.blit(rule_image, (0, 250))

    # NEXTボタン
    pygame.draw.rect(surface, "white", BACK_BUTTON, 3)
    back_text = small_font.render("NEXT", True, "white")
    surface.blit(back_text, (415, 20))


# 初期値処理
def reset():
    global tubes_list, tubes_history, tube_rects, select_tube, selected, select_ball, clear_list
    tubes_list = []
    tubes_history = []
    tube_rects = []
    select_tube = None
    selected = False
    select_ball = None
    clear_list = []


# レベル選択画面
def select_level():
    # 文字の設定
    text = small_font.render("Please select a level", True, "white")
    # 文字の描画
    surface.blit(text, (50, 100))
    # LEVELボタンの描画
    for i in range(11):
        pygame.draw.rect(surface, "white", LEVEL_BUTTON[i], 3)
    level = 1
    for i in range(3):
        for j in range(4):
            # レベルごと文字の設定
            level_text = large_font.render(f"{level}", True, "white")
            # レベルごと文字の描画
            if level < 10:
                surface.blit(level_text, (75 + 100 * j, 215 + 110 * i))
            elif level == 12:
                pass
            else:
                surface.blit(level_text, (60 + 100 * j, 215 + 110 * i))
            level += 1


# ゲーム情報の初期化処理
def init_game_info():
    global tubes_list, origin_tube_list, adjust, line, tube_x, tube_rects

    divide_list = []  # ボールを振り分ける用のリスト

    for i in range(tubes_num):
        # 試験管の数だけ空のリストを作成
        tubes_list.append([])
        # 試験管の数だけクリアリスト（初期値はFalse）を作成
        clear_list.append(False)
        # ボールの種類 × 4回分を振り分けリストに追加
        # ※2つの試験管は空にするので、ボールの種類数 = 総試験管数 - 2）
        if i < tubes_num - 2:
            for _ in range(4):
                divide_list.append(i)

    # 試験管にボールをランダムに振り分ける
    for i in range(tubes_num - 2):
        for _ in range(4):
            ball = random.choice(divide_list)  # ランダムに選択
            tubes_list[i].append(ball)  # ボールを試験管に追加
            divide_list.remove(ball)  # 振り分けリストから取り除く

    # 初期状態を保存するためにコピーを作成
    origin_tube_list = copy.deepcopy(tubes_list)

    # 試験管の数が偶数の時
    if tubes_num % 2 == 0:
        adjust = 0
    # 試験管の数が奇数の時
    else:
        adjust = 1

    line = tubes_num // 2 + adjust  # 1列の試験管の数
    tube_x = WIDTH // line  # 1本ごとの幅

    # 1列目
    for i in range(line):
        # 試験管の四角座標(左上のx座標, y座標, 横幅, 縦幅)
        box = pygame.Rect(5 + tube_x * i, 130, 65, 215)
        # 試験管の描画座標をリストに追加
        tube_rects.append(box)
    # 2列目
    for i in range(line - adjust):
        # 試験管の四角座標
        box = pygame.Rect(5 + tube_x * i, 425, 65, 215)
        # 試験管の描画座標をリストに追加
        tube_rects.append(box)

    # 文字の設定
    text = small_font.render("Please select a level", True, "white")
    # 文字の描画
    surface.blit(text, (50, 100))
    # LEVELボタンの描画
    for i in range(11):
        pygame.draw.rect(surface, "white", LEVEL_BUTTON[i], 3)
    level = 1
    for i in range(3):
        for j in range(4):
            # レベルごと文字の設定
            level_text = large_font.render(f"{level}", True, "white")
            # レベルごと文字の描画
            if level < 10:
                surface.blit(level_text, (75 + 100 * j, 215 + 110 * i))
            elif level == 12:
                pass
            else:
                surface.blit(level_text, (60 + 100 * j, 215 + 110 * i))
            level += 1


# ゲーム描画処理
def draw():
    # ボールの描画
    # 1列目
    for i in range(line):
        for j in range(len(tubes_list[i])):
            # 円の描画:pygame.draw.circle(描画する画面, 色,
            #                            (中心点のx座標, y座標), 円の半径, 線の太さ(0だと塗りつぶし))
            pygame.draw.circle(
                surface,
                COLOR_LIST[tubes_list[i][j]],
                (37 + tube_x * i, 315 - (50 * j)),
                25,
            )
    # 2列目
    for i in range(line - adjust):
        for j in range(len(tubes_list[i + line])):
            pygame.draw.circle(
                surface,
                COLOR_LIST[tubes_list[i + line][j]],
                (37 + tube_x * i, 610 - (50 * j)),
                25,
            )
    # 選択中のボールがある場合
    if select_ball != None and select_tube != None:
        # 1列目の時
        if select_tube < line:
            pygame.draw.circle(
                surface, COLOR_LIST[select_ball], (37 + tube_x * select_tube, 90), 25
            )
        # 2列目の時
        else:
            pygame.draw.circle(
                surface,
                COLOR_LIST[select_ball],
                (37 + tube_x * (select_tube - line), 385),
                25,
            )

    # 試験管の描画
    # 四角の描画:pygame.draw.rect(描画する画面, 色, 四角座標, 線の太さ, 角の丸み)
    for i, tube_rect in enumerate(tube_rects):
        pygame.draw.rect(surface, "white", tube_rect, 5, 3)
        # 選択中の時は緑色で囲む
        if i == select_tube:
            pygame.draw.rect(surface, "lime", tube_rect, 3, 5)
        # 全て揃った時は金色で囲む
        if len(set(tubes_list[i])) == 1 and len(tubes_list[i]) == 4:
            pygame.draw.rect(surface, "gold", tube_rect, 5, 5)

    # Backボタン
    # ボタンの描画
    pygame.draw.rect(surface, "white", BACK_BUTTON)
    # 文字の設定：render(描画する文字, 文字の境界をなめらかにするか,　色)
    back_text = small_font.render("BACK", True, "black")
    # 文字の描画：blit(render, 開始座標)
    surface.blit(back_text, (415, 20))

    # MENUボタン
    # ボタンの描画
    pygame.draw.rect(surface, "white", MENU_BITTON)
    # 文字の設定：render(描画する文字, 文字の境界をなめらかにするか,　色)
    menu_text = small_font.render("MENU", True, "black")
    # 文字の描画：blit(render, 開始座標)
    surface.blit(menu_text, (15, 20))


# メニュー処理
def menu():
    # メニュー枠の描画
    pygame.draw.rect(surface, "red", (95, 95, 310, 260))
    pygame.draw.rect(surface, "black", (100, 100, 300, 250))
    # ボタンの描画
    # RESTARTボタン
    restart_text = small_font.render("R E S T A R T", True, "white")
    surface.blit(restart_text, (175, 185))
    pygame.draw.rect(surface, "white", RESTART_BUTTON, 3)
    # SELECT LEVELボタン
    select_level_text = small_font.render("SELECT LEVEL", True, "white")
    surface.blit(select_level_text, (160, 275))
    pygame.draw.rect(surface, "white", SELECT_LEVEL_BUTTON, 3)
    # CLOSEボタン
    pygame.draw.line(surface, "red", (395, 105), (375, 125), 3)
    pygame.draw.line(surface, "red", (375, 105), (395, 125), 3)
    pygame.draw.rect(surface, "black", CLOSE_BUTTON, 1)


# クリア画面
def clear():
    # 最高レベルクリアの時
    if tubes_num == 14:
        # 画像の設定
        img = pygame.image.load("image/complete.png")
        # 画像の描画
        surface.blit(img, (95, 95))
    # 最高レベル以外クリアの時
    else:
        # 画像の設定
        img = pygame.image.load("image/clear.png")
        # 画像の描画
        surface.blit(img, (85, 95))

        # SELECT LEVELボタン
        # ボタンの描画
        pygame.draw.rect(surface, "red", SELECT_LEVEL_BUTTON)
        # 文字の設定
        select_level_text = small_font.render("SELECT LEVEL", True, "white")
        # 文字の描画
        surface.blit(select_level_text, (160, 275))


# メイン関数
def main():
    global phase, clear_list
    while True:
        surface.fill("black")  # 背景を黒にする

        check_event()  # イベントチェック処理（終了、マウス入力）を実行

        # タイトル画面の時
        if phase == 0:
            start()  # タイトル画面処理

        # ルール説明1,2の時
        elif phase == 1 or phase == 2:
            rule()  # ルール説明処理

        # レベル選択画面の時
        elif phase == 3:
            select_level()  # レベル選択画面処理

        # ゲーム画面の時
        elif phase == 4:
            draw()  # 描画処理
            for i, tube in enumerate(tubes_list):
                # セット型にしたときに要素数が1 and 試験管の要素数が4の時
                # ※list → setにすると重複する値は消える
                if len(set(tube)) == 1 and len(tube) == 4:
                    # 試験管のクリアフラグをTrueにする
                    clear_list[i] = True
            # 試験管のクリアフラグのFalse数が2になったらクリア画面へ
            if clear_list.count(False) == 2:
                phase = 6

        # メニュー画面の時
        elif phase == 5:
            draw()  # 描画処理
            menu()  # メニュー画面処理

        # クリア画面の時
        elif phase == 6:
            draw()  # 描画処理
            clear()  # クリア画面処理

        pygame.display.flip()  # 画面更新処理
        clock.tick(FPS)  # フレームレートの設定


# ファイルを実行した時に、メイン関数を呼び出す
if __name__ == "__main__":
    main()
