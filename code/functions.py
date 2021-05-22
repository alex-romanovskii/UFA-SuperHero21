import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
margin=30

columns=['№','Наименование предприятия','ОКВЭД','Вид деятельности','Отчетный период прошлого года (В натуральном выражении)',
    'Отчетный период прошлого года (В стоимостном выражении)','Отчетный период текущего года (В натуральном выражении)',
    'Отчетный период текущего года (В стоимостном выражении)','Отношение периодов, %','Отчетный месяц прошлого года (В натуральном выражении)',
    'Отчетный месяц прошлого года (В стоимостном выражении)','Отчетный месяц текущего года (В натуральном выражении)',
    'Отчетный месяц текущего года (В стоимостном выражении)','Отношение месяцев, %']

online_columns=['№','Наименование предприятия','ОКВЭД','Вид деятельности','Отчетный период прошлого года (В натуральном выражении)','Отчетный период прошлого года (В стоимостном выражении)','Отчетный период текущего года (В натуральном выражении)',
    'Отчетный период текущего года (В стоимостном выражении)','Отчетный месяц прошлого года (В натуральном выражении)',
    'Отчетный месяц прошлого года (В стоимостном выражении)','Отчетный месяц текущего года (В натуральном выражении)',
    'Отчетный месяц текущего года (В стоимостном выражении)','Месяц','Год']



def fig_setting(fig):
    fig['layout']['paper_bgcolor']='rgba(0,0,0,0)' 
    fig['layout']['font']['color']="#00FF00"
    fig['layout']['plot_bgcolor']='rgba(0,0,0,0)' 
    fig['layout']['font']['size']=14
    fig['layout']['margin']['l']=margin
    fig['layout']['margin']['r']=margin
    fig['layout']['margin']['t']=margin
    fig['layout']['margin']['b']=margin
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#FFFFFF')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#FFFFFF')
#     fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))
    fig.update_xaxes(tickangle=45)
    return fig

work_path='dataset/result_df.csv'

def get_label_activity():
    res=['добыча металлических руд','Добыча сырой нефти и природного газа ',
       'добыча прочих полезных ископаемых', 'предоставление услуг в области добычи полезных ископаемых',
       'производство текстильных изделий ', 'производство одежды',
       'производство кожи и изделий из кожи','производство изделий народных художественных промыслов ',
       'обработка древесины и производство изделий из дерева и пробки, кроме мебели, производство изделий из соломки и материалов для плетения','производство бумаги и бумажных изделий','производство кокса, нефтепродуктов',
       'производство химических веществ и химических продуктов','производство лекарственных средств и материалов, применяемых в медицинских целях','производство резиновых и пластмассовых изделий','производство прочей неметаллической минеральной продукции',
       'производство металлургическое','производство готовых металлических изделий, кроме машин и оборудования',
       'производство машин и оборудования для металлургии','производство машин и оборудования для добычи полезных ископаемых и строительства','производство станков, машин и оборудования для обработки металлов и прочих твердых материалов',
       'производство компьютеров, электронных и оптических изделий','производство электрического оборудования',
       'производство машин и оборудования, не включенных в другие группировки',
       'производство автотранспортных средств, прицепов и полуприцепов','производство прочих транспортных средств и оборудования','производство мебели', 'ремонт и монтаж машин и оборудования ',
       'обеспечение электрической энергией, газом и паром; кондиционирование воздуха',
       'водоснабжение; водоотведение, организация сбора и утилизации отходов, деятельность по ликвидации загрязнений']
    rr=[]
    res=[{i[:40]+'...':i} if len(i)>40 else {i:i} for i in res]
    res=[i for i in res if pd.notnull(i)]
    for i in res:
        r={}
        a,b=list(i.items())[0]
        r['label']=a
        r['value']=b
        rr.append(r)
    return rr

def get_man(df):
    df=df[df['№'].notnull()]
    res=df['Наименование предприятия'].unique()
    rr=[]
    res=[{i[:40]+'...':i} if len(i)>40 else {i:i} for i in res]
    res=[i for i in res if pd.notnull(i)]
    for i in res:
        r={}
        a,b=list(i.items())[0]
        r['label']=a
        r['value']=b
        rr.append(r)
    return rr

def man_value():
    try:
        return get_man(get_dataset())[0]['value']
    except:
        return ''


def get_dataset():
    try:
        df=pd.read_csv(work_path)
        return df
    except:
        columns=['№','Наименование предприятия','ОКВЭД','Вид деятельности','Отчетный период прошлого года (В натуральном выражении)',
    'Отчетный период прошлого года (В стоимостном выражении)','Отчетный период текущего года (В натуральном выражении)',
    'Отчетный период текущего года (В стоимостном выражении)','Отношение периодов, %','Отчетный месяц прошлого года (В натуральном выражении)',
    'Отчетный месяц прошлого года (В стоимостном выражении)','Отчетный месяц текущего года (В натуральном выражении)',
    'Отчетный месяц текущего года (В стоимостном выражении)','Отношение месяцев, %','Год','Месяц']
        df=pd.DataFrame(columns=columns)
        df.to_csv('dataset/result_df.csv',index=False)
        return df

def prepare_form(file_path, year,header=4,columns=columns):
    """
    Keyword arguments:
    file_path : str (path to xlxs file of form)
    header : int (last row containing header information)
    
    This function parse all sheets and returns a DataFrame with adjustments for further work    
    """
 
    exel_file=pd.ExcelFile(file_path)
    sheets_list=exel_file.sheet_names
    for index, sheet in enumerate(sheets_list):
        if index==0:       
            df=exel_file.parse(sheet, header=header, names=columns)
#             df.iloc[:,[2,3]]=df.iloc[:,[2,3]].fillna(method='ffill', axis=0)
            df['Месяц']=sheet
        else:
            df_new=exel_file.parse(sheet, header=header, names=columns)
#             df_new[df_new['№'].notnull()]=df_new[df_new['№'].notnull()].fillna(method='ffill', axis=0)
#             df.iloc[:,[2,3]]=df.iloc[:,[2,3]].fillna(method='ffill', axis=0)
            df_new['Месяц']=sheet
            df=pd.concat([df,df_new])
    df=df.copy()
    df.iloc[:,[2,3]]=df.iloc[:,[2,3]].fillna(method='ffill', axis=0)    
    df=df.reset_index(drop=True)
    df=df.copy()
    df.loc[:,'Год']=year
    df=df.drop_duplicates()
    return df

def pic1(months,df,period,year):
    try:
        df=df[df['№'].notnull()]
        df=df[df['Месяц'].isin(months)]
        df=df[['Наименование предприятия', 'Месяц','Год','ОКВЭД',period]]
        df=df[df['Год']==year]
        df = df.groupby('Наименование предприятия', as_index=False).agg({'ОКВЭД':'first',
                                    period:'sum'})
        result=df[period].sum()

        fig = px.sunburst(df,
                          path=[[result]*len(df),"ОКВЭД", "Наименование предприятия"],
                          values=period, width=700, height=700,color_discrete_sequence=px.colors.qualitative.Light24)
        fig=fig_setting(fig)   
        return fig
    except:
        fig=px.sunburst(width=700, height=700)
        fig=fig_setting(fig)
        return fig
    

def pic2(df,manufacture, relation,years):
    try:
        df=df[df['№'].notnull()]
        df=df[df['Наименование предприятия']==manufacture]
        df=df[df['Год'].isin(years)]
        fig = px.line(df, x='Месяц', y=relation, color='Год',title="{}".format(manufacture),color_discrete_sequence=px.colors.qualitative.Light24)
        fig=fig_setting(fig)
        fig.update_layout(xaxis_title="Месяца",legend_title="Года")
        return fig
    except:
        fig=px.line(width=700, height=700)
        fig=fig_setting(fig)
        fig.update_layout(xaxis_title="Месяца",legend_title="Года")
        return fig
    

def pic3(df,years,period,stat):
    try:
        df=df[df['№'].notnull()]
        df = df.groupby([stat,'Год'], as_index=False)[period].sum()
        df=df[df['Год'].isin(years)]
        df['Год']=df['Год'].astype(str)
        x=df[stat].apply(lambda x:x[:20]+'...' if len(x)>20 else x[:20])
        fig = px.bar(df, x=x, y=period,
                 color='Год', barmode='group',width=700, height=700,color_discrete_sequence=px.colors.qualitative.Light24)
        fig=fig_setting(fig)
        fig.update_layout(xaxis_title="{}".format(stat),legend_title="Года")
        return fig
    except:
        fig=px.bar(width=700, height=700)
        fig=fig_setting(fig)
        fig.update_layout(xaxis_title="{}".format(stat),legend_title="Года")
        return fig
 
def pic4(df,months,period,stat):
    try:
        df=df[df['№'].notnull()]
        df = df.groupby([stat,'Месяц'], as_index=False)[period].sum()
        df=df[df['Месяц'].isin(months)]
        x=df[stat].apply(lambda x:x[:20]+'...' if len(x)>20 else x[:20])
        fig = px.bar(df, x=x, y=period,
                 color='Месяц', barmode='group',
                 width=700, height=700,color_discrete_sequence=px.colors.qualitative.Light24)
        fig=fig_setting(fig)
        fig.update_layout(xaxis_title="{}".format(stat),legend_title="Месяца")
        return fig
    except:
        fig=px.bar(width=700, height=700)
        fig=fig_setting(fig)
        fig.update_layout(xaxis_title="{}".format(stat),legend_title="Месяца")
        return fig

def pic5(df,regions,man_type):
    try:
        df=df[(df['регион'].isin(regions)) & (df['тип производства']==man_type)]
        fig = px.line(df, x="Год", y="величина", color='регион',width=700
                          , height=700,color_discrete_sequence=px.colors.qualitative.Light24)
        fig=fig_setting(fig)
        fig.update_layout(xaxis_title="Года",yaxis_title='Индекс производства',legend_title="Регионы")
        return fig
    except:
        fig = px.line(width=700,height=700,color_discrete_sequence=px.colors.qualitative.Light24)
        fig=fig_setting(fig)
        fig.update_layout(xaxis_title="Года",yaxis_title='Индекс производства',legend_title="Регионы")
        return fig

def pic6(df, months,years,each=False):
    try:
        label_y='Суммарное количество отчетов с пропусками'
        df=df[df['№'].notnull()]
        df=df.copy()
        df.loc[:,'Пропуски']=df.isnull().sum(axis = 1)
        if each==False:
            df.loc[:,'Пропуски']=df.loc[:,'Пропуски'].apply(lambda x: 1 if x>0 else 0)
            label_y='Суммарное количество пропусков в отчетах'
        df = df.groupby(['Наименование предприятия','Месяц','Год'], as_index=False)['Пропуски'].sum()
        df=df[(df['Месяц'].isin(months)) & (df['Год'].isin(years))]
        df = df.groupby(['Наименование предприятия','Год'], as_index=False)['Пропуски'].sum()
        df=df[df['Пропуски']>0]
        df['Год']=df['Год'].astype(str)
        x=df['Наименование предприятия'].apply(lambda x:x[:20]+'...' if len(x)>20 else x[:20])
        fig = px.bar(df, x=x, y=['Пропуски'],
                 color='Год', barmode='group',width=650, height=650,color_discrete_sequence=px.colors.qualitative.Light24)
        fig=fig_setting(fig)
        fig.update_layout(xaxis_title="Предприятия",yaxis_title=label_y,legend_title="Года")
        return fig
    except:
        fig=px.bar(width=650, height=650)
        fig=fig_setting(fig)
        fig.update_layout(xaxis_title="Предприятия",yaxis_title=label_y,legend_title="Года")
        return fig   

path_json='counties.txt'

def pic7(df,path_json=path_json):
    try:
        with open(path_json, 'r') as fp:
            counties  = json.load(fp)    

        JSON_NAMES=[i['properties']['name'] for i in counties['features']]    
        def region_cleaning(column):
            if column=='Архангельская область (кроме Ненецкого АО)':
                return 'Архангельская область'
            elif column=='Город Москва':
                return 'Москва'
            elif column=='Город Санкт-Петербург':
                return 'Санкт-Петербург'
            elif column=='Чувашская Республика':
                return 'Республика Чувашия'
            elif column=='Республика Северная Осетия-Алания':
                return 'Республика Северная Осетия — Алания'
            elif column=='Ханты-Мансийский автономный округ':
                return 'Ханты-Мансийский АО'
            elif column=='Тюменская область (кроме Ханты-Мансийского АО - Югры и Ямало-Ненецкого АО)':
                return 'Тюменская область'
            else:
                return column

        df['регион']=df['регион'].apply(lambda x:region_cleaning(x))
        df=df[df['регион'].isin(JSON_NAMES)]
        df=df.groupby(['регион','Год','тип производства'], as_index=False)['величина'].sum()
#     df=df[df['тип производства'].isin(type_man)]
#     df=df.groupby(['регион','Год'], as_index=False)['величина'].sum()
        fig = px.choropleth_mapbox(df,geojson=counties,locations='регион',color="величина",featureidkey="properties.name",
        center={"lat": 64.461428, "lon": 89.941743},mapbox_style="open-street-map",opacity=0.5,color_continuous_scale="Viridis", 
        zoom=1.4,animation_frame='Год',color_discrete_sequence=px.colors.qualitative.Light24)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig=fig_setting(fig)
        fig['layout']['coloraxis']['colorbar']['title']['text']='Индекс производства'
        return fig    
    except:
        fig = px.choropleth_mapbox()
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig=fig_setting(fig)
    
    
path='rosstat/2015-2020.xlsx'  

def rosstat_prepare(path=path):
    names=['регион']
    a=pd.read_excel(path,header=[1,2])
    for i in a.columns[1:]:
        name=i[0]+' '+str(i[1]).split(' ')[0]
        names.append(name)
    a.columns=names  
    for r,i in enumerate(a.columns[1:]):
        if r==0:
            df=a[['регион',i]]
            new_name=i.split(' ')[:-1]
            year=int(i.split(' ')[-1])
            new_name=' '.join(new_name)
            df=df.copy()
            df.columns=['регион','величина']
            df.loc[:,'Год']=year
            df.loc[:,'тип производства']=new_name
            df.drop(df.tail(5).index,inplace=True)
        else:
            df_new=a[['регион',i]]
            new_name=i.split(' ')[:-1]
            year=int(i.split(' ')[-1])
            new_name=' '.join(new_name)
            df_new=df_new.copy()
            df_new.columns=['регион','величина']
            df_new.loc[:,'Год']=year
            df_new.loc[:,'тип производства']=new_name
            df_new.drop(df_new.tail(5).index,inplace=True)
            df=pd.concat([df,df_new],axis=0)
    df.loc[:,'тип производства']=df.loc[:,'тип производства'].apply(lambda x: 'Промышленное производство' if x=='Промышленное производство1' else x)   
    df.loc[:,'величина']=pd.to_numeric(df['величина'], errors='coerce')  
    df = df.dropna(subset=['величина'])
    df.loc[:,'величина'] = df['величина'].astype('float')
    return df  