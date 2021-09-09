from math import degrees,radians,sin,atan

def longitudDe_LaRecta (punto_1 :list, punto_2 :list):
        #         _________________________
        #        /(X2 - X1)^2 + (Y2 - Y1)^2
        return (((punto_2[0] - punto_1[0])**2) + ((punto_2[1] - punto_1[1])**2))**.5



def AngulosDe_LaRecta(punto_1 :list, punto_2 :list):
    #      (Y2 - Y1)       _1                         _.-`| (X1,Y1) a<
    #  m = ---------    tan   (m)               m _.-`   _|
    #      (X2 - X1)               (X2,Y2) a< _.-`______|_|
    m = (punto_2[1] - punto_1[1])/(punto_2[0] - punto_1[0])
    angulos = dict()
    angulos['X1,0'] = abs(degrees(atan(m)))
    angulos['0,Y2'] = 90 - angulos['X1,0']
    return angulos




def coordenadasCirculares(CoorDel_centro: list, RADIO ,NumDe_DivicionesDel_Circulo = 0, unidadesDe_Desplazamiento = 0, sentido =''):
    x_centro  = CoorDel_centro[0]
    y_centro = CoorDel_centro[1]
    x = y = 0
    
    try:
        unidadDe_DivicionDel_Circulo = 360 / NumDe_DivicionesDel_Circulo
    except ZeroDivisionError:
        return {'x': x_centro, 'y': y_centro}

    if sentido == 'horario':
        y = 90 - ((unidadDe_DivicionDel_Circulo * unidadesDe_Desplazamiento) + unidadDe_DivicionDel_Circulo) 
        x = 90 - abs(y)
    elif sentido == 'antihorario':
        x =  - ((unidadDe_DivicionDel_Circulo * unidadesDe_Desplazamiento) + unidadDe_DivicionDel_Circulo)
        y = 90 - abs(x)
    else: # sentido Radial
        x = 90 - (unidadDe_DivicionDel_Circulo * unidadesDe_Desplazamiento)
        y = 90 - abs(x)

    carteciano_x = (sin(radians(x)) * RADIO)
    carteciano_y = (sin(radians(y)) * RADIO)
    return {'x' :  x_centro + carteciano_x, 'y' : y_centro - carteciano_y}

#                                  x1+ --> 
#                        y1+ +- - - - - |- - - - - - +
#                        |   |      . . 12. .        | 
#                        v   |    11    |      1     |
#[oX +, oY -]__/ [-x, +y ]   |  10      |        2   |   [+x ,+y ] \__ [oX +, oY -]
#              \ [+x1,+y1]   |.         | [oX,oY]  . |   [+x1,+y1] /
#                ------------|9---------|/---------3 |-----------  
#                            |.         |          . | 
#                            |  8       |        4   |
#[oX +, oY -]__/ [-x, +y ]   |    7     |      5     |   [+x, -y ] \__ [oX +, oY -]
#              \ [+x1,+y1]   |      . . 6 . .        |   [+x1,+y1] /
#                            +- - - - - |- - - - - - + 
#                                       |



if __name__ == '__main__':
    XD = coordenadasCirculares([100,100], 100,12,2,'horario')
    print(XD)