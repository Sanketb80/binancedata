from django.urls import path
from .views import get_data,get_data1,get_data2,get_data_twohr,get_data_1hr,get_data3,one_hr,four_hr,one_day

urlpatterns = [
    
    path('get_data1/', get_data1, name='get-data1'),
    path('get_data2/', get_data2, name='get-data4'),
    path('get_data_4hr/',get_data_twohr,name='4hr'),
    path('get_data3/',get_data3, name='get-data3'),
    path('get_data_1hr/',get_data_1hr, name='1hr'),
    path('get_data_4hr/',get_data_twohr,name='4hr'),
    path('get_data_24hr/', get_data, name='get-data'),
    path('chart_1hr/',one_hr,name='one_hr'),
    path('chart_4hr/',four_hr,name='four_hr'),
    path('chart_24hr/',one_day,name='one_day'),
]