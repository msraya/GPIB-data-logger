import ConfigParser
import visa
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.exporters as pge
import os.path as osp
import os
from sys import exit

# import the "form class" from your compiled UI
from logger import Ui_Dialog

# For the icon appear on application in the bottom bar of windows 10
import ctypes
myappid = 'Manolo.GPIB.Plot_GPIB.V02' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

# Main windows as simple dialog window
class Dialog(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent=parent)
        pg.setConfigOptions(antialias=True)

        # set up the form class as a `ui` attribute
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(_fromUtf8("Frequency Logger"))
        self.setWindowIcon(QtGui.QIcon("hola.png"))
        self.ui.pb_exit.clicked.connect(exit_btn)
        self.ui.pb_save.clicked.connect(save_btn)
        self.ui.pb_start.clicked.connect(start_btn)
        self.ui.pb_stop.clicked.connect(stop_btn)
        
        global combo       
        combo=self.ui.select_box
        
        global curve, plot
        curve = self.ui.graphicsView.plot(pen='y')
        plot = self.ui.graphicsView
        plot.showGrid(x=True, y=True, alpha=1.0)
        plot.enableAutoRange('xy', True)
        plot.setClipToView(False)
        plot.setTitle(_fromUtf8("Frequency Logger"))
        plot.setLabels(left=('Frequency', 'Hz'))
        plot.setLabels(bottom=('Samples', 's'))        
        
        global timer
        timer = QtCore.QTimer()
        timer.timeout.connect(update)
        
        global apath, rm, config, Device
        apath=os.getenv('INSTDIR')
        if apath==None:
            apath='';
        else:
            apath=apath+'\\'
    
        if not osp.exists(apath+'multi.ini'):
            config= ConfigParser.RawConfigParser()
            config.add_section('Main')
            vipath=os.getenv('VXIPNPPATH')
            config.set('Main', 'VisaLib', vipath+'WinNT\\agvisa\\agbin\\visa32.dll')
            config.set('Main','Device_List','34401A 53220A 53131A K2015 NRVS')
            config.set('Main', 'Device', '34401A')                
            config.add_section('34401A')
            config.set('34401A', 'CONF', '*RST;SYST:BEEP;DISP OFF;CONF:VOLT:DC 10,0.00001')
            config.set('34401A', 'READ', 'READ?')
            config.set('34401A', 'GPIB_Device', 'GPIB0::15::INSTR')
            config.add_section('53220A')
            config.set('53220A', 'CONF', "*RST;DISP OFF;CONF:FREQ 1E6, 0.01;")
            config.set('53220A', 'READ', 'READ?')
            config.set('53220A', 'GPIB_Device', 'GPIB0::3::INSTR')
            config.add_section('53131A')
            config.set('53131A', 'CONF', "*RST;STAT:PRES;DISP:ENAB OFF;FUNC 'FREQ 1';EVEN:LEV:AUTO OFF;ROSC:SOUR INT;ROSC:EXT:CHEC OFF;:DIAG:CAL:INT:AUTO OFF;:FREQ:EXP 950000;:HCOP:CONT OFF;FREQ:ARM:STAR:SOUR IMM;FREQ:ARM:STOP:SOUR TIM;FREQ:ARM:STOP:TIM .100;:INIT:CONT ON;")
            config.set('53131A', 'READ', 'FETC:FREQ?')
            config.set('53131A', 'GPIB_Device', 'GPIB0::3::INSTR')
            config.add_section('K2015')         
            config.set('K2015', 'CONF', "*RST;DISP:ENAB 0;VOLT:DC:RANG 10;VOLT:DC:DIG 7;FUNC 'VOLT:DC'")
            config.set('K2015', 'READ', 'READ?')
            config.set('K2015', 'GPIB_Device', 'GPIB0::16::INSTR')                        
            config.add_section('NRVS')         
            config.set('NRVS', 'CONF', "C1;DA 50;U0;M0;KA1;O0;RS4;SC0;N1;B0;W4;AV2;X3")
            config.set('NRVS', 'READ', 'X1')
            config.set('NRVS', 'GPIB_Device', 'GPIB0::13::INSTR')   
            
            with open(apath+'multi.ini', 'wt') as configfile:
                config.write(configfile)
            configfile.close()
            infodialog('Creado archivo '+apath+'multi.ini')

        config = ConfigParser.ConfigParser()
        configfile=open(apath+'multi.ini')
        config.readfp(configfile)
        configfile.close()
        
        combo.clear()
        lista_device=config.get('Main','Device_List', 0).split()
        for equipo in lista_device :
            combo.addItem(equipo)
        Device=config.get('Main', 'Device', 0)
        combo.setCurrentIndex(combo.findText(Device))
        combo.currentIndexChanged.connect(selectionchange)
        visa_lib=config.get('Main', 'VisaLib', 0)
        try:        
            rm = visa.ResourceManager(visa_lib)
        except:
            errordialog("Cannot Start VISA Subsistem: " + visa_lib + '.')
            return
            
        init_gpib()

def init_gpib():
        global inst, data, number, config
        #if inst != None:
         #   inst.close()
        gpib_dev=config.get(Device, 'GPIB_Device', 0)
        try:
            inst = rm.open_resource(gpib_dev)
        except:
            errordialog("Cannot connect with device: "+gpib_dev+'.')
            return
            
        global gpib_read
        inst.timeout=1000;
        inst.read_termination='\n';
        inst.delay=1.2;
        gpib_conf=config.get(Device, 'CONF', 0)
        for x in gpib_conf.split(';'):
            write_dis(x.strip())
        gpib_read=config.get(Device, 'READ', 0)
        print(gpib_read)
        val=query_dis(gpib_read)

        print(val)
        # val=val[1:-1]
        print(float(val))        
        data=[val]
        curve.setData(data)
        number=0    
    

def selectionchange():
        global combo, apath
        text=combo.currentText()
        config = ConfigParser.ConfigParser()
        configfile=open(apath+'multi.ini')
        config.readfp(configfile)
        configfile.close()        
        config.set('Main', 'Device', text)
        with open(apath+'multi.ini', 'wt') as configfile:
                config.write(configfile)
        configfile.close()
        init_gpib()                
  #      config.close();        
    
def query_dis(cadena):
    global inst, timer
    try:            
        return inst.query(cadena)
    except:
        errordialog("Device not answer.")
        timer.stop()          
        #exit()
        
def write_dis(cadena):
    global inst
    try:            
        inst.write(cadena)
    except:
        errordialog("Device not answer.")
       # exit()
        
def errordialog(texto):
   msg = QtGui.QMessageBox()
   msg.setIcon(QtGui.QMessageBox.Critical)
   msg.setText("Application Error")
   msg.setInformativeText(texto)
   msg.setWindowTitle("Error")
   msg.setStandardButtons(QtGui.QMessageBox.Ok)
   msg.exec_()

def infodialog(texto):
   msg = QtGui.QMessageBox()
   msg.setIcon(QtGui.QMessageBox.Information)
   msg.setText("Aplication Information")
   msg.setInformativeText(texto)
   #msg.setDetailedText(texto)
   msg.setWindowTitle("Information")
   
   msg.setStandardButtons(QtGui.QMessageBox.Ok)
   msg.exec_()

def update():
    global ptr, data, curve, inst, gpib_read
    tmp=[None] 
    try:
        tmp[0]=float(query_dis(gpib_read))
    except:
        []
    data.extend(tmp)
    curve.setData(data)

def exit_btn():
    app.exit()
    
def save_btn():
    global curve, plot, number
    exporter = pge.ImageExporter(plot.plotItem)
    files=apath+'save'+str(number)+'.png'
    exporter.export(files)
    number+=1;
    infodialog('File '+files+' saved sucessfully.')

def start_btn():
    global timer
    timer.start(100)
    
def stop_btn():
    global timer
    timer.stop()  

app = QtGui.QApplication([])
widget = Dialog()
widget.show()
app.exec_()
