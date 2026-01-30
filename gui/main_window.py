import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
import pyqtgraph as pg
from PySide6.QtCore import QTimer

df = pd.read_excel("telemetryData.xlsx")

index = 0
window_size = 300 



speed = df["speed"].values
steer = df["steer"].values
throttle = df["throttle"].values
brake = df["brake"].values
drs = df["drs"].values
gear = df["gear"].values


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Telemetry Dashboard")
window.resize(1200, 800)

layout = QGridLayout(window)

def create_plot(title, row, col, color='w'):
    plot = pg.PlotWidget(title=title)
    plot.showGrid(x=True, y=True)

    if title == 'Throttle and Brake':
        throttle_curve = plot.plot([], pen='g')
        brake_curve = plot.plot([], pen='r')
        layout.addWidget(plot, row, col, 1, 2)

        return throttle_curve, brake_curve

    curve = plot.plot([], pen=color)
    layout.addWidget(plot, row, col)
    return curve


speed_curve = create_plot("Speed (km/h)", 0, 0)
steer_curve = create_plot("Steer", 0, 1)
throttle_curve, brake_curve = create_plot("Throttle and Brake", 1, 0)

drs_container = QWidget()
drs_layout = QHBoxLayout(drs_container)
drs_layout.setSpacing(10)
drs_layout.setContentsMargins(0, 0, 0, 0)

drs_label = QLabel(f"DRS")
drs_label.setStyleSheet("""
    QLabel{
        color: white;
        font-size: 18px;
        font-weight: bold
    }
""")

drs_indicator = QLabel()
drs_indicator.setFixedSize(20, 20)
drs_indicator.setStyleSheet("""
    QLabel {
        background-color: #ff0000;
        border-radius: 8px;
    }
""")

drs_glow = QGraphicsDropShadowEffect()
drs_glow.setBlurRadius(20)
drs_glow.setOffset(0, 0)
drs_glow.setColor(QColor(255, 0, 0))

drs_indicator.setGraphicsEffect(drs_glow)

drs_layout.addWidget(drs_label)
drs_layout.addWidget(drs_indicator)

gear_container = QWidget()
gear_layout = QHBoxLayout(gear_container)
gear_layout.setSpacing(30)
gear_layout.setContentsMargins(0, 0, 0, 0)

gear_label = QLabel("GEAR: ")
gear_label.setStyleSheet("""
    QLabel{
        color: white;
        font-size: 18px;
        font-weight: bold
    }
""")

gear_layout.addWidget(gear_label)

bottom_panel_left = QWidget()
bottom_panel_left.setStyleSheet("""
    QWidget{
        background-color: #000;
        border-radius: 4px
    }
""")
bottom_layout_left = QGridLayout(bottom_panel_left)
bottom_layout_left.setSpacing(30)
bottom_layout_left.setContentsMargins(20, 15, 20, 15)

bottom_panel_right = QWidget()
bottom_panel_right.setStyleSheet("""
    QWidget{
        background-color: #000;
        border-radius: 4px
    }
""")
bottom_layout_right = QGridLayout(bottom_panel_right)
bottom_layout_right.setSpacing(30)
bottom_layout_right.setContentsMargins(20, 15, 20, 15)


bottom_layout_left.addWidget(drs_container, 0, 0, 1, 1)
bottom_layout_left.addWidget(gear_container, 1, 0, 1, 1)
layout.addWidget(bottom_panel_left, 2, 0, 1, 1)
layout.addWidget(bottom_panel_right, 2, 1, 1, 1)



def update():
    global index

    if index >= len(speed):
        timer.stop()
        return

    start = 0

    speed_curve.setData(speed[start:index])
    steer_curve.setData(steer[start:index])
    throttle_curve.setData(throttle[start:index])
    brake_curve.setData(brake[start:index])

    if gear > 1:
        gear_label.setText(f"GEAR: {gear[index]}")
    elif gear < 0:
        gear_label.setText(f"GEAR: R")
    else:
        gear_label.setText(f"GEAR: N")

    drs_value = "ENABLED" if drs[index] == 1 else "DISABLED"

    if drs[index] == 1:
        drs_value = "ENABLED"
        drs_indicator.setStyleSheet("""
            QLabel {
                background-color: #00ff00;
                border-radius: 10px;
            }
        """)
        drs_glow.setColor(QColor(0, 255, 0))
        drs_glow.setBlurRadius(25)
    else:
        drs_value = "DISABLED"
        drs_indicator.setStyleSheet("""
        QLabel {
                background-color: #ff0000;
                border-radius: 10px;
            }
        """)
        drs_glow.setColor(QColor(255, 0, 0))
        drs_glow.setBlurRadius(15)

    drs_label.setText(f"DRS: {drs_value}")
    

    index += 1

    
timer = QTimer()
timer.timeout.connect(update)
timer.start(16)  # ~60 FPS (16 ms)




window.show()
sys.exit(app.exec())