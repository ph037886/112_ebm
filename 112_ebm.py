import streamlit as st
from deta import Deta
import pandas as pd
from random import randrange

def link_deta(base_name): #連接Deta資料庫
    deta = Deta(st.secrets['DB_TOKEN'])
    db = deta.Base(base_name)
    return db

db=link_deta(st.secrets['DB'])

st.set_page_config(page_title='112年實證藥學-抽籤網頁',layout="wide") #修改網頁title，並預設為寬廣模式
st.markdown('## 112年實證藥學-抽籤網頁') 

st.markdown('---') 
st.markdown('### 抽點~')

if st.button('抽'):
    while True:
        r=randrange(0,60) #隨機產生亂數
        #排除已經抽到的人，有抽到過的人在資料庫裡面會註記OK
        #因此如果抽到重覆，出來的資料量會是0，不會觸發break，就會再重抽
        who=db.fetch({'key':str(r),'1120502?ne':'OK'})
        who=who.items
        if len(who)==1:
            who=who[0]
            break
    #很無聊的加入streamlit的小動畫
    if r%2==0:
        st.balloons() 
    else:
        st.snow()
    #Deta抽出來的資料是字典，用字典的方式取值
    st.markdown('#### '+'學號：'+str(who['學號']))
    st.markdown('#### '+'班級：'+who['學生班級'])
    st.markdown('#### '+'姓名：'+who['姓名'])
    st.markdown('---') 
    updates={"1120502":'OK'}
    #把抽過的人回寫回資料庫
    db.update(updates, str(r))
else:
    st.write('尚未抽出')


