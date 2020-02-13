import glob
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle, os
from jiscode import jiscode

home = os.path.expanduser('~') + '/ETL/ETL9G'
# 保存先や画像サイズの指定 --- (*1)
out_dir =home + "/png-etl9g" # 画像データがあるディレクトリ
im_size = 25 # 画像サイズ
save_file = home + "/ETL9G.pickle" # 保存先
plt.figure(figsize=(9, 17)) # 出力画像を大きくする
jis1 = jiscode()

files = glob.glob(out_dir +"/*")
kanji = []
for f in files:
    kanji.append(int(os.path.basename(f)[0:4],16))
# カタカナの画像が入っているディレクトリから画像を取得 --- (*2)
# kanji = list(range(177, 220 + 1))
# kanji.append(166) # ヲ
# kanji.append(221) # ン
result = []
k=0
for i, code in enumerate(kanji):
    code_uni = jis1.jis2uni(code)
    img_dir = out_dir + "/" + "{0:02X}({1:})".format(code, chr(code_uni))
    # img_dir = out_dir + "/" + str(code)
    fs = glob.glob(img_dir + "/*")
    print("dir=",  img_dir)
    # 画像を読み込んでグレイスケールに変換しリサイズする --- (*3)
    for j, f in enumerate(fs):
        try:
            img = cv2.imread(f)
            s = img.shape
            if s[0]>0 and s[1]>0:
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img_gray, (im_size, im_size))
                result.append([code, img])
                # Jupyter Notebookで画像を出力
                k += 1
                if k<=50 :
                    plt.subplot(10, 5, k)
                    plt.axis("off")
                    plt.title(str(i))
                    plt.imshow(img, cmap='gray')
        except :
            pass
# ラベルと画像のデータを保存 --- (*4)
pickle.dump(result, open(save_file, "wb"))
plt.show()
print("ok")
