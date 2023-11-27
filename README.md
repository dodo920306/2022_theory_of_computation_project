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

<img src="images/db_user.png" width="300"/>

#### 建立預約資料

<img src="images/db_activities.png" width="300"/>

### 取消預約
選擇欲取消的預約:

<img src="images/cancel.png" width="300"/>

### 集點
<img src="images/point.png" width="300"/>

### 最新消息
<img src="images/news.png" width="300"/>

### 與我聯繫
<img src="images/contact.png" width="300"/>


取消再按對應的回應按鍵，一樣可以切回預約狀態，不須從頭預約
