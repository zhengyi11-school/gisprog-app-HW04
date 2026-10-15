"""臺北 YouBike 空站觀察：115-1 地理資訊系統運用程式的 App 範本。

執行方式：在終端機輸入 solara run app.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import solara
from solara.components.datatable import DataTableWidget
from solara.util import IPYVUETIFY_V3

DATA_PATH = Path(__file__).parent / "data" / "youbike_w3_長表.csv"

# 讀檔放在元件外面：App 啟動時只讀一次，切換選項時不會重新讀檔。
# sno、act 指定為字串，避免被自動轉成整數（W3 的 read_json 陷阱，read_csv 也一樣）。
df = pd.read_csv(DATA_PATH, dtype={"sno": str, "act": str})
營運資料 = df[df["act"] == "1"]  # 空站比例只計算營運中的站
print('讀取成功')

時段們 = sorted(df["時段"].unique())
行政區們 = sorted(df["sarea"].unique())
行政區選項 = ["全區"] + 行政區們
資料時間 = "、".join(sorted(df["snapshot_time"].dropna().unique()))

# reactive：值改變時，用到它的元件會自動重新執行。
門檻 = solara.reactive(0)   #值有變動，他就會通知大家
時段 = solara.reactive(時段們[0])
行政區 = solara.reactive("全區")


def 各區空站比例(資料, 門檻值):
    """計算各區的站數、空站數與空站比例（可借車 <= 門檻值 算空站）。"""
    資料 = 資料.assign(空站=資料["available_rent_bikes"] <= 門檻值)
    表 = 資料.groupby("sarea").agg(站數=("sno", "size"), 空站數=("空站", "sum"))
    表["空站比例"] = (表["空站數"] / 表["站數"]).round(3)
    return 表.sort_values("空站比例", ascending=False).reset_index()


@solara.component
def 各區資料表(表, 選取行政區):
    """顯示各區彙總資料，並醒目標示目前選取的行政區。"""
    欄位們 = list(表.columns)
    表格資料 = []
    選取列 = None

    for 列索引, (_, 列) in enumerate(表.iterrows()):
        if 列["sarea"] == 選取行政區:
            選取列 = 列索引

        資料列 = {"__row__": 列索引}
        for 欄位 in 欄位們:
            資料列[欄位] = str(列[欄位])
        表格資料.append(資料列)

    if IPYVUETIFY_V3:
        表頭 = [{"title": 欄位, "key": 欄位, "sortable": False} for 欄位 in 欄位們]
    else:
        表頭 = [{"text": 欄位, "value": 欄位, "sortable": False} for 欄位 in 欄位們]

    每頁筆數 = max(10, len(表格資料))
    選項 = {
        "descending": False,
        "page": 1,
        "itemsPerPage": 每頁筆數,
        "sortBy": [],
        "totalItems": len(表格資料),
    }

    return DataTableWidget.element(
        total_length=len(表格資料),
        items=表格資料,
        headers=表頭,
        headers_selections=[],
        options=選項,
        items_per_page=每頁筆數,
        selections=[],
        selection_colors=[],
        selection_enabled=False,
        highlighted=選取列,
        scrollable=False,
        column_actions=[],
        cell_actions=[],
        _column_actions_callbacks=[],
        _cell_actions_callbacks=[],
        on_column_header_hover=None,
        column_header_widget=None,
    )


@solara.component   #它只是裝飾器
def Page(): #solora是方便寫程式的東東
    solara.Title("YouBike 空站觀察")
    solara.Markdown("# 臺北 YouBike 各區空站比例")

    # 滑桿預設會撐滿整個頁寬，用 Column 限制最大寬度，比較好操作。
    with solara.Column(style={"max-width": "480px"}):
        solara.SliderInt("空站門檻：可借車 ≤", value=門檻, min=0, max=5)    #這裡滑竿讓“門檻”被改變了，reactive接下來也會通知大家改變
    solara.ToggleButtonsSingle(value=時段, values=時段們)
    solara.Select("選擇行政區", value=行政區, values=行政區選項)

    當時 = 營運資料[營運資料["時段"] == 時段.value]
    表 = 各區空站比例(當時, 門檻.value)
    if 行政區.value == "全區":
        圖表顏色 = ["所有行政區"] * len(表)
        顏色對照 = {"所有行政區": "#4C78A8"}
        表格選取行政區 = None
    else:
        圖表顏色 = [
            "選取行政區" if 區 == 行政區.value else "其他行政區"
            for 區 in 表["sarea"]
        ]
        顏色對照 = {"選取行政區": "#E45756", "其他行政區": "#B8C4CE"}
        表格選取行政區 = 行政區.value

    圖表資料 = 表.assign(顯示狀態=圖表顏色)

    圖 = px.bar(
        圖表資料,
        x="空站比例",
        y="sarea",
        color="顯示狀態",
        color_discrete_map=顏色對照,
        orientation="h",
        title=f"{時段.value}，可借車 ≤ {門檻.value} 算空站（只算營運中的站）",
        labels={"sarea": "", "空站比例": "空站比例", "顯示狀態": ""},
    )
    # 每區給 30 px 高度，行政區名稱才不會被 Plotly 自動隔行省略；換成區數更多的縣市也適用。
    圖.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_tickformat=".0%",
        height=150 + 30 * len(表),
        showlegend=False,
    )
    solara.FigurePlotly(圖)

    solara.Markdown("## 各行政區空站狀況")
    各區資料表(表, 表格選取行政區)

    solara.Markdown("## 站點狀況")

    區域資料 = df[df["時段"] == 時段.value]
    if 行政區.value != "全區":
        區域資料 = 區域資料[區域資料["sarea"] == 行政區.value]
    區域資料 = 區域資料.sort_values(["sarea", "sna"])
    站點表 = 區域資料[
        ["sna", "act", "Quantity", "available_rent_bikes"]
    ].rename(
        columns={
            "sna": "站點",
            "act": "是否營運中",
            "Quantity": "總車柱數",
            "available_rent_bikes": "可借車數",
        }
    )
    站點表["是否營運中"] = 站點表["是否營運中"].map({"1": "是", "0": "否"})
    solara.DataFrame(站點表)

    solara.Markdown(
        "資料來源：臺北市 YouBike 2.0 即時資料（臺北市資料大平臺），"
        "依政府資料開放授權條款第 1 版使用。"
        f"資料時間：{資料時間}。"
    )
