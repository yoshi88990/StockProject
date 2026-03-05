import win32com.client
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
excel = win32com.client.Dispatch("Excel.Application")
try:
    wb = excel.Workbooks.Open(os.path.abspath(r"111\週間工程表_260210.xlsx"), UpdateLinks=0, ReadOnly=True)
    ws = wb.Worksheets(1)
    
    for s in ws.Shapes:
        txt = ""
        try:
            if s.TextFrame2.HasText: txt = s.TextFrame2.TextRange.Text
            elif s.TextFrame.HasText: txt = s.TextFrame.Characters().Text
        except: pass
        if "テレ台" in txt or "脚回り足場組立" in txt:
            print(f"Text [{txt.strip()}] -> Row: {s.TopLeftCell.Row}, Col: {s.TopLeftCell.Column}")
finally:
    excel.Quit()
