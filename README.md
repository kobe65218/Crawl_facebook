# 運用selenium爬取Faceook

## 目的 ：

運用network活動、即時貼文數及滑動距離來判斷滑動是否到底，爬取粉絲頁所有貼文及留言

## 停止捲動邏輯 ：

1. network活動
發現每當滑動捲軸時就會向後端 https://www.facebook.com/ajax/bulk-route-definitions/ post取資料

2. 因此每一次post就等待現在貼文大於post前貼文，在繼續滑動

3. 如果滑動後沒有post以及捲軸位置也沒有變化就break，停止滑動

