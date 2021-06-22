# CNC Mill
## 問題描述
### 資料集簡介
使用Kaggle上的資料集：CNC Mill Tool Wear。此資料集為透過CNC milling machine中提取出來的銑床加工數據。
該資料集中有18個不同實驗之數據資料集(experiment.csv)，每個實驗中包含了特定時段內機器移動的座標軌跡等。除此之外，還有一資料集內容是針對這18個實驗最後狀態的統整 (train.csv)，其中包含：實驗編號、材料（蠟）、進料速度和夾緊壓力、工具狀況（未磨損和磨損的工具）以及該工具是否通過外觀檢查。本資料集可用於：
	1. 刀具磨損之監督式分類 
	2. 夾緊壓力不足所導致需要人工檢驗的情況預測

![](https://i.imgur.com/fbKe68H.png)

圖 1	Modern High Speed CNC Lathe Machine Working

資料來源：https://www.youtube.com/watch?v=jF4F8Zr2YO8&t=25s
 
### 資料集內容

#### train.csv
包含7個欄位，其中前四個欄位為input feature，其餘三個欄位為output。

表 1	train.csv的資料欄位
![](https://i.imgur.com/Tos8aNM.png)


在此問題中我們使用了刀具狀況(Tool Condition)、進料速度(Feed Rate)、夾緊壓力(Clamp Pressure)這三個特徵。

#### experienment_1.csv - experienment_18.csv
每個檔案裡包含48個欄位，紀錄了某段時間內機器移動的軌跡。其中有X、Y、Z、S、M五種軸向的紀錄資料，並包含了運動相關的位置、速度、加速度、負載力大小、驅動器負載電流等資訊。

### 目標問題

目標函數為train.csv中的Tool Condition(刀具狀況)，用以判斷何時須更換銑床上的刀具，進行刀具磨損之監督式分類，分為worn(磨損)與unworn(未磨損)。
 
## 研究方法

### 資料預處理

1. 將各個實驗中的數據取平均，統整至train.csv中
2. 透過相關係數，剔除不必要的特徵(高度正相關的兩個特徵取其一留下)
3. 資料切割(test_size=0.3)， 18筆中有12筆train data、6筆test data

![](https://i.imgur.com/KA9yvox.png)

圖 2	experienment.csv的數據取平均、結合train.csv，做相關測試

![](https://i.imgur.com/WpIOt3l.png)

圖 3	資料清理，剔除不必要的特徵

### 資料分析方法

#### 決策樹 (Decision Tree)
決策樹採用樹形結構，使用層層推理來實現最終的分類，由根節點、內部節、葉節點構成。預測時，在樹的內部節點處用某一屬性值進行判斷，根據判斷結果決定進入哪個分支節點，直到到達葉節點處，得到分類結果。

表 2	決策樹優缺點

![](https://i.imgur.com/ZaiItKf.png)

#### 支援向量機 (SVM)
SVM是一種基於統計學習理論基礎的機器學習模型，針對小樣本、非線性、高維度與局部最小點等問題具有相對的優勢。簡單說就是找到一個決策邊界(decision boundary)讓兩類之間的邊界(margins)最大化，使其可以完美區隔開來。


表 3	支援向量機優缺點

![](https://i.imgur.com/CXeP2po.png)

#### 邏輯斯回歸 (Logistic Regression)

邏輯斯回歸為平滑的曲線，是解決工業規模問題最流行的算法，核心思想是利用現有數據對分類邊界建立回歸方程，以此進行分類。回歸可以理解為最佳擬合，是一種選擇最優分類的算法。

表 4	邏輯斯回歸優缺點

![](https://i.imgur.com/hTC6In9.png)
	
## 分析結果與討論
### 分析結果
#### 決策樹

使用吉尼係數(Gini)作為資訊量的超參數，另外因此資料集數量較少，樹最高(max_depth)設為2以避免Overfitting。

 ![](https://i.imgur.com/6PPh7jX.png)

圖 4	決策樹視覺化結果

表 5	決策樹混淆矩陣

![](https://i.imgur.com/iuWM3cz.png)

#### 支援向量機
其中SVM的超參數包括：decision_function_shape、kernel、C、gamma等，在手動嘗試了不同的Kernel function後，選擇了使用預設的kernel RBF。

表 6	SVM中不同Kernel的Accuracy表現

![](https://i.imgur.com/HyttglY.png)

表 7	SVM混淆矩陣

![](https://i.imgur.com/pMUGBUK.png)


#### 邏輯斯回歸

表 8	邏輯斯回歸混淆矩陣

![](https://i.imgur.com/AUkRguP.png)


#### 三種算法各衡量指標比較

表 9	三種算法在準確率、精確率、召回率與F1-socre的比較

![](https://i.imgur.com/wB4lg7B.png)

就準確度(Accuracy)而言，以SVM的結果最好。召回率(Recall)是實際上有磨損的被預測出有磨損的比例，精確率(Precision)則是預測為有磨損實際上有磨損的比例。但是在刀具磨損的分類問題中，已經被磨損的刀具若是仍被判定為未磨損，可能導致銑床機器受損，而提早停止使用「可能耗損的」刀具也會導致刀片的浪費 (陳健立，2012) 。因此在這個問題中，我們更應該參考召回率(Recall)的結果，此時可以發現也是SVM比較符合期待。
但若是同樣看重召回率與精確率，可以使用F1-score進行衡量。此時則可以發現，SVM的表現最好。我們未來或許能透過調整兩個種算法的超參數以達該算法的最佳預測結果，或者是增加資料量讓預測結果更具參考價值。


## 參考文獻

1. 陳健立，2012。以電腦視覺畫面鑑定車削刀片等級之技術研究。朝陽科技大學工業工程與管理系碩士論文。
2. 知乎，2018。常用機器學習常用算法優點及缺點總結。取自
https://zhuanlan.zhihu.com/p/36928215。搜尋日期：2021年6月3日。
3. Chao, CM., Yu, YW., Cheng, BW. et al. 2014 Construction the Model on the Breast Cancer Survival Analysis Use Support Vector Machine, Logistic Regression and Decision Tree. Journal of Medical Systems, 38, 106.
4. Daniel, F.H., & Bernd M. 2019. Tool wear monitoring of a retrofitted CNC milling machine using artificial neural networks, Manufacturing Letters, 19, 1-4.
5. Data School. 2014. Simple guide to confusion matrix terminology. https://www.dataschool.io/simple-guide-to-confusion-matrix-terminology/ Access June 3, 2021.

