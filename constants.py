# for production
DATA_SOURCE_TYPE = 'csv'
DATALAKE_HTTPSEVER_FOLDER = r'C:\inetpub\wwwroot\DataLake'
DATALAKE_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\ProjectBook_DataLake'

PROJECTBOOKCHECK_INPUT_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\prod\input'
PROJECTBOOKCHECK_INPUT_ARCHIVE_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\archive\input'

PROJECTBOOKCHECK_HTTPSERVER_FOLDER = r'C:\inetpub\wwwroot\DataLake\ProjectBookCheck'
PROJECTBOOKCHECK_OUTPUT_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\prod\output'

LOG_FILE = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\prod\log\ProjectBookExport.log'




#for development
DATA_SOURCE_TYPE = 'csv'
DATALAKE_HTTPSERVER_FOLDER = r'.\output\HTTPSERVER'
DATALAKE_FOLDER = r'.\output\DATALAKE'

# PROJECTBOOKCHECK_INPUT_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\dev\input'

PROJECTBOOKCHECK_INPUT_ARCHIVE_FOLDER = r'\\ct.dot.ca.gov\dfshq\DIROFC\Asset Management\4e Project Book\Projectbook_DataChecksSupport\archive\input'

PROJECTBOOKCHECK_HTTPSERVER_FOLDER = r'.\output\HTTPSERVER\PROJECTBOOKCHECK'
PROJECTBOOKCHECK_OUTPUT_FOLDER = r'.\output\DATALAKE\PROJECTBOOKCHECK'

LOG_FILE = r'.\output\LOG\ProjectBookExport.log'

