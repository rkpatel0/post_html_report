import regression.database as db
import regression.report_gen as gen
import webgen.report as reb

# -----------------------------------------------------------------------------
# Configurable Parameters
# -----------------------------------------------------------------------------
CHANNEL = 'B'            # 'A' or 'B'
EVKTYPE = 'EVK1900'       # EVK1900 / EVK900 / EVK2400
TESTTYPE = 'CHAR'        # CHAR / SOAK / PMU
REPORT_EXT = 'DCOS_PART_TEMP_FULL'      # Unique Report Name
SAVE_PATH = r'C:\Users\Rishi.Patel\iDocuments\Maxim\webreports\SC2200/'

# Files to Read
logfiles = [
           'TT_158B20150504T132514.csv',
#           'TT_158B20150501T153956.csv',
            ]

# -----------------------------------------------------------------------------
# Use to overwrite default settings
# -----------------------------------------------------------------------------
analysis = {
#            'filter': [],    # Add param to this list to overwrite default
#            'sweep': [],
#            'derate': []
            }

# -----------------------------------------------------------------------------
# Generate Objects
# -----------------------------------------------------------------------------
if TESTTYPE == 'CHAR':
    oGen = gen.Char(config=analysis, chan=CHANNEL)
elif TESTTYPE == 'PMU':
    oGen = gen.Pmu(config=analysis, chan=CHANNEL)
elif TESTTYPE == 'SOAK':
    oGen = gen.Soak(config=analysis, chan=CHANNEL)
else:
    raise IndexError('No Test found of TYPE:' + TESTTYPE)

oData = db.Reader()
oWeb = reb.MaximIntegrated({'save_path': SAVE_PATH})
# -----------------------------------------------------------------------------
# Read Data, Process and Generate Report
# -----------------------------------------------------------------------------
data = oData.fetch_datalogs(logfiles, EVKTYPE, TESTTYPE, 'C:\Users\Rishi.Patel\Desktop/')
pages = oGen.data_to_report(data, oData.info)
oWeb.generate_report(pages, name=TESTTYPE + '_' + EVKTYPE + '_' + REPORT_EXT)
