import os
import streamlit as st
import pandas as pd
from collections import Counter
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import seaborn as sns
import plotly.express as px
import numpy as np
from matplotlib import font_manager

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 指定SimHei字体文件的相对路径
font_path = os.path.join(current_dir, 'SimHei.ttf')

# 打印字体文件路径以确认
st.write(f"Font path: {font_path}")

# 检查文件是否存在
if not os.path.exists(font_path):
    st.error("字体文件未找到，请检查字体文件路径。")
else:
    # 添加字体到matplotlib
    try:
        font_manager.fontManager.addfont(font_path)
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        st.success("字体文件加载成功！")
    except Exception as e:
        st.error(f"加载字体文件时出错: {e}")

# 全局设置Seaborn的字体
sns.set(font="SimHei", style="whitegrid")

# 对于Plotly，我们需要在每次创建图表时单独设置字体，因为Plotly不支持全局字体设置
def update_plotly_layout(fig):
    fig.update_layout(
        font=dict(
            family="SimHei",
            size=14,
            color="black"
        )
    )

# 获取页面内容并解析正文
def get_words(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding  # 设置编码防止乱码
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 只提取正文部分
    paragraphs = soup.find_all('p')
    text = ' '.join([paragraph.get_text() for paragraph in paragraphs])

    return text

# 使用WordCloud库绘制词云图
def plot_wordcloud_wordcloud(top_n_words):
    frequencies = {word: count for word, count in top_n_words.items()}
    wordcloud = WordCloud(font_path=font_path, background_color='white', width=800, height=600).generate_from_frequencies(frequencies)

    # 将词云图显示为图片，并调整图片大小
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt.gcf())  # 使用Streamlit显示图表

# 使用Matplotlib库绘制纵向柱状图
def plot_bar_chart_vertical_matplotlib(top_n_words):
    data = {'关键词': list(top_n_words.keys()), '词频': list(top_n_words.values())}
    df = pd.DataFrame(data)
    df = df.sort_values(by='词频', ascending=False)  # 降序排列数据

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df['关键词'], df['词频'], color='skyblue')
    ax.set_xlabel('关键词', fontsize=12)
    ax.set_ylabel('词频', fontsize=12)
    ax.set_title('关键词频率分析', fontsize=14)
    st.pyplot(fig)  # 使用Streamlit显示图表

# 使用Matplotlib库绘制横向柱状图
def plot_bar_chart_horizontal_matplotlib(top_n_words):
    data = {'关键词': list(top_n_words.keys()), '词频': list(top_n_words.values())}
    df = pd.DataFrame(data)
    df = df.sort_values(by='词频', ascending=True)  # 升序排列数据

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(df['关键词'], df['词频'], color='skyblue')
    ax.set_xlabel('词频', fontsize=12)
    ax.set_ylabel('关键词', fontsize=12)
    ax.set_title('关键词频率分析', fontsize=14)
    st.pyplot(fig)  # 使用Streamlit显示图表

# 使用Matplotlib库绘制折线图
def plot_line_chart_matplotlib(top_n_words):
    data = {'关键词': list(top_n_words.keys()), '词频': list(top_n_words.values())}
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['关键词'], df['词频'], marker='o', color='skyblue')
    ax.set_xlabel('关键词', fontsize=12)
    ax.set_ylabel('词频', fontsize=12)
    ax.set_title('关键词频率分析', fontsize=14)
    st.pyplot(fig)  # 使用Streamlit显示图表

# 使用Matplotlib库绘制散点图
def plot_scatter_chart_matplotlib(top_n_words):
    data = {'关键词': list(top_n_words.keys()), '词频': list(top_n_words.values())}
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(df['关键词'], df['词频'], color='skyblue')
    ax.set_xlabel('关键词', fontsize=12)
    ax.set_ylabel('词频', fontsize=12)
    ax.set_title('关键词频率分析', fontsize=14)
    st.pyplot(fig)  # 使用Streamlit显示图表

# 使用Matplotlib库绘制饼状图
def plot_pie_chart_matplotlib(top_n_words):
    labels = list(top_n_words.keys())
    sizes = list(top_n_words.values())
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')  

    # 添加图例
    ax.legend(wedges, labels, title="关键词", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # 调整图例字体大小
    for text in texts + autotexts:
        text.set_fontsize(12)

    st.pyplot(fig)  # 使用Streamlit显示图表

# 使用Seaborn库绘制箱线图
def plot_box_plot_seaborn(top_n_words):
    data = {'关键词': list(top_n_words.keys()), '词频': list(top_n_words.values())}
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x="关键词", y="词频", data=df, color="skyblue")
    ax.set_xlabel('关键词', fontsize=12)
    ax.set_ylabel('词频', fontsize=12)
    ax.set_title('词频箱线图', fontsize=14)
    st.pyplot(fig)  # 使用Streamlit显示图表

# 使用Plotly绘制交互式条形图
def plot_interactive_bar_chart_plotly(top_n_words):
    data = {'关键词': list(top_n_words.keys()), '词频': list(top_n_words.values())}
    df = pd.DataFrame(data)
    fig = px.bar(df, x='关键词', y='词频', title='关键词频率分析', labels={'关键词': '关键词', '词频': '词频'})
    update_plotly_layout(fig)
    st.plotly_chart(fig)  # 使用Streamlit显示Plotly图表

# 提取正文文本，以utf-8编码写入txt文件
def extract_and_write_text(text, base_file_name='news'):
    output_folder = os.path.join(current_dir, 'output_files')
    os.makedirs(output_folder, exist_ok=True)  

    file_number = 1
    while os.path.exists(os.path.join(output_folder, f'{base_file_name}_{file_number}.txt')):
        file_number += 1

    output_file = os.path.join(output_folder, f'{base_file_name}_{file_number}.txt')

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

    st.success(f'成功将页面文本保存为文件{output_file}')

# 主函数
def main():
    st.title('网页词频分析器')

    # 输入 URL
    url = st.text_input('输入网页 URL:')
    if not url:
        st.warning('请输入有效的网页 URL。')
        return

    try:
        # 获取正文
        text = get_words(url) 
        # 使用jieba进行中文分词，排除标点符号和其他没有意义的中文字
        words = [word for word in jieba.lcut(text) if word.isalnum() and len(word) > 1]
        # 获取词频
        word_frequency = Counter(words)
        # 获取词语种类数
        word_counts = len(word_frequency)

        # 选择展示词语种类的数量
        min_value = 1
        max_value = min(40, word_counts)
        n = (min_value + max_value) // 2
        n = st.slider('选择关键词数量', min_value, max_value, value=n)
        
        # 获取词频高的前n个词,并根据词频高低从高到低排序
        top_n_words = dict(sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)[:n])

        # 创建布局
        col1, col2 = st.columns([1, 1])

        # 提取正文文本并写入文件
        col1.button('提取正文文本并写入文件', on_click=lambda: extract_and_write_text(text))

        # 选择词频统计方式
        chart_type = col2.selectbox('选择可视化方式', ['词云图', '横向柱状图', '饼状图', '纵向柱状图', '折线图', '散点图', '箱线图', '交互式条形图'])

        # 根据选择的统计方式显示相应图表
        st.subheader(chart_type)
        if chart_type == '词云图':
            plot_wordcloud_wordcloud(top_n_words)
        elif chart_type == '横向柱状图':
            plot_bar_chart_horizontal_matplotlib(top_n_words)
        elif chart_type == '箱线图':
            plot_box_plot_seaborn(top_n_words)
        elif chart_type == '饼状图':
            plot_pie_chart_matplotlib(top_n_words)
        elif chart_type == '纵向柱状图':
            plot_bar_chart_vertical_matplotlib(top_n_words)
        elif chart_type == '折线图':
            plot_line_chart_matplotlib(top_n_words)
        elif chart_type == '散点图':
            plot_scatter_chart_matplotlib(top_n_words)
        elif chart_type == '交互式条形图':
            plot_interactive_bar_chart_plotly(top_n_words)

    except Exception as e:
        st.warning(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()