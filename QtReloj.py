from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import QPixmap,QPainter
from PyQt5.QtCore import QRectF,QPointF
from HerramientasCartecianas import coordenadasCirculares

class QReloj(QtWidgets.QWidget):

    CambioDeFecha = QtCore.pyqtSignal(bool)
    CambioMeridiano = QtCore.pyqtSignal(str)

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        self.propiedades_internas()
        self.iniciador()


    def  propiedades_internas(self):
        self.setMinimumSize(200,200)


    def Pixmap_verifiacacion(self):
        self.lienzo = QPixmap(self.rect().size())
        return self.lienzo.isNull()


    def iniciador(self):
        self.lienzo = None
        self.CENTRO = None
        self.longitudMaxVentana = 0
        self.longitudMinVentana = 0

        self.sec = self.min =  59 
        self.hr = 11
        self.hr_24 = 11


        self.__AbortarMision__  = self.Pixmap_verifiacacion()


    def __centro(self):
        centro_x = self.size().width() / 2
        centro_y = self.size().height() / 2
        if centro_x > centro_y:
            self.longitudMaxVentana = self.size().width()
            self.longitudMinVentana = self.size().height()
        else:
            self.longitudMaxVentana = self.size().height()
            self.longitudMinVentana = self.size().width()
        return (centro_x,centro_y)


    def paintEvent(self,event):
        # inicio para dibujar todo el programa
        self.__iniciar__()
        
    def __iniciar__(self):
        if self.__AbortarMision__:
            return
        self.CENTRO = self.__centro()
        #color del fondo
        self.lienzo.fill(QtGui.QColor('#10002b'))
        #crear linezo
        Pintar = QPainter(self)
        Pintar.drawPixmap(0,0,self.lienzo)
        self.DibujarContenido(Pintar)


    def DibujarContenido(self,Pintar):
        Pintar.setRenderHint(QPainter.Antialiasing,True)
        self._dibujarContornoReloj(Pintar)
        self._dibujarManesilla(Pintar,self.longitudMinVentana *.35,self.sec,60,2,'#fdffb6')
        self._dibujarManesilla(Pintar,self.longitudMinVentana *.30,self.min,60,5,'#9bf6ff')
        self._dibujarManesilla(Pintar,self.longitudMinVentana *.20,self.hr,12,7,'#ffc09f')


    def resizeEvent(self, event):
        #redibujar en caso de redimencionarse la ventana
        self.__resetear__()

    def __resetear__(self):
        if self.__AbortarMision__:
            return
        del self.lienzo
        self.lienzo = None
        self.__AbortarMision__ = self.Pixmap_verifiacacion()
        self.__Recalcular__ = True


    def __Centra_dimencion(self,Tam_Reloj):
        tam_x = self.size().width()
        tam_y = self.size().height()
        return QRectF((tam_x - Tam_Reloj)/2, (tam_y - Tam_Reloj)/2,Tam_Reloj,Tam_Reloj)

        
    def _dibujarContornoReloj(self,Pintar):
        Pen = QtGui.QPen()
        Pen.setWidth(3)
        Pen.setColor(QtGui.QColor('#7400b8'))
        Pintar.setPen(Pen)
        Pintar.drawEllipse(self.__Centra_dimencion(self.longitudMinVentana - 20))
        self.__minutero_y_segundero(Pintar)

        
    def __minutero_y_segundero(self,Pintar):
        Pen = Pintar.pen()
        Pen.setColor(QtGui.QColor('#ffadad'))
        Pintar.setPen(Pen)

        for i in range(60):
            p1 = coordenadasCirculares(self.CENTRO,self.longitudMinVentana*.45, 60,i)
            p2 = coordenadasCirculares(self.CENTRO,self.longitudMinVentana*.44, 60,i)
            Pintar.drawLine(QPointF(p1['x'],p1['y']),QPointF(p2['x'],p2['y']))

        Pen.setColor(QtGui.QColor('#9bf6ff'))
        Pintar.setPen(Pen)
        for i in range(12):
            p1 = coordenadasCirculares(self.CENTRO,self.longitudMinVentana*.45, 12,i)
            p2 = coordenadasCirculares(self.CENTRO,self.longitudMinVentana*.40, 12,i)
            p3 = coordenadasCirculares(self.CENTRO,self.longitudMinVentana*.35, 12,i,'horario')
            Pintar.drawLine(QPointF(p1['x'],p1['y']),QPointF(p2['x'],p2['y']))
            Pintar.drawText(QPointF(p3['x'] - 3,p3['y'] + 3),str(i + 1))


    def _dibujarManesilla(self,Pintar,longitud,unidad_de_tiempo,ciclos,grosor = 1,color='#000000'):
        Pen = Pintar.pen()
        Pen.setWidth(grosor)
        Pen.setCapStyle(QtCore.Qt.RoundCap)
        Pen.setColor(QtGui.QColor(color))
        Pintar.setPen(Pen)
        XY = coordenadasCirculares(self.CENTRO,longitud,ciclos,unidad_de_tiempo,'horario')
        coor_XY = QPointF(XY['x'],XY['y'])
        Pintar.drawLine(QPointF(self.CENTRO[0],self.CENTRO[1]),coor_XY)

    def CorrerTiempo(self):
        self.ActualizarSec(self.sec + 2)

    def ActualizarSec(self,sec):
        self.sec = sec - 1
        if self.sec > 59:
            self.sec = 0
            self.ActualizarMin(self.min + 2)
        else:
            self.update()

    def ActualizarMin(self,min):
        self.min = min - 1
        if self.min > 59:
            self.min = 0
            self.ActualizarHr(self.hr + 2)
        else:
            self.update()

    def ActualizarHr(self,hr):
        self.hr_24 = hr - 1
        if self.hr_24 > 23:
            self.hr_24 = 0
            self.CambioDeFecha.emit(True)
            self.CambioMeridiano.emit('AM')
        if self.hr_24 > 11 :
            self.hr  = self.hr_24 - 12
            self.CambioMeridiano.emit('PM')
        else:
            self.hr = self.hr_24
        self.update()

    def ActualizarHoraCompleta(self,Hr,Min,Sec):
        self.hr_24 = Hr - 1
        if self.hr_24 > 11:
            self.hr = self.hr_24 - 12
            self.CambioMeridiano.emit('PM')
        else:
            self.hr = self.hr_24
            self.CambioMeridiano.emit('AM')
        self.min = Min - 1
        self.sec = int(Sec) - 1
        self.update()


    

   
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    v = QReloj()
    v.ActualizarHoraCompleta(12,17,37)
    v.show()
    sys.exit(app.exec_())
