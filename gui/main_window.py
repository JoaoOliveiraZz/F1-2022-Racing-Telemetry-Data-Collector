import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QHBoxLayout
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

# drs_value = 'DISABLED'
# drs_label = QLabel(f"DRS: {drs_value}")
# drs_label.setStyleSheet("""
#     QLabel{
#         color: white;
#         font-size: 18px;
#         font-weight: bold
#     }
# """)
# layout.addWidget(drs_label, 2, 1, 1, 2)

bottom_panel = QWidget()
bottom_panel.setStyleSheet("""
    QWidget{
        background-color: #000;
        border-radius: 4px
    }
""")
bottom_layout = QHBoxLayout(bottom_panel)
bottom_layout.setSpacing(30)
bottom_layout.setContentsMargins(20, 15, 20, 15)

layout.addWidget(bottom_panel, 2, 0, 1, 2)



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

    drs_value = "ENABLED" if drs[index] == 1 else "DISABLED"

    # drs_label.setText(f"DRS: {drs_value}")

    index += 1

    
timer = QTimer()
timer.timeout.connect(update)
timer.start(16)  # ~60 FPS (16 ms)




window.show()
sys.exit(app.exec())