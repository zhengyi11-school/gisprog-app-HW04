---
title: YouBike 空站觀察
emoji: 🚲
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# 臺北 YouBike 空站觀察

> 上面 `---` 之間的設定是給 HuggingFace Spaces 讀的（W5 部署時使用），請保留。

115-1 地理資訊系統運用程式 App：選擇空站門檻、觀測時段及行政區，查看臺北 YouBike 各區的空站比例與站點狀況。

## App 用途

這個 App 可以回答：在選定的觀測時段，當「可借車數小於或等於門檻」視為空站時，各行政區營運中站點的空站比例是多少？哪個行政區比例較高？

選擇特定行政區後，圖表和彙總表會標示該區，站點表則列出該區在所選時段的各站營運狀態、總車柱數與可借車數。選擇「全區」會列出所選時段所有行政區的站點。

## 資料

| 項目 | 內容 |
|---|---|
| 資料提供機關 | 臺北市政府交通局 |
| 資料集 | 臺北市資料大平臺「YouBike2.0 臺北市公共自行車即時資訊」 |
| 資料集頁面 | [臺北市資料大平臺](https://data.gov.taipei/dataset/detail?id=c6bc8aed-557d-41d5-bfb1-8da24f78f2fb) |
| 即時資料介接網址 | `https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json` |
| 授權 | [政府資料開放授權條款－第 1 版](https://data.gov.tw/license)，使用時須標示來源 |
| 本 App 使用的資料時間 | 2026-09-30（三）08:34、15:49、22:35，共三個時段快照 |
| 快照檔案 | `data/youbike_w3_長表.csv` |

CSV 的 `snapshot_time` 欄位記錄的時間分別是 2026-09-30 08:34:52、15:49:52、22:35:52；介面以分鐘顯示時段。此檔案是整理後的固定快照，不會隨即時資料自動更新。

`app.py` 需要的欄位：`snapshot_time`、`時段`、`sno`、`sna`、`sarea`、`act`、`Quantity`、`available_rent_bikes`。

## 在 Codespaces 執行

1. 在 repo 頁面按 **Code → Codespaces → Create codespace on main**。
2. 等環境建好（第一次約 2–3 分鐘，會自動安裝 `requirements.txt` 的套件）。
3. 在終端機輸入：

   ```bash
   solara run app.py
   ```

4. 右下角出現提示時，按 **Open in Browser**；或到「連接埠」分頁，開啟 8765 埠。

## 修改之後

```bash
git status          # 哪些檔案被改了？
git diff            # 改了哪幾行？
git add app.py      # 只加入你確認過的檔案
git commit -m "說明你改了什麼"
git push
```

**agent 改完之後，一定先看 `git diff` 再 commit。**

## 授權

- **程式碼**（`app.py`、`Dockerfile` 等）：MIT License，見 [`LICENSE`](LICENSE)。可以自由使用、修改、公開，請保留 `LICENSE` 檔。
- **資料**（`data/youbike_w3_長表.csv`）：整理自臺北市資料大平臺「YouBike2.0 臺北市公共自行車即時資訊」，資料提供機關為臺北市政府交通局，依政府資料開放授權條款－第 1 版使用，不適用 MIT。該條款允許重製、散布及改作，但須標示原資料提供機關與資料集來源。來源與授權資訊見上方「資料」表格。
