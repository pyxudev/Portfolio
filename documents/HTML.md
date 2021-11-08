# HTML記述標準

**スタイルが違う文字列**
例：
\<span class="style_1">一行目\</span>
\<span class="style_2">二行目\</span>

NG例：
\<span class="style_1">一行目\</span>
二行目

---
**改行**
必ずcssを使って指定する(pタグのreturnというclassに固定で改行するように設定してます)
例：
一行目
\<p class="return">\</p>
二行目

NG例:
１．一行目\<br>二行目
２．一行目
二行目

---
**空白**
例：
\<div style="display: block; margin-bottom: XXpx;">
内容
\</div>

NG例:
\<br>
\<br>

---
**遷移先、画像等のリンク**
絶対参照を使う
例：
\<img src="https://OOOO/wp-content/uploads/XXX.png">
\<a href="https://OOOO/XXX/"></a>

NG例:
\<img src="../../../wp-content/uploads/XXX.png">
\<a href="./XXX/"></a>

---
**文字と画像**
例：
１．文字文字文字
　　 ーーーー   
　　|　画像　|
　　 ーーーー  
=>
\<span>文字文字文字文字字文字文字文字\</span>
\<p class="return">\</p>
\<img src="https://OOOO/wp-content/uploads/XXX.png">

２．
文字 ーーーー   
文字|　画像　|
文字 ーーーー  
=>
\<div class="flex">
    \<p>文字文字文字文字字文字文字文字\</p>
    \<p>\<img src="https://OOOO/wp-content/uploads/XXX.png">\</p>
\</div>
\<style>
.flex{
&emsp;&emsp;display: flex;
&emsp;&emsp;justify-content: space-between;
}
.flex > p{
&emsp;&emsp;width: 49%;
}
\</style>

NG例：
文字文字文字文字字文字文字文字
\<img src="https://OOOO/wp-content/uploads/XXX.png">

こうなります=>
文字文字文字
&nbsp;ーーーー   
|　画像　|
&nbsp;ーーーー  
文字文字文字

---
2021/09/10 Xu
