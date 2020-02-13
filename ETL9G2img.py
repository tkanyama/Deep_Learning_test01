# ETL1Cのファイルを読み込む
import struct
from PIL import Image, ImageEnhance
import glob, os
from jiscode import jiscode

# 出力ディレクトリ
home = os.path.expanduser('~') + '/ETL/ETL9G'
outdir = home + "/png-etl9g/"
if not os.path.exists(outdir): os.mkdir(outdir)
jis1 = jiscode()
# ETL1ディレクトリ以下のファイルを処理する --- (*1)
files = glob.glob(home +"/ETL9G/*")
i=0
for fname in files:
    if fname == home + "/ETL9G/ETL9INFO": continue # 情報ファイルは飛ばす
    print(fname)
    # ETL1のデータファイルを開く --- (*2)
    f = open(fname, 'rb')
    f.seek(0)
    # i = 0
    while True:
        # メタデータ＋画像データの組を一つずつ読む --- (*3)
        s = f.read(8199)
        if not s: break
        # バイナリデータなのでPythonが理解できるように抽出 --- (*4)
        # r = struct.unpack('>H2sH6BI4H4B4x2016s4x', s)
        r = struct.unpack('>2H8sI4B4H2B34x8128s7x', s)
        if r[1]>0:
            code_ascii = r[1]
            code_jis = r[1]
            code_uni = jis1.jis2uni(code_jis)
            # 画像データとして取り出す --- (*5)
            iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
            iP = iF.convert('L')
            # 画像を鮮明にして保存
            dir = outdir + "/" + "{0:02X}({1:})".format(code_jis, chr(code_uni))
            if not os.path.exists(dir): os.mkdir(dir)
            fn = "{0:02X}-{1:02X}{2:04X}.png".format(code_jis, r[0], i)
            fullpath = dir + "/" + fn
            #if os.path.exists(fullpath): continue
            enhancer = ImageEnhance.Brightness(iP)
            iE = enhancer.enhance(16)
            iE.save(fullpath, 'PNG')
            i += 1

print("ok")
