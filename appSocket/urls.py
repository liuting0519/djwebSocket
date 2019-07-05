from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^websoket_g2/', views.websocket_g2),
    url(r'^echo_two', views.echo_two),
    url(r'^port_number', views.port_number),
    url(r'^open_serial_1', views.open_serial_1),
    url(r'^close_serial_1', views.close_serial_1),
    url(r'^open_serial_2', views.open_serial_2),
    url(r'^close_serial_2', views.close_serial_2),
    url(r'^stop', views.stop)
]