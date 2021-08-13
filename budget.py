#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 17:05:55 2021

@author: katebelisle
"""

import camelot
import pandas as pd
import numpy as np
import collections

def clean_currency(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    
    if isinstance(x, str):
        x=x.replace("*","")
        x=x.replace(",","")
        if x=='':
            return(0)
        elif x[0]!='$':
            return(0)
        else:
            x=x.split(' ')[0]
            x=x.replace('$',"")
            return float(x)
    return(x)

def c(itr):
    return(list(range(len(itr))))
fpath='/Users/katebelisle/Documents/fndocs/budgets/'
fn=["/Users/katebelisle/Documents/fndocs/budgets/2020-2021-BC-Approved-Budget-1-12-21.pdf",
    "/Users/katebelisle/Documents/fndocs/budgets/2019-approved-bc-combined-rev3.pdf",
    "/Users/katebelisle/Documents/fndocs/budgets/2020-final-budgets-rev1.pdf"]
tpg=[44,41,42]
fiscal=["2021","2019","2020"]
xclude=[['42'],['41'],['23','40']]
#%%
b=[]
litems=collections.defaultdict(set)
lsubitems=collections.defaultdict(set)
for r in c(fn):
    byear=fiscal[r]
    pgs=list(range(tpg[r]))
    pg=[str((p+1)) for p in pgs[1:]]
    pg=[p for p in pg if p not in xclude[r] ]
#    for p in pg:
    tables=camelot.read_pdf(fn[r],pages=",".join(pg))
 #       tables=camelot.read_pdf(fn[r],pages='3')
    dfs=True
    for t in c(tables):
        df=tables[t].df.copy()
        df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)

        titles=[sub.replace("\n", "") for sub in df.loc[0]   ]     
        titles=[sub.replace("#", "") for sub in titles   ]     
        titles=[sub.replace("*", "") for sub in titles   ]     
        titles=[sub.replace(".", " ") for sub in titles   ]     
        titles=[x if x[:3] not in ["BOS"] else f"{byear} BOS" for x in titles]
        titles=[x if x[:2] not in ["BC"] else  f"{byear} BC"  for x in titles]
#
        lineitem=titles[0].replace("-"," ")
        lineitem=lineitem.replace("  "," ")
        lineitem=lineitem.replace("\n"," ")

        lineitem=lineitem.replace("Forrest","Forest")
        if (lineitem==''):
            lineitem=titles[1]
        if (lineitem[0]==' '):
            lineitem=lineitem[:1]
        linecode=lineitem[:4]
        if(linecode[0]!='4'):
            linecode=f'4{linecode}'[:4]
        linedesc=lineitem[5:]
        litems[linecode].add(linedesc)
        print(lineitem)
        print(linedesc)
        titles[0]="item"
        if((r==0 )& (t==7)):
            df.drop(df.index[[0,1,2]],inplace=True)
        else:
            df.drop(df.index[[0,1]],inplace=True)
        df.columns=titles
        df['item'].replace("\n", " ", inplace=True)      
        df['item'].replace("-", " ", inplace=True)      
        df['item'].replace('', np.nan, inplace=True)
        df['item'].replace('\\', ' & ', inplace=True)
        df['item'].replace(' ',' ', inplace=True)
        df.dropna(subset=['item'], inplace=True)
        linecode=linecode.title()
        for i in set(df.item):
            lsubitems[linecode].add(i)
        df["linecode"]=linecode
        df["budgetyear"]=byear
        df["page"]=t
        titles=["linecode","budgetyear","page"]+titles
        
        #df["linedesc"]=linedesc
        for i in list(range(len(titles)))[4:]:
            print(i)
            print(titles[i])
#            df['item'].replace('', np.nan, inplace=True)
#            df[titles[i]].replace(to_replace="\$([0-9,\.]+).*", value=r"\1", regex=True, inplace=True)
            df[titles[(i)]] = df[titles[(i)]].apply(clean_currency)
        
        if (dfs):
            budget=df[titles]
            dfs=False
        else:
            budget=budget.append(df[titles],ignore_index=True)
    b.append(budget)
                
#%%
# budget=b[0]
# l=len(b)-1 
# for d in list(range(l)):
#    i=d+1
#    budget=budget.reset_index(drop=True)
#    new=b[i].reset_index(drop=True)
#   budget=budget.merge(new,how='outer',on=['linecode','item'])       
#%%
keynames={}
for k,v in litems.items():
    lv=list(v)
    keynames[k]=lv[0]
    
inames=[]
for k,v in lsubitems.items():
    lv=list(v)
    for n in lv:
        inames=inames+[[k,n,n.title()]]
#%%
#ixref=pd.DataFrame(inames)
#ixref.to_csv("itemnames.csv")     
ixref=pd.read_csv("itemnames.csv")[["fromv","tov"]]
xsdict=collections.defaultdict(set)
for i in range(len(ixref)):
    xsdict[ixref.fromv[i]]=ixref.tov[i]
xdict={}
xdict["item"]=xsdict


#%%
budget=pd.concat(b)
cc=[c for c in budget.columns if len(c)>0]
cc=[c for c in cc if c[0] in ['B','2']]
cc.sort()
budget.replace(xdict,inplace=True)
cby=["linecode","item","budgetyear","page"]         
cby=["linecode","item"]         
budget.sort_values(by=cby,inplace=True)
budget=budget[cby+cc].copy()
budget.to_excel("budget.xlsx")

#%%
conbudget=budget[cby+cc].groupby(cby).sum().reset_index()
#%%
totals=conbudget[conbudget["item"]=="TOTAL"].copy()
totals.to_excel("totals.xlsx")
lc=totals.linecode
k={}
k["linecode"]=keynames
#totals=totals.replace(to_replace=k,inplace=True)

