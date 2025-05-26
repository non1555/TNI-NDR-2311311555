import streamlit as st
import data as data

st.set_page_config(layout="wide") 

row1 = st.columns([1,10,1])

with row1[1]:

    row1_sub = st.columns(6)

    with row1_sub[0]:
        st.title("MAJOR")

    with row1_sub[1]:
        st.header(data.df["ราคาปิด"][0] )
        change = str(data.df["เปลี่ยนแปลง"][0]) + " (" + str(data.df["เปลี่ยนแปลง(%)"][0]) + "%)"
        if data.df["เปลี่ยนแปลง"][0] > 0.00:
            st.success(change)
        else:
            st.error(change)

    with row1_sub[3]:
        st.error("lowest : " + str(data.df["ราคาต่ำสุด"][0]))
        st.success("hightest : " + str(data.df["ราคาสูงสุด"][0]))

    with row1_sub[4]:
        st.write("Volume ('000 shares)")
        st.subheader(str(data.df["ปริมาณ(พันหุ้น)"][0]))

    with row1_sub[5]:
        st.write("Value (Million Baht)")
        st.subheader(str(data.df["มูลค่า(ล้านบาท)"][0]))

row2 = st.columns([1,4,1])

with row2[1]:
    month = st.radio("Month(s)",[1,3,6], index=2, horizontal=True)
    st.pyplot(data.graph(month))

row3 = st.columns(1)

with row3[0]:
    st.write("Data of " + str(month) + " Months")
    st.dataframe(data.table(month), use_container_width=True)