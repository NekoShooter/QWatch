import pytz
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QApplication,\
                            QWidget,\
                            QPushButton,\
                            QVBoxLayout,\
                            QHBoxLayout,\
                            QButtonGroup,\
                            QLabel

from datetime import datetime
import time
from QtReloj import QReloj

class ventanaPrincipal(QWidget):
    def __init__(self):
        super(QWidget,self).__init__()
        self.porpiedades_internas()
        self.iniciador()
        self.estilo()
        self.estructura()
        self.conexiones()
        self.ActualizarFechaHora()
        self.ARRANCAR()

    def porpiedades_internas(self):
        self.setMaximumSize(250,250)

    def iniciador(self):
        self.boton_local = QPushButton('Local')
        self.boton_Mexico = QPushButton('Cd Mexico')
        self.boton_EU = QPushButton('New York')
        self.boton_Japon = QPushButton('Tokio')

        self.grupoDe_Botones = QButtonGroup()
        self.grupoDe_Botones.addButton(self.boton_local,0)
        self.grupoDe_Botones.addButton(self.boton_Mexico,1)
        self.grupoDe_Botones.addButton(self.boton_EU,2)
        self.grupoDe_Botones.addButton(self.boton_Japon,3)

        self.reloj  = QReloj()
        self.meridiano = QLabel('AM')
        self.sec = self.min = self.hr = 0
        self.dia = self.mes = self.anyo = 0

        self.Tiempo = QtCore.QTimer()

        self.Pais_seleccionado = 0
        self.Pais = ('Local','Mexico : CDMX', 'EU : Nueva_York','Japon : Tokio')

        self.etiqueta = QLabel('Reloj')

    def estilo(self):
        self.setStyleSheet('background-color:#10002b;')
        paleta = QtGui.QPalette()
        paleta.setColor(QtGui.QPalette.WindowText,QtGui.QColor('#9bf6ff'))
        paleta.setColor(QtGui.QPalette.ButtonText,QtGui.QColor('#9bf6ff'))
        self.etiqueta.setPalette(paleta)
        self.meridiano.setPalette(paleta)
        self.meridiano.setAlignment(QtCore.Qt.AlignCenter)
        self.boton_EU.setPalette(paleta)
        self.boton_EU.setFlat(True)
        self.boton_Mexico.setPalette(paleta)
        self.boton_Mexico.setFlat(True)
        self.boton_Japon.setPalette(paleta)
        self.boton_Japon.setFlat(True)
        self.boton_local.setPalette(paleta)
        self.boton_local.setFlat(True)

    def estructura(self):
        h1 = QHBoxLayout()
        h1.addWidget(self.etiqueta)
        h1.addWidget(self.meridiano)

        div_reloj = QHBoxLayout()
        div_reloj.addWidget(self.reloj)
        div_botones = QHBoxLayout()
        div_botones.addWidget(self.boton_local)
        div_botones.addWidget(self.boton_Mexico)
        div_botones.addWidget(self.boton_EU)
        div_botones.addWidget(self.boton_Japon)

        self.CUERPO = QVBoxLayout(self)
        self.CUERPO.addLayout(h1)
        self.CUERPO.addLayout(div_reloj)
        self.CUERPO.addLayout(div_botones)

    def conexiones(self):
        self.grupoDe_Botones.buttonClicked[int].connect(self.__push__)
        self.reloj.CambioDeFecha.connect(self.ActualizarFechaHora)
        self.Tiempo.timeout.connect(self.reloj.CorrerTiempo)
        self.reloj.CambioMeridiano.connect(self.meridiano.setText)

    def ARRANCAR(self):
        self.Tiempo.start(1000)

    def __push__(self,Pais_elegido):
        self.Pais_seleccionado = Pais_elegido
        self.ActualizarFechaHora()
        

    def ActualizarFechaHora(self):
        ubicacion_actual = self.Pais[self.Pais_seleccionado]
        zonaHoraria = None
        if ubicacion_actual == 'Mexico : CDMX':
            zonaHoraria = pytz.timezone('America/Mexico_City')
        elif ubicacion_actual == 'EU : Nueva_York':
            zonaHoraria = pytz.timezone('America/New_York')
        elif ubicacion_actual == 'Japon : Tokio':
            zonaHoraria = pytz.timezone('Asia/Tokyo')
        fecha_y_hora = datetime.now(zonaHoraria)
        self.hr = fecha_y_hora.hour
        self.min = fecha_y_hora.minute
        self.sec = int(fecha_y_hora.second)
        self.dia = fecha_y_hora.date().day
        self.mes = fecha_y_hora.date().month
        self.anyo = fecha_y_hora.date().year
        self.__actualizarCalendario__()

        self.__actualizarReloj__()

    def __actualizarReloj__(self):
        self.reloj.ActualizarHoraCompleta(self.hr, self.min, self.sec)
    def __actualizarCalendario__(self):
        self.etiqueta.setText(f'{self.dia}/{self.mes}/{self.anyo} : Pais {self.Pais[self.Pais_seleccionado]}')
            


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    v = ventanaPrincipal()
    v.show()
    sys.exit(app.exec_())