import pandas as pd
import numpy as np
import os


# (1) Structure du trafic multimodal (interne et échange) en se basant sur des matrices globales

## Cette fonction permet d'identifier avec un chiffre 1 si l'origine ou la destination sont dans le périmètre restreint (centre/kern) ou dans le périmètre élargi (agglomeration)
def replace_by_one(df:pd.DataFrame):
    df.loc[df['origin_in_agglomeration'] > 0, 'origin_in_agglomeration'] = 1
    df.loc[df['destination_in_agglomeration'] > 0, 'destination_in_agglomeration'] = 1
    df.loc[df['origin_in_kern'] > 0, 'origin_in_kern'] = 1
    df.loc[df['destination_in_kern'] > 0, 'destination_in_kern'] = 1
    return(df)

## Cette fonction permet de calculer le trafic interne et le trafic d'échange par rapport à chacun des périmètres en déplacements par unité de temps par mode
def interne_echange(df:pd.DataFrame):
    df['interne_agglo']=df.origin_in_agglomeration*df.destination_in_agglomeration*df.total
    df['interne_centre']=df.origin_in_kern*df.destination_in_kern*df.total
    df['echange_agglo']=abs(df.origin_in_agglomeration-df.destination_in_agglomeration)*df.total
    df['echange_centre']=abs(df.origin_in_kern-df.destination_in_kern)*df.total
    return(df)

## Cette fonction permet de combiner dans le même tableau l'ensemble des modes
def dansTableau(df:pd.DataFrame,structure:pd.DataFrame,i,mode_transport):
    structure.at[i,'mode_transport']=mode_transport
    structure.at[i,'interne_agglo']=df['interne_agglo'].sum()
    structure.at[i,'interne_centre']=df['interne_centre'].sum()
    structure.at[i,'echange_agglo']=df['echange_agglo'].sum()
    structure.at[i,'echange_centre']=df['echange_centre'].sum()
    return(structure)

# (2) Identification des principales relations par modes ou totaux pour l'ensemble des relations ou pour le trafic interne ou d'échange en se basant sur des matrices globales

## Le trafic de transit et hors périmètre est retiré des dataframes
def clean(test:pd.DataFrame):
    test['somme']=test['origin_in_agglomeration']+test['destination_in_agglomeration']+test['origin_in_kern']+test['destination_in_kern']
    test_sans0 = test[test['somme'] != 0]
    return (test_sans0)

## Cette fonction combine les codes orgine et destination en commençant par celui ayant la plus "petite" valeur
def sort_code(df:pd.DataFrame):
    df['code']=df.iloc[:,0]+ "&" + df.iloc[:,1]
    df['min']=df[df.columns[0:2]].min(axis=1)
    df['max']=df[df.columns[0:2]].max(axis=1)
    df['ordered_code']=df['min']+ "&" + df['max']
    return(df)

## Cette fonction combine les fichiers dans le même dataframe en spécifiant pour chaque colonne le mode en question
def mergeMatrix(df_TP:pd.DataFrame, df_Piet:pd.DataFrame, df_Velo:pd.DataFrame, df_TIM:pd.DataFrame):
    #ajouter les attributs code et ordered_code
    df_TP=sort_code(df_TP)
    df_TIM=sort_code(df_TIM)
    df_Velo=sort_code(df_Velo)
    df_Piet=sort_code(df_Piet)
    #renommer les attributs pour la concaténation
    df_TP.rename(columns={'origin':'origin_TP','destination':'destination_TP','total':'total_TP','origin_in_agglomeration':'origin_in_agglomeration_TP','destination_in_agglomeration':'destination_in_agglomeration_TP','origin_in_centre':'origin_in_centre_TP','destination_in_centre':'destination_in_centre_TP','interne_agglo':'interne_agglo_TP', 'interne_centre':'interne_centre_TP', 'echange_agglo':'echange_agglo_TP',
       'echange_centre':'echange_centre_TP','somme':'somme_TP','ordered_code':'ordered_code_TP'},inplace=True)
    df_TIM.rename(columns={'origin':'origin_TIM','destination':'destination_TIM','total':'total_TIM','origin_in_agglomeration':'origin_in_agglomeration_TIM','destination_in_agglomeration':'destination_in_agglomeration_TIM','origin_in_centre':'origin_in_centre_TIM','destination_in_centre':'destination_in_centre_TIM','interne_agglo':'interne_agglo_TIM', 'interne_centre':'interne_centre_TIM', 'echange_agglo':'echange_agglo_TIM',
       'echange_centre':'echange_centre_TIM','somme':'somme_TIM','ordered_code':'ordered_code_TIM'},inplace=True)
    df_Velo.rename(columns={'origin':'origin_Velo','destination':'destination_Velo','total':'total_Velo','origin_in_agglomeration':'origin_in_agglomeration_Velo','destination_in_agglomeration':'destination_in_agglomeration_Velo','origin_in_centre':'origin_in_centre_Velo','destination_in_centre':'destination_in_centre_Velo','interne_agglo':'interne_agglo_Velo', 'interne_centre':'interne_centre_Velo', 'echange_agglo':'echange_agglo_Velo',
       'echange_centre':'echange_centre_Velo','somme':'somme_Velo','ordered_code':'ordered_code_Velo'},inplace=True)
    df_Piet.rename(columns={'origin':'origin_Piet','destination':'destination_Piet','total':'total_Piet','origin_in_agglomeration':'origin_in_agglomeration_Piet','destination_in_agglomeration':'destination_in_agglomeration_Piet','origin_in_centre':'origin_in_centre_Piet','destination_in_centre':'destination_in_centre_Piet','interne_agglo':'interne_agglo_Piet', 'interne_centre':'interne_centre_Piet', 'echange_agglo':'echange_agglo_Piet',
       'echange_centre':'echange_centre_Piet','somme':'somme_Piet','ordered_code':'ordered_code_Piet'},inplace=True)
    #fusion des matrices
    df_V=pd.concat([df_TP.set_index('code'),df_Piet.set_index('code'),df_Velo.set_index('code'),df_TIM.set_index('code')], axis = 1)
    return df_V

# (3) Identification du trafic d'échange sur une pénétrante ou toutes les pénétrantes par rapport à un périmètre

## Cette fonction permet pour chacun des axes pénétrants d'identifier le trafic interne, d'échange et de transit
def AxePenetrant(df:pd.DataFrame,structure:pd.DataFrame,i,Penetrante,perimetre_centre,perimetre_agglo):
    structure.at[i,'Penetrante']=Penetrante
    structure.at[i,'interne_agglo']=df['interne_agglo'].sum()
    structure.at[i,'interne_centre']=df['interne_centre'].sum()
    structure.at[i,'echange_agglo']=df['echange_agglo'].sum()
    structure.at[i,'echange_centre']=df['echange_centre'].sum()
    structure.at[i,'Transit_centre']=df['total'].sum()-df['interne_centre'].sum()-df['echange_centre'].sum()
    structure.at[i,'Transit_agglo']=df['total'].sum()-df['interne_agglo'].sum()-df['echange_agglo'].sum()
    structure.at[i,'perimetre_centre']=perimetre_centre
    structure.at[i,'perimetre_agglo']=perimetre_agglo
    structure.at[i,'Transit_centre']=structure.at[i,'Transit_centre']*structure.at[i,'perimetre_centre']
    structure.at[i,'Transit_agglo']=structure.at[i,'Transit_agglo']*structure.at[i,'perimetre_agglo']
    return(structure)

## Cette fonction calcule le trafic de transit et l'introduit dans le tableau
def TransitV(df:pd.DataFrame,df1:pd.DataFrame,i,mode_transport_Annee):
    df.at[i,'mode_transport_Annee']=mode_transport_Annee
    df.at[i,'Transit_centre']=df1['Transit_centre'].sum()/2 # La divison par deux permet de supprimer les trajets sortant par une autre pénétrante
    df.at[i,'Transit_agglo']=df1['Transit_agglo'].sum()/2 # La divison par deux permet de supprimer les trajets sortant par une autre pénétrante
    return(df)