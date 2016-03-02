import regression.database as db
import regression.report_gen as gen
import webgen.report as reb

# ------------------------------------------------------------------------------
# Configurable Parameters
# ------------------------------------------------------------------------------
CHANNEL = 'A'               # 'A' or 'B'
EVKTYPE = 'EVK1900'         # EVK1900 / EVK900 / EVK2400
TESTTYPE = 'SOAK'           # CHAR / SOAK / PMU
REPORT_EXT = 'TMP_73A'      # Unique Report Name
SAVE_PATH = r'C:\Users\Rishi.Patel\iDocuments\Maxim\webreports\SC2200/'

# Files to Read
logfiles = [
#           'TTT_96A20141208T003004.csv',
           'FFF_107A20141215T123944.csv',
            ]

# ------------------------------------------------------------------------------
# Use to overwrite default settings
# ------------------------------------------------------------------------------
analysis = {
#            'filter': [],    # Add param to this list to overwrite default
#            'sweep': [],
#            'derate': []
            }

# ------------------------------------------------------------------------------
# Generate Objects
# ------------------------------------------------------------------------------
oData = db.Reader()
oGen = gen.Generate(config=analysis, chan=CHANNEL, test=TESTTYPE)
oWeb = reb.MaximIntegrated({'save_path': SAVE_PATH})

# ------------------------------------------------------------------------------
# Read Data, Process and Generate Report
# ------------------------------------------------------------------------------
data = oData.fetch_datalogs(logfiles, TESTTYPE, EVKTYPE)
pages = oGen.create_pages(data, oData.info)
oWeb.generate_report(pages, name=REPORT_EXT +  '_' + TESTTYPE + '_' + EVKTYPE)