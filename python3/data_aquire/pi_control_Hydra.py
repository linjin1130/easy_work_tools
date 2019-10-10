from pipython import GCSDevice
from pipython import GCSDevice, pitools

CONTROLLERNAME = 'POLLUX'
STAGES = None  # this controller does not need a 'stages' setting
REFMODE = None

ip = '172.16.0.34'
hyrda = GCSDevice(CONTROLLERNAME)
hyrda.ConnectTCPIP(ipaddress=ip, ipport=400)
# gcs.InterfaceSetupDlg()
print(hyrda.qIDN())
if hyrda.HasqVER():
    print('version info: {}'.format(hyrda.qVER().strip()))

print('initialize connected stages...')
pitools.startup(hyrda, stages=STAGES, refmode=REFMODE)
print('initialize connected stages...')
pitools.startup(hyrda, stages=STAGES, refmode=REFMODE)
hyrda.VEL(2, 2)
print(hyrda.qVEL(2))
# hyrda.MOV(hyrda.axes[1], 11.0)

# To check the on target state of an axis there is the GCS command
# qONT(). But it is more convenient to just call "waitontarget".

pitools.waitontarget(hyrda)

hyrda.CloseConnection()