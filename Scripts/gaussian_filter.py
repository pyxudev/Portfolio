# ガウシアンフィルタは線形フィルタなので、行列の畳み込み演算で書けるが、
# 今回は非線形フィルタであるバイラテラルフィルタに拡張しやすいように、
# 画素ごとに処理をする方法で書いている。
# （局所領域内の加重平均は、空間距離による重みと画素値の差による重みと
# 局所領域の行列演算でもっと簡単に書ける。早くできた人は試してみよう。）


# モジュールのインポート
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math


# 画像の読み込み
file_name = "Lena"
n_gauss = 10
img_in = cv2.imread(f"{file_name}_gauss{n_gauss}.png", cv2.IMREAD_GRAYSCALE)
if img_in is None:
    raise Exception("MyError: 画像を読み込めませんでした。")


# 型変換
img_in = img_in.astype("float64")


# パラメータ
r = 3 # 窓半径


# パディング処理
img_in_L = img_in.copy()
img_in_L=np.vstack([img_in_L[1+r:1:-1,::], img_in_L])
img_in_L=np.vstack([img_in_L, img_in_L[-1:-1-r:-1,::]])
img_in_L=np.hstack([img_in_L[::,1+r:1:-1], img_in_L])
img_in_L=np.hstack([img_in_L, img_in_L[::,-1:-1-r:-1]])
print(img_in_L.shape)


# ガウシアンフィルタ処理
sigma = (2*r+1)/6 # 内部パラメータ：標準偏差

img_out = np.zeros_like(img_in)
ii = 0
for i in range(r,img_in_L.shape[0]-r):
    jj = 0
    for j in range(r,img_in_L.shape[1]-r):
        for m in range(-r,r+1):
            for n in range(-r,r+1): 
                h1 = math.exp(-(m**2+n**2)/(2*sigma**2))
                h2 = 2*math.pi*sigma**2
                h = h1/h2
                img_out[ii,jj] += h*img_in_L[i+m,j+n]
                
                # カーネルの表示
                if ii==0 and jj ==0:
                    print(round(h,6),end=" ")
                    if n == r: print("");
        jj += 1
    ii +=1


# 画像の表示
plt.gray()
plt.subplot(1,2,1)
plt.imshow(img_in, vmin=0, vmax=255)
plt.subplot(1,2,2)
plt.imshow(img_out, vmin=0, vmax=255)
plt.show()


# 画像の保存
cv2.imwrite(f"{file_name}_gauss{n_gauss}_gf.png", img_out)


# MSE評価
def my_MSE(img_org, img_trg):
    """自作MSE評価関数"""
    return ((img_org.astype("float64")-img_trg.astype("float64"))**2).mean()

img_org = cv2.imread(f"{file_name}.png", cv2.IMREAD_GRAYSCALE)
if img_org is None:
    raise Exception("MyError: 画像を読み込めませんでした。")

img_out = cv2.imread(f"{file_name}_gauss{n_gauss}_gf.png", cv2.IMREAD_GRAYSCALE)
if img_out is None:
    raise Exception("MyError: 画像を読み込めませんでした。")

print("img_in:MSE", my_MSE(img_org[0+r:img_org.shape[0]-r, 0+r:img_org.shape[1]-r], img_in[0+r:img_in.shape[0]-r, 0+r:img_in.shape[1]-r]))
print("img_out:MSE", my_MSE(img_org[0+r:img_org.shape[0]-r, 0+r:img_org.shape[1]-r], img_out[0+r:img_out.shape[0]-r, 0+r:img_out.shape[1]-r]))
# 窓半径3だと平滑化しすぎて、ノイズありの画像よりMSEが悪くなる。ガウシアンフィルタは窓半径1か2ぐらいが適している。
