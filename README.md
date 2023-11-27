# 2022_Theory_of_computation_project
歡迎來到青年活動中心！這是一個模擬活動預約系統的 linebot！

你可以透過與linebot互動獲取青年活動的最新消息並預約參與了解我們
(以下功能以Linebot, PostgreSQL, Pytransition實作)

## FSM
<img src="images/fsm.png" width="500"/>

它看起來超級繁雜的！這是因為為了使用者方便起見，所有 state 皆可舜切換至其他任意 state。

試試看你就知道了！使用者不需要再按錯之後「回上一動」，而是直接回去原訊息點擊正確的選項。

## 圖文選單
<img src="images/menu.png" width="300"/>

### 關於
取得使用說明

<img src="images/directions.png" width="300"/>

### 地點
取得活動中心地點

<img src="images/location.png" width="300"/>

### 預約
流程如下: 

<img src="images/book.png" width="300"/>

選擇欲參與活動類別:

<img src="images/catalog.png" width="300"/>

選擇活動:

<img src="images/activities.png" width="300"/>

選擇日期:

<img src="images/date.png" width="300"/>

選擇時間:

<img src="images/time.png" width="300"/>

確定!:

<img src="images/confirm.png" width="300"/>

### 資料庫
#### 建立使用者資料
![螢幕擷取畫面 (650)](https://user-images.githubusercontent.com/74814435/209558260-0123ccf8-8844-46cd-88a5-50bd68d6d139.png)
#### 建立預約資料
![螢幕擷取畫面 (649)](https://user-images.githubusercontent.com/74814435/209558209-1567f6d0-bf5d-4275-816b-bc9c5f7a2eae.png)

### 取消預約
選擇欲取消的預約:
![image](https://user-images.githubusercontent.com/74814435/209558506-e0eba22d-8b9d-4783-b83a-1df87d306a91.png)

### 集點
![image](https://user-images.githubusercontent.com/74814435/209558618-3964631e-e3df-4598-abb2-5021ad478b7e.png)

### 最新消息
![image](https://user-images.githubusercontent.com/74814435/209558647-b4899fe8-3c12-4387-b981-f37364e367cb.png)

### 與我聯繫
![image](https://user-images.githubusercontent.com/74814435/209558661-fd929dd9-f56b-46af-9f60-24c33a66691d.png)

<br/>
取消再按對應的回應按鍵，一樣可以切回預約狀態，不須從頭預約
