# plasmid_sequence_checker

### 使用目的:作成したプラスミドの配列チェック 
### 使用法 
1. シーケンス解析した結果のfastaファイル(幾つでも可)をドラッグ&ドロップによりアップロード<br>

2. プラスミドの配列ファイル(fasta or gcc)をアップロード **※これは1 ファイルのみ**<br>

3. パラメーターの設定<br>
   シーケンスリードの5',3'の切り出しをしてNが含まれないようにする。<br>
   シーケンスリードの向きを設定(デフォルトはforward,Reverseを見たい時はReverse_modeをonにする)<br>
   
4. 実行ボタンをクリックするとファイルごとにタブが作成されそこにアラインメント結果が表示される<br>

   <img src="/sample_sequence/result_read2.png" width="50%"><br>
   
   <span style="color: red">※赤字部分が変異部分(-は欠失)</span>
   <span style="color: red;">これは赤いテキストです。</span>
   

アプリ公開しています。<br>
[リンク](https://plasmidsequencechecker-ez7wagcpayygvcwkpeqqev.streamlit.app/)


