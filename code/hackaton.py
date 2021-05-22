import pandas as pd
import base64
import io
import const
import functions
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
from dash.dependencies import Input, Output, State
pd.options.display.max_rows=1000 


df_rosstat = functions.rosstat_prepare()
fig7 = functions.pic7(df_rosstat)

app = dash.Dash(__name__)
server = app.server

app.title = const.title
auth = dash_auth.BasicAuth(app,const.VALID_USERNAME_PASSWORD_PAIRS)


app.layout = html.Div([
    html.Div([
        html.Div(html.Img(src=app.get_asset_url('logo.png'),style={'height':'90%','margin-top':'2%'}),
            style={'width':'10%','height':'100%','display': 'inline-block','vertical-align': 'middle'}),
        html.Div(html.H1("Министерство промышленности, энергетики и инноваций Республики Башкортостан",
            style={'font-size': '180%','color': 'rgba(0,0,0,0.6)','text-shadow': '2px 2px 3px rgba(255,255,255,0.1)'}),
                style={'width':'80%','height':'100%','display': 'inline-block','vertical-align': 'middle'}),
    ],style={'width': '90%','height':'100px','margin':'20px auto auto auto'}),
    
    html.Div([
        html.Div(
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='О нас', value='tab-1',className='custom-tab',),
        dcc.Tab(label='Дашборд', value='tab-2',className='custom-tab',),
        dcc.Tab(label='Форма онлайн', value='tab-3',className='custom-tab',),
        dcc.Tab(label='Загрузить', value='tab-4',className='custom-tab',),
    ]),style={'width':'100%','text-shadow': '2px 8px 6px rgba(0,0,0,0.2) 0px -5px 35px rgba(255,255,255,0.3)'}),
        
        html.Div(id='tabs-example-content'
                 ,style={'background-image': 'linear-gradient(to top, #09203f 0%, #537895 100%)',
                                'border-bottom-left-radius': '10px', 'border-bottom-right-radius': '10px',
                                'box-shadow': 'rgba(0, 0, 0, 0.3) 0px 19px 38px, rgba(0, 0, 0, 0.22) 0px 15px 12px'}
                )],
        
        style={'width':'90%','margin':'0 auto 30px auto'})
])

@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3(const.about_us, style={'width':'45%', 'padding':'0 0 0 20px','display': 'inline-block','vertical-align': 'top','font-size':'20px','color': 'white'}),
            html.Div(html.Img(src=app.get_asset_url('scale_1200.webp'),style={'width':'95%'}),
            style={'width':'45%','height':'40px','display': 'inline-block','vertical-align': 'top','padding':'20px'})])
    
    elif tab == 'tab-2':
        return html.Div([    
#1 pic
            html.Div([
                html.Div([
                    html.H3('Объемы производства предприятий РБ в натуральном выражении',style=const.tab2_h),
                    html.Label('Выберите месяц (один и более)',style=const.tab2_label),
                    html.Div(dcc.Checklist(id = 'pic1-month',options=const.tab2_months,
                        value=['январь'],
                        labelStyle=const.tab2_checklist,),
                        style=const.tab2_div_check),                   
                    html.Label('Тип отчетного периода',style=const.tab2_label),
                    html.Div(dcc.Dropdown(id = 'pic1-period',options=const.tab2_periods,
                        value='Отчетный период прошлого года (В натуральном выражении)',
                        style=const.tab2_drop),style=const.tab2_div_drop),
                    html.Label('Год',style=const.tab2_label),
                    html.Div(dcc.Dropdown(id="pic1-year",
                        options=const.tab2_years,
                        value=2020,style=const.tab2_drop),style=const.tab2_div_drop)],
                    style=const.tab2_left),
                html.Div(
                    dcc.Graph(id = 'pic1',
                    figure = functions.pic1(['январь'],functions.get_dataset(),'Отчетный месяц прошлого года (В натуральном выражении)',2020),
                    style=const.tab2_graph),
                    style=const.tab2_right)
            ],style=const.tab2_each_block),           
#2 pic
            html.Div([
                html.Div([
                    html.H3('Индекс промышленного производства',style=const.tab2_h),
                    html.Label('Отношение',style=const.tab2_label),
                    html.Div(dcc.Dropdown(id="pic2-relat",options=[  
                        {'label': 'Отношение периодов, %', 'value': 'Отношение периодов, %'},
                        {'label': 'Отношение месяцев, %', 'value': 'Отношение месяцев, %'}],
                        value='Отношение периодов, %',style=const.tab2_drop),style=const.tab2_div_drop),    
                    html.Label('Выберите года',style=const.tab2_label),
                    html.Div(dcc.Checklist(id = 'pic2-years',options=const.tab2_years,
                        value=[2020],labelStyle=const.tab2_checklist,),style=const.tab2_div_check),    
                    html.Label('Выберите предприятие',style=const.tab2_label),
                    html.Div(dcc.Dropdown(id="pic2-slider",options=functions.get_man(functions.get_dataset()),
                        value=functions.man_value(),
                    style=const.tab2_drop),style=const.tab2_div_drop)],
                style=const.tab2_left),
                html.Div(      
                    dcc.Graph(id = 'pic2',
                    figure = functions.pic2(functions.get_dataset(),'Предприятие 1','Отношение периодов, %',[2020]),
                    style=const.tab2_graph),
                style=const.tab2_right)],
            style=const.tab2_each_block),                     
#3 pic
            html.Div([
                html.Div([
                    html.H3('Индекс промышленного производства',style=const.tab2_h),
                    html.Label('Тип отчетного периода',style=const.tab2_label),
                    html.Div(dcc.Dropdown(id = 'pic3-period',options=const.tab2_periods,
                        value='Отчетный период прошлого года (В натуральном выражении)',
                        style=const.tab2_drop),style=const.tab2_div_drop),       
                    html.Label('Выберите года',style=const.tab2_label),
                    html.Div(dcc.Checklist(id = 'pic3-years',options=const.tab2_years,
                        value=[2020],
                        labelStyle=const.tab2_checklist,),
                        style=const.tab2_div_check),
                    html.Label('Вид деятельности/ОКВЭД',style=const.tab2_label),
                    html.Div(dcc.Dropdown(id="pic3-stat",options=[  
                        {'label': 'Вид деятельности', 'value': 'Вид деятельности'},
                        {'label': 'ОКВЭД', 'value': 'ОКВЭД'}],
                        value='Вид деятельности',style=const.tab2_drop),style=const.tab2_div_drop),
                ],style=const.tab2_left),
                html.Div(      
                    dcc.Graph(id = 'pic3',
                    figure = functions.pic3(functions.get_dataset(),[2020],'Отчетный период прошлого года (В натуральном выражении)','Вид деятельности'),
                    style=const.tab2_graph)
                ,style=const.tab2_right)
            ],style=const.tab2_each_block),                
#4 pic
            html.Div([
                html.Div([
                    html.H3('Индекс промышленного производства',style=const.tab2_h),
                    html.Label('Тип отчетного периода',style=const.tab2_label),
                    html.Div(dcc.Dropdown(id = 'pic4-period',options=const.tab2_periods,
                        value='Отчетный период прошлого года (В натуральном выражении)',
                        style=const.tab2_drop),style=const.tab2_div_drop),          
                    html.Label('Месяца (один и более)',style=const.tab2_label),
                    html.Div(dcc.Checklist(id = 'pic4-month',options=const.tab2_months,
                        value=['январь'],
                        labelStyle=const.tab2_checklist,),
                        style=const.tab2_div_check),
                    html.Label('Вид деятельности/ОКВЭД',style=const.tab2_label),
                    html.Div(dcc.Dropdown(id="pic4-stat",options=[  
                        {'label': 'Вид деятельности', 'value': 'Вид деятельности'},
                        {'label': 'ОКВЭД', 'value': 'ОКВЭД'}],
                        value='Вид деятельности',style=const.tab2_drop),style=const.tab2_div_drop),],
                style=const.tab2_left),
                html.Div(      
                    dcc.Graph(id = 'pic4',
                    figure = functions.pic3(functions.get_dataset(),[2020],'Отчетный период прошлого года (В натуральном выражении)','Вид деятельности'),
                    style=const.tab2_graph),
                style=const.tab2_right)],
            style=const.tab2_each_block),
# 5 pic            
            html.Div([
                html.Div([
                    html.H3('Индекс промышленного производства по регионам',style=const.tab2_h),
                    html.Label('Выберите регион (один и более)',style=const.tab2_label),
                    html.Div(dcc.Checklist(id = 'rosstat-reg',options=const.tab2_rosstat_reg,
                        value=['Республика Башкортостан','Республика Татарстан'],
                        labelStyle=const.tab2_checklist,),
                        style=const.tab2_div_check), 
                    html.Label('Выберите ОКВЭД',style=const.tab2_label),            
                    html.Div(dcc.Dropdown(id="rosstat-man-type",options=const.tab2_rosstat_man,
                        value='Обрабатывающие производства',style=const.tab2_drop),style=const.tab2_div_drop)],
                style=const.tab2_left),
                html.Div(      
                    dcc.Graph(
                    id = 'pic5',
                    figure = functions.pic5(df_rosstat,['Республика Башкортостан','Республика Татарстан'],'Обрабатывающие производства'),
                    style=const.tab2_graph)
                ,style=const.tab2_right)],
            style=const.tab2_each_block),
# 7 pic            
            html.Div([
                html.Div([
                    html.H3('Тепловая карта',style=const.tab2_h)],
                style=const.tab2_left),
                html.Div(      
                    dcc.Graph(id = 'pic7',
                    figure = fig7,
                    style=const.tab2_graph)
                ,style=const.tab2_each_block)],
            style=const.tab2_each_block)],                   
        style=const.tab2_each_block)
    elif tab == 'tab-3':
        return html.Div([
            html.Div(
                [html.H3('Онлайн форма',style=const.tab3_h),
                html.H3('На этой странице, каждое предприятие может подать отчет онлайн, заполнив форму',style=const.tab3_label)]
            ,style=const.tab3_each_block),           
# 1 half            
            html.Div(
                [html.Label('Наименование предприятия',style=const.tab3_label_form),
                html.Div(dcc.Input(id="f1",placeholder="Наименование предприятия",style=const.tab3_drop),style=const.tab3_div_drop),
                html.Label('Выберите ОКВЭД',style=const.tab3_label_form),
                html.Div(dcc.Dropdown(id="f2",options=const.tab2_rosstat_man,
                    value='Обрабатывающие производства',style=const.tab3_drop),style=const.tab3_div_drop),
                html.Label('Выберите вид деятельности',style=const.tab3_label_form),
                html.Div(dcc.Dropdown(id="f3",options=functions.get_label_activity(),
                    value=functions.get_label_activity()[0]['value'],style=const.tab3_drop),style=const.tab3_div_drop),         
                html.Label('Отчетный период прошлого года (В натуральном выражении)',style=const.tab3_label_form),
                html.Div(dcc.Input(id="f4",placeholder="Отчетный период прошлого года (В натуральном выражении)",style=const.tab3_drop),style=const.tab3_div_drop), 
                html.Label('Отчетный период прошлого года (В стоимостном выражении)',style=const.tab3_label_form),
                html.Div(dcc.Input(id="f5",placeholder="Отчетный период прошлого года (В стоимостном выражении)",style=const.tab3_drop),style=const.tab3_div_drop), 
                html.Label('Отчетный период текущего года (В натуральном выражении)',style=const.tab3_label_form),
                html.Div(dcc.Input(id="f6",placeholder="Отчетный период текущего года (В натуральном выражении)",style=const.tab3_drop),style=const.tab3_div_drop),
                html.Label('Отчетный период текущего года (В стоимостном выражении)',style=const.tab3_label_form),
                html.Div(dcc.Input(id="f7",placeholder="Отчетный период текущего года (В стоимостном выражении)",style=const.tab3_drop),style=const.tab3_div_drop),]
            ,style=const.tab3_half),
# 2 half          
            html.Div([
                html.Label('Отчетный месяц прошлого года (В натуральном выражении)',style=const.tab3_label_form),
                html.Div(dcc.Input(id="f8",placeholder="Отчетный месяц прошлого года (В натуральном выражении)",style=const.tab3_drop),style=const.tab3_div_drop), 
                html.Label('Отчетный месяц прошлого года (В стоимостном выражении)',style=const.tab3_label_form),
                html.Div(dcc.Input(id="f9",placeholder="Отчетный месяц прошлого года (В стоимостном выражении)",style=const.tab3_drop),style=const.tab3_div_drop),   
                html.Label('Отчетный месяц текущего года (В натуральном выражении)',style=const.tab3_label_form),
                html.Div(dcc.Input(id="f10",placeholder="Отчетный месяц текущего года (В натуральном выражении)",style=const.tab3_drop),style=const.tab3_div_drop), 
                html.Label('Отчетный месяц текущего года (В стоимостном выражении)',style=const.tab3_label_form),
                html.Div(dcc.Input(id="f11",placeholder="Отчетный месяц текущего года (В стоимостном выражении)",style=const.tab3_drop),style=const.tab3_div_drop),
                html.Label('Месяц',style=const.tab3_label_form),
                html.Div(dcc.Dropdown(id="f12",options=const.tab2_months, value='январь',style=const.tab3_drop),style=const.tab3_div_drop),
                html.Label('Год',style=const.tab3_label_form),
                html.Div(dcc.Dropdown(id="f13",options=const.tab2_years, value=2020,style=const.tab3_drop),style=const.tab3_div_drop),
                html.Div(html.Button('Подать форму', id='fsubmit', n_clicks=0,style=const.button),style=const.tab3_button),
                html.Div(id='f14',style=const.alert)
            ],style=const.tab3_half)       
        ],style=const.tab3_each_block)          
    elif tab == 'tab-4':
        return html.Div([
            html.Div([
                html.H3('Форма загрузки файла',style=const.tab4_h),
                html.H3('Страница для загрузки данных по форме 36 в формате xlsx',style=const.tab4_label),
                html.Label('Выберите год',style=const.tab4_label_form),
                html.Div(dcc.Dropdown(id="tab4-f0",options=const.tab2_years, value=2020,style=const.tab4_drop),style=const.tab4_div_drop),
                dcc.Upload(id='upload-data',children=
                    html.Div(['Перетащите или ',html.A('выберите файл')],style=const.tab4_drop),style=const.tab4_div_drop,
                multiple=False),
                html.Div(id='tab4-output1', style=const.alert),
                html.Div(html.Button('Отправить файл', id='tab4-fsubmit', n_clicks=0,style=const.button),style=const.tab4_button),
                html.Div(id='tab4-output2', style=const.alert),
            ],style=const.tab4_half_l),
            html.Div([
                html.Div([
                    html.H3('Анализ предприятий с пустыми значениями в отчете',style=const.tab4_h),
                    html.Div(
                        html.Label('Выберите месяц (один и более)',style=const.tab4_label),
                    style={'width':'35%','display': 'inline-block','textAlign': 'center','vertical-align': 'top'}),
                    html.Div(
                        html.Label('Выберите года',style=const.tab4_label),
                    style={'width':'33%','display': 'inline-block','textAlign': 'center','vertical-align': 'top'}),
                    html.Div(
                        html.Label('Количество',style=const.tab4_label),
                    style={'width':'31%','display': 'inline-block','textAlign': 'center','vertical-align': 'top'}),
                    html.Div(
                        html.Div(dcc.Checklist(id = 'tab4-f1',options=const.tab2_months,
                        value=['январь'],
                        labelStyle=const.tab4_checklist,),
                        style=const.tab4_div_check),
                    style={'width':'35%','display': 'inline-block','textAlign': 'center','vertical-align': 'top'}),
                    html.Div(
                        html.Div(dcc.Checklist(id = 'tab4-f2',options=const.tab2_years,
                        value=[2020],labelStyle=const.tab4_checklist,),style=const.tab4_div_check),
                    style={'width':'33%','display': 'inline-block','textAlign': 'center','vertical-align': 'top'}),
                    html.Div(
                        html.Div(dcc.RadioItems(id = 'tab4-f3',options=[{'label': 'Количество nan', 'value': True},
        {'label': 'Отчеты с nan', 'value': False},],
                        value=True,labelStyle={'width': '100%','textAlign': 'left','display': 'inline-block','color': 'white','font-size':'18px','vertical-align': 'top'},),style=const.tab4_div_check),
                    style={'width':'31%','display': 'inline-block','textAlign': 'center','vertical-align': 'top'}), 
                ],
                style=const.tab4_each_block),
            html.Div(
                dcc.Graph(id = 'pic6',
                    figure = functions.pic6(functions.get_dataset(),['январь','февраль'],[2020],each=True),
                    style=const.tab2_graph))   
            ],style=const.tab4_half_r),
        ],style=const.tab4_each_block)
 

@app.callback(
    Output("pic1", "figure"), 
    [Input("pic1-month", "value"),Input("pic1-period", "value"),Input("pic1-year", "value")],)    
def update_charts1(months,period,year):
    return functions.pic1(months,functions.get_dataset(),period,year)

@app.callback(
    Output("pic2", "figure"), 
    [Input("pic2-slider", "value"),Input("pic2-relat", "value"),Input("pic2-years", "value")])    
def update_charts2(man,relat,years):
    return functions.pic2(functions.get_dataset(),man,relat,years)    
    
@app.callback(
    Output("pic3", "figure"), 
    [Input("pic3-years", "value"),Input("pic3-period", "value"),Input("pic3-stat", "value")])    
def update_charts3(years,period,stat):
    return functions.pic3(functions.get_dataset(),years,period,stat)     
    
@app.callback(
    Output("pic4", "figure"), 
    [Input("pic4-month", "value"),Input("pic4-period", "value"),Input("pic4-stat", "value")])    
def update_charts4(months,period,stat):
    return functions.pic4(functions.get_dataset(),months,period,stat)
  
@app.callback(
    Output("pic5", "figure"), 
    [Input("rosstat-reg", "value"),Input("rosstat-man-type", "value")])    
def update_charts5(regions,man_type):
    return functions.pic5(df_rosstat,regions,man_type)    

@app.callback(
    Output("pic6", "figure"), 
    [Input("tab4-f1", "value"),Input("tab4-f2", "value"),Input("tab4-f3", "value")])    
def update_charts6(months,years,each):
    return functions.pic6(functions.get_dataset(),months,years,each=each)  

@app.callback(
    Output('f14', 'children'),
    [Input('fsubmit', 'n_clicks')],
    [State('f1', 'value'),State('f2', 'value'),State('f3', 'value'),State('f4', 'value'),State('f5', 'value'),
     State('f6', 'value'),State('f7', 'value'),State('f8', 'value'),State('f9', 'value'),State('f10', 'value'),
     State('f11', 'value'),State('f12', 'value'),State('f13', 'value'),])    
def buttom(cl,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13):
    if cl==0:
        return html.P('', style={'color':'red'})
    else:
        if all([f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13]):
            try:
                f4, f5, f6, f7, f8,f9,f10,f11 = float(f4),float(f5), float(f6), float(f7), float(f8), float(f9), float(f10), float(f11)
                df=pd.DataFrame([[999,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13]],columns=functions.online_columns)
                df['Отношение периодов, %']=(df['Отчетный период текущего года (В натуральном выражении)']/df['Отчетный период прошлого года (В натуральном выражении)'])*100
                df['Отношение месяцев, %']=(df['Отчетный месяц текущего года (В натуральном выражении)']/df['Отчетный месяц прошлого года (В натуральном выражении)'])*100
                df_old=functions.get_dataset()
                df=pd.concat([df_old,df])
                df=df.drop_duplicates()
                df.to_csv('dataset/result_df.csv',index=False)
                return html.P('Анкета загружена')
            except:
                return html.P('Проверьте правильность заполнения. Используйте точку для разделения дробной части')
        else:
            return html.P('Заполните все поля')

@app.callback(Output('tab4-output1', 'children'),
              [Input('upload-data', 'filename')])
def print_file(filename):
    if filename is None:
        return html.P('')
    else:
        return html.P('Файл {} загружен'.format(filename))
 
@app.callback(Output('tab4-output2', 'children'),
              [Input('tab4-fsubmit', 'n_clicks')],
              [State('upload-data', 'filename'),State('upload-data', 'contents'),State('tab4-f0', "value")])
def update_output(cl,filename,contents,year):
    if cl==0:
        return html.P('')
    if filename is None :
        return html.P('Загрузите файл')
    try:
        ras=filename.split('.')[-1]
        if ras!='xlsx':
            return html.P('Неправильный формат, нужен xlsx')
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.ExcelFile(io.BytesIO(decoded))
        df=functions.prepare_form(df,year)
        var=df[df['№'].notnull()]
        nan=sum(var.iloc[:,1:].isnull().sum().values)        
        df_old=functions.get_dataset()   
        a=len(set(df_old.columns))
        b=len(set(df.columns))
        if a-b==0:
            df=pd.concat([df_old,df])
            df=df.drop_duplicates()
            df.to_csv('dataset/result_df.csv',index=False)
            if nan>0:
                return html.P('Файл {} принят, но в файле есть пропуски'.format(filename))
            else:
                return html.P('Файл {} принят'.format(filename))
        else:
            raise Exception
    except:
        return html.P('Неправильная форма')        

# if __name__ == "__main__":
#     app.run_server(host = '127.0.0.1')
if __name__ == "__main__":
    app.run_server(host = '127.0.0.1',debug=True)





