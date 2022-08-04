import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer

import matplotlib.pyplot as plt
import seaborn as sns

import openpyxl

def render_html(file,height=700,width=700):
	html_file = codecs.open(file,'r')
	page = html_file.read()
	stc.html(page,width=width,height=height,scrolling=True)

stc.html("<h1 style='color:blue;'>NLP text analys</h1>",height=80)

# DICTIONARY
ordlista = {'fall':['halkade', 'fall', 'ramlade'], 
    'fel dosering':['dos', 'dosering', 'feldos', 'fel dosering']}

custom_biwords = ['fel medicinering', 'felaktig behandling', 'felaktig dosering']

# FUNCTIONS
# tokenization with bi-words and cleaning
def custom_tokenizer(rapport):
    token_custom = []
    for item in custom_biwords:
        token_custom += RegexpTokenizer(item).tokenize(rapport.lower())
    tokens = nltk.word_tokenize(rapport.lower())
    tokens = token_custom + tokens
    stop_words_sv = stopwords.words('swedish')
    tokens_no_stopwords = [word for word in tokens if word not in stop_words_sv]
    return tokens_no_stopwords

# extracting incidents
def incident_extractor(tokens_no_stopwords):
    res = []
    for key, value in ordlista.items(): 
        for j in value:
            if j in tokens_no_stopwords:
                res.append(key)
            else:
                continue
    return res

def main():
    uploaded_file = st.sidebar.file_uploader("Choose an Excel file")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        stc.html("<h2 style='color:navy;'>Rådata</h2>",height=80)

        st.write(df)
        # preparing df with classified cases
        df['olyckor'] = df['rapport'].apply(custom_tokenizer).apply(incident_extractor).apply(set).apply(list).apply(''.join)
        
        stc.html("<h2 style='color:blue;'>Olyckstyp extrahering</h2>",height=80)
        
        st.write(df)
        # Plot: Incident frequency
        stc.html("<h2 style='color:blue;'>Olycksfrekvens</h2>",height=80)

        fig, bar = plt.subplots()
        bar = sns.barplot(x = df.olyckor.value_counts().index,
                y = df.olyckor.value_counts())
        bar.set(ylim=(0, None))
        fig
        
        # Plot: Incident frequency around the clock
        stc.html("<h2 style='color:blue;'>Olycksfrekvens dygnet runt</h2>",height=80)

        df_time_gr = pd.DataFrame(df.groupby('tid').count()['rapport'])
        df_time_gr = df_time_gr.reset_index()

        fig, g = plt.subplots()
        g = sns.barplot(data = df_time_gr,                
            x= 'tid',                  
            y = 'rapport',
                palette = sns.color_palette('crest', n_colors = len(df_time_gr['tid'])))
        g.set(xlabel = 'klockslag', ylabel = 'olycksfrekvens')
        g.set_xticklabels(g.get_xticklabels(), rotation=30)
        fig

    else:
        st.write('Upload Excel file')

if __name__ == "__main__":
	main()

