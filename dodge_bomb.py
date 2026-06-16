import time
import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル(横方向判定結果,縦方向判定結果)
    True：画面内/False：画面外
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向判定
        tate = False
    return yoko, tate

#演習１
def gameover(screen: pg.Surface) -> None:
    black_img = pg.Surface((WIDTH, HEIGHT)) #演習1-1
    black_img.fill((0, 0, 0))
    black_img.set_alpha(200)#演習1-2透明度
    #演習1-3　白文字GameOver
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH//2, HEIGHT//2
    black_img.blit(txt, txt_rct)
    #演習1-4　こうかとん画像
    kk1_img = pg.image.load("fig/4.png") 
    # 左側のこうかとん（文字の中心から左に200ピクセル、縦は中央）
    kk_left_rct = kk1_img.get_rect()
    kk_left_rct.center = (WIDTH // 2 - 200, HEIGHT // 2)
    black_img.blit(kk1_img, kk_left_rct)
    
    # 右側のこうかとん（文字の中心から右に200ピクセル、縦は中央）
    kk_right_rct = kk1_img.get_rect()
    kk_right_rct.center = (WIDTH // 2 + 200, HEIGHT // 2)
    black_img.blit(kk1_img, kk_right_rct)

    screen.blit(black_img, (0,0)) #演習1-5画面表示
    #演習1-6
    pg.display.update()
    time.sleep(5)

#演習2
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0)) #黒を透明化
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1,11)] #加速度のリスト
    return bb_imgs, bb_accs

#演習3
def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    kk_img = pg.image.load("fig/3.png")
    
    # 左右反転させた右向きの画像（右側の方向で使い回すと綺麗になります）
    kk1_img = pg.transform.flip(kk_img, True, False)
    
    kk_dict = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 0.9), #静止（左向き）
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 0.9), #左
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 0.9), #左上
        (0, -5): pg.transform.rotozoom(kk_img, -90, 0.9), #上 (左から90度時計回り=-90)
        (+5, -5): pg.transform.rotozoom(kk1_img, 45, 0.9), #右上
        (+5, 0): pg.transform.rotozoom(kk1_img, 0, 0.9), #右
        (+5, +5): pg.transform.rotozoom(kk1_img, -45, 0.9), #右下
        (0, +5): pg.transform.rotozoom(kk1_img, -90, 0.9), #下
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 0.9), #左下
    }
    return kk_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")  
    #こうかとん初期化 
    kk_imgs = get_kk_imgs() #演習3にて追加
    kk_img = kk_imgs[(0, 0)] #演習3にて変更
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    #演習２　リストを取得
    bb_imgs, bb_accs = init_bb_imgs()

    #爆弾の初期化
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #半径10の赤い円の描画
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect() #爆弾rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) #横・縦初期座標
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): #こうかとんRectと爆弾Rectが重なったら 
            print("ゲームオーバー")
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向
                sum_mv[1] += mv[1] #縦方向
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #動きをなかったことにする
        #演習３　合計移動量に従ってこうかとんの画像を切り替える
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)

        #演習2の後半
        idx = min(tmr // 500, 9)#時間に応じて爆弾の大きさと速度（加速度）を切り替える
        bb_img = bb_imgs[idx] #現在の段階の爆弾画像を取得
        bb_rct.width = bb_img.get_rect().width #幅更新
        bb_rct.height = bb_img.get_rect().height #高さ更新
        #元の速度に加速度を掛け算して現在の速度（avx, avy）を計算
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
