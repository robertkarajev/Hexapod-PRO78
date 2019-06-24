import portSetup.portSetup as port
import walking.tripodgait as walking
import standing.stableStance as standing
import yoloServer.yolo_pickle_server as server
import time
import string
import threading

boundary = (85, 224, 416, 555, 640)
centerLocationPoint = 0;
personYLocationBorder = 0;

config = port.Configurations("UART1","/dev/ttyO1",9600)
config.initializePorts()
config.serialConn.close()
config.serialConn.open()

ready = threading.Event()
connection = server.Server(ready=ready)
mythread = threading.Thread(target=connection.connect)
mythread.start()
ready.wait()
thread = threading.Thread(target=connection.run)
thread.start()

try:
    if config.serialConn.isOpen():
        standing.stableStance(config)
        
        #Loop for main program
        while(True):
            #turnLeftBoudaries = 0 - 85
            #strafeLeftBoundary = 85 - 224
            #forwardBackwardBoundary = 224 - 416
            #strafeRightBoundary = 416 - 555
            #turnRightBoundary = 555 - 640
            if (connection.rectCenterWidth < 85 and connection.rectCenterWidth > 0):
                standing.stableStance(config)
                walking.turnLeft(config)
                
            elif (connection.rectCenterWidth < 224 and connection.rectCenterWidth > 85):
                walking.strafeLeft(config)
                
            elif (connection.rectCenterWidth < 416 and connection.rectCenterWidth > 224):
                #front 85 - 220
                #stand 220 - 265
                #back 265 - 615
                if connection.dimensionRectangleWidth > 85 and connection.dimensionRectangleWidth < 220:
                    standing.stableStance(config)
                    walking.tripodWalking(config)
                    
                elif connection.dimensionRectangleWidth > 220 and connection.dimensionRectangleWidth < 265:
                    standing.stableStance(config)

                elif connection.dimensionRectangleWidth > 265 and connection.dimensionRectangleWidth < 615:
                    standing.stableStance(config)
                    walking.reverse(config)
                
                else:
                    standing.stableStance(config)
                    
            elif (connection.rectCenterWidth < 555 and connection.rectCenterWidth > 416):
                walking.strafeRight(config)

            elif (connection.rectCenterWidth < 640 and connection.rectCenterWidth > 555):
                walking.turnRight(config)

            elif connection.rectCenterWidth < 0 or connection.rectCenterWidth > 640:
                standing.stableStance(config)
            
            else:
                standing.stableStance(config)

            time.sleep(0.2)

except KeyboardInterrupt:
    standing.sit(config)
    config.serialConn.close()
    connection.conn.close()