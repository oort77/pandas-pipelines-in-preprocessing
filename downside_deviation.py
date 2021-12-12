#!/usr/bin/env python
# coding: utf-8


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import pickle
plt.rcParams["figure.figsize"] = [12, 8]
plt.rcParams["figure.dpi"] = 120
plt.style.use('fivethirtyeight')


st.set_page_config(page_title='Downside deviation',
                   page_icon='./lincoln_indy.ico', layout='wide', initial_sidebar_state='auto')

with open('./df.pickle', 'rb') as f:
    df = pickle.load(f)

st.header('Downside deviation')
target = st.sidebar.slider('Target', min_value=-15, max_value=40, value=1)

col1, col2 = st.columns([3, 5])

with col1:
    st.subheader("Data: ")
    st.markdown('<hr></hr>', unsafe_allow_html=True)
    df['Year'] = df['Year'].apply(lambda x: int(x))
    df['Return-Target'] = df['Return'] - target
    df['Diffs'] = target*(df['Return-Target'] < 0)
    # df.set_index('Year', drop=True, inplace=True)
    st.dataframe(df[['Year', 'Return', 'Return-Target']])
    downside_deviation = np.sqrt(
        ((df.loc[df['Return-Target'] < 0, 'Return-Target'])**2).sum()/df.shape[0])
    upside_deviation = np.sqrt(
        ((df.loc[df['Return-Target'] > 0, 'Return-Target'])**2).sum()/df.shape[0])

    st.write(
        f'**Downside deviation** = {downside_deviation:.2f},  **upside deviation** = {upside_deviation:.2f}')


with col2:

    bar1 = alt.Chart(df, title="Returns, target and upside/downside deviations").mark_bar(size=30).encode(
        x='Year:O',
        y='Return'
    ).properties(
        width=800, height=500)
    alt.Axis(titleFontSize=36)

    bar2 = alt.Chart(df).mark_bar(opacity=0.6, size=30,
                                  color='purple').encode(
        alt.X('Year:O'),
        alt.Y('Diffs', title="Returns")
    ).properties(
        width=800, height=500)

    lines = pd.DataFrame(
        columns=['target', 'upside_deviation', 'downside_deviation'])
    lines.loc[0, :] = [target, target +
                       upside_deviation, target-downside_deviation]

    line_target = alt.Chart(lines).mark_rule(color='orange', size=3).encode(
        alt.Y('target:Q'))

    line_up = alt.Chart(lines).mark_rule(color='green', size=2).encode(
        alt.Y('upside_deviation:Q'))
    line_down = alt.Chart(lines).mark_rule(color='red', size=2).encode(
        alt.Y('downside_deviation:Q'))

    chart = bar1+bar2+line_target+line_up+line_down

    st.altair_chart(chart)
    # import seaborn as sns

    fig,ax=plt.subplots(figsize=(10,5),dpi=200)
    # sns.distplot(df['Return'],bins=9, color='green', hist_kws={"linewidth": 3,
    #                         "alpha": 1, "color": "lightblue"})
    plt.hist(df['Return'],bins=9,rwidth=.45, color='lightblue')
    plt.axvline(x=target,color='orange')
    plt.axvline(x=target +
                       upside_deviation,color='green')
    plt.axvline(x=target-downside_deviation,color='red')

    st.pyplot(fig)

