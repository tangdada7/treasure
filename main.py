#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/9/20 下午1:20
# @Author : MiuziZhou
from statistics import LinearRegression

import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
from sklearn.linear_model import LinearRegression


# 读取并清洗房屋数据
def load_and_clean_data(file_path):
    data = pd.read_excel(file_path)
    data_cleaned = data.dropna(subset=['总价', '平方米', '小区名称'])
    data_cleaned.loc[:, '总价'] = data_cleaned['总价'].str.replace('万', '').astype(float)
    data_cleaned.loc[:, '平方米'] = data_cleaned['平方米'].str.replace('平米', '').astype(float)
    return data_cleaned


# 创建Dash应用，添加线性回归曲线及其系数表格
def create_app_with_regression(data_cleaned):
    app = Dash(__name__)
    app.layout = html.Div([
        html.H1("房屋价格预测", style={'text-align': 'center', 'padding': '20px'}),
        html.Div([
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in data_cleaned['小区名称'].unique()],
                value=data_cleaned['小区名称'].unique()[0],
                style={'width': '40%', 'height': '50px', 'margin-right': '5px'}
            ),
            dcc.Input(
                id="area-input",
                type="number",
                placeholder="输入房屋面积（平方米）",
                style={'width': '10%', 'height': '50px', 'margin-left': '5px'}
            ),
            html.Button('预测价格', id='predict-button', n_clicks=0,
                        style={'width': '10%', 'height': '50px', 'margin-left': '5px'})
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
        html.Div(id='predicted-price', style={'margin-top': '20px', 'font-size': '20px'}),
        dcc.Graph(id='price-graph', style={'height': '600px'}),
        html.H2("回归模型详情", style={'padding': '20px'}),
        html.Div(id='regression-details')
    ])

    @app.callback(
        Output('predicted-price', 'children'),
        Output('price-graph', 'figure'),
        Output('regression-details', 'children'),
        Input('predict-button', 'n_clicks'),
        State('region-dropdown', 'value'),
        State('area-input', 'value')
    )
    def update_output(n_clicks, region, area):
        X = data_cleaned['平方米'].values.reshape(-1, 1)
        y = data_cleaned['总价'].values
        reg = LinearRegression().fit(X, y)
        predictions = reg.predict(X)
        fig = px.scatter(data_cleaned, x='平方米', y='总价', color='小区名称', title='所有小区房屋面积与价格关系')
        fig.add_scatter(x=data_cleaned['平方米'], y=predictions, mode='lines', name='总体回归线',
                        line=dict(color='red'))

        # 创建回归模型详情表格
        model_details = html.Table([
            html.Tr([html.Td("斜率"), html.Td(f"{reg.coef_[0]:.2f}")]),
            html.Tr([html.Td("截距"), html.Td(f"{reg.intercept_:.2f}")])
        ], style={'width': '100%', 'text-align': 'left', 'padding': '10px'})

        if n_clicks > 0 and region and area:
            region_data = data_cleaned[data_cleaned['小区名称'] == region]
            region_X = np.array([[float(area)]])
            region_prediction = reg.predict(region_X)[0]
            price_display = f"预测价格：{region_prediction:.2f} 万元"
            fig.add_scatter(x=region_X.flatten(), y=[region_prediction], mode='markers',
                            marker=dict(color='black', size=12), name='你的预测')
            return price_display, fig, model_details
        return "", fig, model_details

    return app


# 主函数，整合数据并运行应用
def main_with_regression():
    house_data_path = '小区房屋信息.xlsx'
    data_cleaned = load_and_clean_data(house_data_path)
    app = create_app_with_regression(data_cleaned)
    app.run_server(debug=True)


if __name__ == '__main__':
    main_with_regression()



