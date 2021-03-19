import PyPDF2
import os 
from os.path import isfile, join
import pandas as pd
import tkinter as tk
from tkinter import Tk
from tkinter.filedialog import askdirectory
import wordninja
import tkinter as tk
from tkinter import simpledialog


def getFolder():
    '''
    shows dialog box and return the path
    '''
    return askdirectory(title='Select Folder') 

def getWordSearch(): 
    ROOT = tk.Tk()
    ROOT.withdraw()
    return simpledialog.askstring(title="Word Search",
                                  prompt="Word to search?:")

def dictOfWhereWordIsFound(searchWord):
    folder=getFolder()
    worddict={}
    files=[f for f in os.listdir(folder) if isfile(join(folder,f))] #returns list of files in folder
    for file in files:
        location=folder+'\\'+file
        pdfFileObj=open(location, 'rb')
        pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
        pages=pdfReader.numPages
        wordarray=[]
        for i in range(pages):
            pageObj=pdfReader.getPage(i).extractText()
            if searchWord in pageObj:
                arr=pageObj.split('\n')
                for wa in arr:
                    if searchWord in wa:
                        wordarray.append(wa)
        if wordarray!=[]:
            worddict[file]=wordarray
    return worddict

def wordDictToDF(searchWord):
    worddict=dictOfWhereWordIsFound(searchWord)
    return pd.DataFrame.from_dict(worddict, orient='index')

def putSpacesBetweenWordsInDF(searchWord):
    df=wordDictToDF(searchWord)
    rows=0
    while rows < len(df):
        columns=0
        while columns< len(df.columns):
            wordList=wordninja.split(df.iloc[rows][columns])
            sentence=' '.join(word for word in wordList)
            df.iloc[rows][columns]=sentence
            columns=columns+1
        rows=rows+1
    return df

def formatForFlatFile(searchWord):
    df=putSpacesBetweenWordsInDF(searchWord)
    df2=pd.DataFrame(columns=[['Doc','Value']])
    columns=0 
    while columns<len(df.columns):
        row=0
        while row< len(df):
            toDf= [df.index,df.iloc[row][columns]]
            toDfseries = pd.Series(toDf, index = df2.columns)
            df2 = df2.append(toDfseries, ignore_index=True)
            row=row+1
        columns=columns+1
    return df2

def main():
    searchWord=getWordSearch()
    filename=searchWord+'found.csv'
    df=formatForFlatFile()
    df.to_csv(filename, index=False)