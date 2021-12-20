# for production
DATA_SOURCE_TYPE = 'csv'
DATALAKE_HTTPSEVER_FOLDER = r'C:\inetpub\wwwroot\DataLake'
DATALAKE_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\ProjectBook_DataLake'

PROJECTBOOKCHECK_INPUT_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\prod\input'
PROJECTBOOKCHECK_INPUT_ARCHIVE_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\archive\input'

PROJECTBOOKCHECK_HTTPSEVER_FOLDER = r'C:\inetpub\wwwroot\DataLake\ProjectBookCheck'
PROJECTBOOKCHECK_OUTPUT_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\prod\output'
TARGET_FY = 2021

LOG_FILE = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\prod\log\ProjectBookExport.log'




#for development
DATA_SOURCE_TYPE = 'csv'
DATALAKE_HTTPSEVER_FOLDER = r'.\output\HTTPSEVER'
DATALAKE_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\ProjectBook_DataLake'

# PROJECTBOOKCHECK_INPUT_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\dev\input'

PROJECTBOOKCHECK_INPUT_ARCHIVE_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\archive\input'

PROJECTBOOKCHECK_HTTPSEVER_FOLDER = r'.\output\HTTPSEVER\PROJECTBOOKCHECK'
PROJECTBOOKCHECK_OUTPUT_FOLDER = r'.\output\DATALAKE\PROJECTBOOKCHECK'

LOG_FILE = r'.\output\LOG\ProjectBookExport.log'

