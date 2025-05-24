import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from dateutil.relativedelta import relativedelta as rel
from sklearn.linear_model import LinearRegression

df = pd.read_excel("MAJOR.xlsx", sheet_name="MAJOR")

df.columns = [
"วันที่", "ราคาเปิด", "ราคาสูงสุด", "ราคาต่ำสุด", "ราคาเฉลี่ย", "ราคาปิด",
"เปลี่ยนแปลง", "เปลี่ยนแปลง(%)", "ปริมาณ(พันหุ้น)", "มูลค่า(ล้านบาท)",
"SET Index", "SET เปลี่ยนแปลง(%)"
]

thai_months = {
"ม.ค.": "01", "ก.พ.": "02", "มี.ค.": "03", "เม.ย.": "04",
"พ.ค.": "05", "มิ.ย.": "06", "ก.ค.": "07", "ส.ค.": "08",
"ก.ย.": "09", "ต.ค.": "10", "พ.ย.": "11", "ธ.ค.": "12"
}

def convert_thai_date(thai_date_str):
    for th, num in thai_months.items():
        if th in thai_date_str:
            day, month_th, year_th = thai_date_str.replace(",", "").split()
            month = thai_months[month_th]
            year = int(year_th) - 543
            return f"{year}-{month}-{int(day):02d}"
    return None

df = df[~df["วันที่"].isna() & ~df["วันที่"].str.contains("วันที่")]
df["วันที่"] = df["วันที่"].apply(convert_thai_date)
df["วันที่"] = pd.to_datetime(df["วันที่"])
df = df.dropna()

def duration(month):
    end = df["วันที่"].iloc[0] - rel(months=month)
    return len(df[df["วันที่"] >= end])

def table(month):
    tbl = df.iloc[:duration(month)]
    tbl["วันที่"] = tbl["วันที่"].dt.date
    return tbl

def graph(month):
    matplotlib.rcParams['font.family'] = 'DejaVu Sans'
    df_sorted = df.sort_values("วันที่", ascending=False)
    X = df_sorted["วันที่"].iloc[:duration(month)].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    y = df_sorted["ราคาปิด"].iloc[:duration(month)].values
    model = LinearRegression()
    model.fit(X, y)
    trend = model.predict(X)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_sorted["วันที่"].iloc[:duration(month)], y, label="Actual Closing Price")
    ax.plot(df_sorted["วันที่"].iloc[:duration(month)], trend, label="Trend (Linear Regression)", linestyle="--", color="red")
    ax.set_title("MAJOR Closing Price Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price (Baht)")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig
