import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
import pyqtgraph as pg
from PySide6.QtCore import QTimer, Qt


df = pd.read_excel("telemetryData.xlsx")

index = 0
window_size = 300 

def svg_to_pixmap(path, size=24, color=None):
    renderer = QSvgRenderer(path)
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    renderer.render(painter)

    if color:
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)

    painter.end()

    return pixmap

speed = df["speed"].values
steer = df["steer"].values
throttle = df["throttle"].values
brake = df["brake"].values
drs = df["drs"].values
gear = df["gear"].values
fl_brakes = df["breakTemperatureFL"].values
fr_brakes = df["breakTemperatureFR"].values
rl_brakes = df["breakTemperatureRL"].values
rr_brakes = df["breakTemperatureRR"].values


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
        border-radius: 10px;
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
bottom_layout_right.setSpacing(2)
bottom_layout_right.setContentsMargins(20, 15, 20, 15)


bottom_layout_left.addWidget(drs_container, 0, 0, 1, 1)
bottom_layout_left.addWidget(gear_container, 1, 0, 1, 1)


fl_brake_icon = QLabel()
fl_brake_icon.setPixmap(svg_to_pixmap("./icons/brake_svg.svg",24, QColor(0, 255, 0)))
fl_brake_temperature = QLabel("100°")

fr_brake_icon = QLabel()
fr_brake_icon.setPixmap(svg_to_pixmap("./icons/brake_svg.svg",24, QColor(0, 255, 0)))
fr_brake_temperature = QLabel("100°")

rl_brake_icon = QLabel()
rl_brake_icon.setPixmap(svg_to_pixmap("./icons/brake_svg.svg",24, QColor(0, 255, 0)))
rl_brake_temperature = QLabel("100°")

rr_brake_icon = QLabel()
rr_brake_icon.setPixmap(svg_to_pixmap("./icons/brake_svg.svg",24, QColor(0, 255, 0)))
rr_brake_temperature = QLabel("100°")

bottom_layout_right.addWidget(fl_brake_icon, 0, 0, Qt.AlignCenter)
bottom_layout_right.addWidget(fl_brake_temperature, 0, 1, Qt.AlignCenter)
bottom_layout_right.addWidget(fr_brake_icon, 0, 2, Qt.AlignCenter)
bottom_layout_right.addWidget(fr_brake_temperature, 0, 3, Qt.AlignCenter)
bottom_layout_right.addWidget(rl_brake_icon, 1, 0, Qt.AlignCenter)
bottom_layout_right.addWidget(rl_brake_temperature, 1, 1, Qt.AlignCenter)
bottom_layout_right.addWidget(rr_brake_icon, 1, 2, Qt.AlignCenter)
bottom_layout_right.addWidget(rr_brake_temperature, 1, 3, Qt.AlignCenter)

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

    if gear[index] > 1:
        gear_label.setText(f"GEAR: {gear[index]}")
    elif gear[index] < 0:
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

    fl_brake_temperature.setText(f"{fl_brakes[index]}°")
    fr_brake_temperature.setText(f"{fr_brakes[index]}°")
    rl_brake_temperature.setText(f"{rl_brakes[index]}°")
    rr_brake_temperature.setText(f"{rr_brakes[index]}°")
    

    index += 1

    
timer = QTimer()
timer.timeout.connect(update)
timer.start(16)  # ~60 FPS (16 ms)




window.show()
sys.exit(app.exec())