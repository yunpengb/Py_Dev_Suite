# -*- coding: utf-8 -*-


import win32com.client
import time

s = win32com.client.Dispatch("SAPI.SpVoice")

#ab = s.GetVoice()

s.Speak(r'hello world��� ���ٵ����ζ����')
time.sleep(2)