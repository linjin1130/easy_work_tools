# 	FileName:DAboard_defines.py
# 	Author:LinJin
# 	E-mail:18685029093@ustc.edu.cn
# 	All right reserved @ LinJin.
# 	Modified: 2018.2.18
#   Description:The command and status define class of DAC

class DABoard_Defines:
   'Class which contains all #defines from uhwd_common.h'
   def __init__(self):
      print ("Calling Board_Defines class constructor")
      
   DRAM_SIZE_BYTES           = 0x40000   
   CMD_NON_VAL               = 0x0       
   CMD_READ_REG              = 0x1       
   CMD_WRITE_REG             = 0x2       
   CMD_READ_MEM              = 0x3       
   CMD_WRITE_MEM             = 0x4       
   CMD_CTRL_CMD              = 0x5       
   CMD_LAST                  = CMD_CTRL_CMD
   CTRL_NON_VAL              = 0x0       
   CTRL_REINIT               = 0x1       
   CTRL_START_CAP            = 0x2       
   CTRL_CHECK_CAP            = 0x3       
   CTRL_START_PLAY           = 0x4       
   CTRL_STOP_PLAY            = 0x5       
   CTRL_ERASE_ALL            = 0x6
   CTRL_ERASE_PART           = 0x7
   CTRL_SET_WDTO             = 0x8
   CTRL_SET_LOOP             = 0x9       
   CTRL_FILL_MEM             = 0xA   
   CTRL_DUMP_MEM             = 0xB       
   CTRL_READ_FLAG            = 0xF
   CTRL_INIT                 = 0x1A
   CTRL_RD_DAC1              = 0x1C
   CTRL_RD_DAC2              = 0x1D
   CTRL_SYNC_CTRL            = 0x18
   CTRL_DAC_POWER            = 0x1E
   CTRL_DAC_DEFAULT          = 0x1B
   CTRL_DUMP_DMARXREGS       = 0x12      
   CTRL_MONITOR              = 0x13
   CTRL_CMD_ADPT              = 0x21
   CTRL_JESD_DATA_IF_SY_STAT  = 0x22
   CTRL_LAST                 = CTRL_JESD_DATA_IF_SY_STAT
   STAT_SUCCESS              = 0x0       
   STAT_ERROR                = 0x1       
   STAT_CMDERR               = 0x2       
   STAT_RDERR                = 0x3       
   STAT_WRERR                = 0x4       
   STAT_MEM_RANGE_ERR        = 0x5       
   STAT_MEM_ALIGN_ERR        = 0x6       
   STAT_SIZE_ERR             = 0x7       
   STAT_SIZE_ALIGN_ERR       = 0x8       
   STAT_ADDR_ALIGN_ERR       = 0x9       
   STAT_DATAIF_BUSY          = 0xA       
   STAT_DATAIF_ERR           = 0xB       
   STAT_DMA_ERR              = 0xC       
   STAT_LAST                 = STAT_DMA_ERR
   BANK_SWREG                = 0x0       
   BANK_CSR                  = 0x1       
   BANK_JESDTX               = 0x2       
   BANK_JESDRX               = 0x3       
   BANK_JESDPHY              = 0x4       
   BANK_JESDIF               = 0x5       
   BANK_MB                   = 0x6       
   BANK_SPI                  = 0x7
   BANK_LAST                 = BANK_SPI
   SWREG_SIZE                = 9         
   SWREG_SWVERSION           = 0x0 << 2      
   SWREG_TESTREG0            = 0x1 << 2       
   SWREG_TESTREG1            = 0x2 << 2       
   SWREG_TESTREG2            = 0x3 << 2       
   SWREG_TESTREG3            = 0x4 << 2       
   SWREG_TESTREG4            = 0x5 << 2       
   SWREG_TESTREG5            = 0x6 << 2       
   SWREG_TESTREG6            = 0x7 << 2       
   SWREG_TESTREG7            = 0x8 << 2       
   SWREG_LAST                = SWREG_TESTREG7
   PLATFORM_IDENTITY         = 0x0 << 2       
   PLATFORM_HWVERSION        = 0x1 << 2       
   PLATFORM_SY_STAT          = 0x2 << 2      
   PLATFORM_IO_CTRL          = 0x10 << 2      
   PLATFORM_IO_STAT          = 0x10 << 2      
   JESD_DATA_IF_TX_STAT      = 0x20 << 2      
   JESD_DATA_IF_RX_STAT      = 0x30 << 2      
   JESD_DATA_IF_LA_STAT      = 0x40 << 2      
   JESD_DATA_IF_LA_CTRL      = 0x40 << 2      
   JESD_DATA_IF_LA_CNFG      = 0x41 << 2    
   JESD_VERSION_REG          = 0x0       
   JESD_RESET_REG            = 0x4       
   JESD_ILA_SUP_REG          = 0x8       
   JESD_SCRAMBL_REG          = 0xC       
   JESD_SYSREF_CTRL_REG      = 0x10      
   JESD_ILA_MULTI_REG        = 0x14      
   JESD_TEST_MODE_REG        = 0x18      
   JESD_ERROR_STAT_REG0      = 0x1C      
   JESD_F_REG                = 0x20      
   JESD_K_REG                = 0x24      
   JESD_LANES_REG            = 0x28      
   JESD_SUBCLASS_REG         = 0x2C      
   JESD_RX_BUF_DELAY_REG     = 0x30      
   JESD_ERR_REP_REG          = 0x34
   JESD_SYNC_STAT_REG        = 0x38      
   JESD_ERROR_STAT_REG1      = 0x3C      
   JESD_LINK_ERR_CNT0        = 0x824     
   JESD_LINK_ERR_CNT1        = JESD_LINK_ERR_CNT0 + 0x40
   JESD_LINK_ERR_CNT2        = JESD_LINK_ERR_CNT1 + 0x40
   JESD_LINK_ERR_CNT3        = JESD_LINK_ERR_CNT2 + 0x40
   JESD_LINK_ERR_CNT4        = JESD_LINK_ERR_CNT3 + 0x40
   JESD_LINK_ERR_CNT5        = JESD_LINK_ERR_CNT4 + 0x40
   JESD_LINK_ERR_CNT6        = JESD_LINK_ERR_CNT5 + 0x40
   JESD_LINK_ERR_CNT7        = JESD_LINK_ERR_CNT6 + 0x40
   JESD_LINK_BUF_ADJ0        = 0x830     
   JESD_LINK_BUF_ADJ1        = JESD_LINK_BUF_ADJ0 + 0x40
   JESD_LINK_BUF_ADJ2        = JESD_LINK_BUF_ADJ1 + 0x40
   JESD_LINK_BUF_ADJ3        = JESD_LINK_BUF_ADJ2 + 0x40
   JESD_LINK_BUF_ADJ4        = JESD_LINK_BUF_ADJ3 + 0x40
   JESD_LINK_BUF_ADJ5        = JESD_LINK_BUF_ADJ4 + 0x40
   JESD_LINK_BUF_ADJ6        = JESD_LINK_BUF_ADJ5 + 0x40
   JESD_LINK_BUF_ADJ7        = JESD_LINK_BUF_ADJ6 + 0x40
   JESD_PHY_VERSION_REG      = 0x0       
   JESD_PHY_PLL_STATUS       = 0x80      
   JESD_PHY_LOOP_OFF         = 0         
   JESD_PHY_LOOP_PCS         = 1         
   JESD_PHY_LOOP_PMA         = 2         
   JESD_PHY_LOOP_MAX         = 2
   SPANSION_FLASH            = 3
   MICRON_FLASH              = 0