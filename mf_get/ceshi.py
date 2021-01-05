import plotly as py
# import plotly.graph_objs as go

pyplt = py.offline.plot
# labels = ['产品1','产品2','产品3','产品4','产品5']
# values = [38.7,15.33,19.9,8.6,17.47]
# trace = [go.Pie(labels=labels, values=values)]
# layout = go.Layout(
#     title = '产品比例配比图',
# )
# fig = go.Figure(data = trace, layout = layout)
# pyplt(fig, filename='1.html')


import plotly.express as px
base_list = []
for i in range(277):
    base_list.append(50)
data_list = [x for x in range(255)] + [0,0,0,0,0,0,0,0,0,0,0,0,0,0] + [100,100,100,100,100,100,100,1]
print(data_list)
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Barpolar(r=base_list,name='c',marker_color='RGB(255,255,255)'))
fig.add_trace(go.Barpolar(r=data_list,name='A',marker_color='RGB(0,123,253)'))
# fig.add_trace(go.Barpolar(r=data_list,name='B',marker_color='RGB(100,123,253)'))
fig.update_traces(text=['A', 'B', 'C', 'D', 'E', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q'])
fig.update_layout(title='A Test',
    #font_size=16,
    legend_font_size=16,
    # polar_radialaxis_ticksuffix='%',
    polar_angularaxis_rotation=90,
)
# fig.show()
pyplt(fig, filename='1.html')