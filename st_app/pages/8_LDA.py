import streamlit as st
st.write("## Тематическое моделирование названий видео по LDA:")
st.write("График вероятностного распределения тем названий видео, демонстрирующий, какие темы присутствуют в каждом названии и с какой вероятностью. Это позволяет увидеть основные тематические группы и понять, как часто и в каком контексте упоминаются определенные темы в названиях видеороликов.")
with open("st_app/lda_visualization_unigram.html", 'r') as lda:
    plot=lda.read()
st.write("## LDA Unigram")
st.components.v1.html(plot, height=1000, width=1200)

with open("st_app/lda_visualization_bigram.html", 'r') as lda:
    plot=lda.read()
st.write("## LDA Bigram")
st.components.v1.html(plot, height=1000, width=1200)
