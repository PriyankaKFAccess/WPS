# DP-4 test module for OES 1.0
# Requirements:
# Selenium Driver: https://www.selenium.dev/downloads/
# Chrome Driver: https://chromedriver.chromium.org/downloads
# The dateutil libraries for Python 3: https://pypi.org/project/python-dateutil/
# The pytz libraries for Python 3: https://pypi.org/project/pytz/
# For default credentials and S3 upload, boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
# Usage: python spmRegression.py [-h] [-r] [-e] [-d] [-l] [-u]
# Arguments:
# -h, --headless:       Specifies headless or display mode for browser (default False)
# -r, --random:         Specifies random or set response mode for assessment (default False)
# -e, --env:            Specifies the environment to login and perform actions (default "uat")
# -d, --directory:      Specifies the directory to save any downloaded PDFs (default current working directory)
# -l, --log-to-file:    Specifies whether to log to the terminal output or to a text file in --directory (default False)
# --username:           Specifies a username to use for logging in; default credentials require S3, so required if S3 not available
# --password:           Specifies a password to use for logging in; default credentials require S3, so required if S3 not available

import sys

from oesLibrary import *
from dateutil.relativedelta import *
from datetime import date
import getopt, csv, os, re, mimetypes
import pprint
from contextlib import redirect_stdout, redirect_stderr

todaysDate = date.today()
uploadBucket = 'wps-qa-automation'

testInfo = {   'administrationdate': '0 years 4 months 0 days',
                             'assessmentform': 'Parent/Caregiver Interview',
                             'assessmenttype': 'dp4',
                             'clientagedays': '10',
                             'clientagemonths': '9',
                             'clientageyears': '2',
                             'clientcaseid': '62501',
                             'clientfirstname': 'DP4-QA',
                             'clientlastname': 'Sample',
                             'password': '',
                             'respondentname': 'DP4-QA Sample',
                             'scoreform': True,
                             'username': '',
                             'validateform': True,
                             'validateformmessage': 'This form is now ready to '
                                                    'score. Please click OK to '
                                                    'continue.'}

argsListAssessment = {   'Child Information': {   'Administration date': '6/23/2020',
                                                      "Child's ID": '62501',
                                                      "Child's age": '2 years '
                                                                     '9 months',
                                                      "Child's name": 'DP4-QA '
                                                                      'Sample'},
                             'Rater Information': {   'Parent/Caregiver’s name': 'Dalia',
                                                      'Parent/Caregiver’s relationship to child': 'Mother'}}

argsListValidation = {   'For Clinician Use Only': {   "Clinician's name/ID": 'S. '
                                                                                    'Jones',
                                                             'Confidence Interval': '95%',
                                                             'Scale Comparison': 'Standard'}}

questionList = {   'Adaptive Behavior Scale': {   'ceiling': 'Pass',
                                                              'q1': ['N'],
                                                              'q10': ['N'],
                                                              'q11': ['N'],
                                                              'q12': ['N'],
                                                              'q13': ['N'],
                                                              'q14': ['N'],
                                                              'q15': ['N'],
                                                              'q16': ['N'],
                                                              'q17': ['N'],
                                                              'q18': ['N'],
                                                              'q19': ['N'],
                                                              'q2': ['Y'],
                                                              'q20': ['N'],
                                                              'q21': ['skip'],
                                                              'q22': ['skip'],
                                                              'q23': ['skip'],
                                                              'q24': ['skip'],
                                                              'q25': ['skip'],
                                                              'q26': ['skip'],
                                                              'q27': ['skip'],
                                                              'q28': ['skip'],
                                                              'q29': ['skip'],
                                                              'q3': ['Y'],
                                                              'q30': ['skip'],
                                                              'q31': ['skip'],
                                                              'q32': ['skip'],
                                                              'q33': ['skip'],
                                                              'q34': ['skip'],
                                                              'q35': ['skip'],
                                                              'q36': ['skip'],
                                                              'q37': ['skip'],
                                                              'q38': ['skip'],
                                                              'q39': ['skip'],
                                                              'q4': ['Y'],
                                                              'q40': ['skip'],
                                                              'q41': ['skip'],
                                                              'q5': ['Y'],
                                                              'q6': ['N'],
                                                              'q7': ['N'],
                                                              'q8': ['N'],
                                                              'q9': ['N']},
                               'Cognitive Scale': {   'ceiling': 'Pass',
                                                      'q1': ['Y'],
                                                      'q10': ['N'],
                                                      'q11': ['N'],
                                                      'q12': ['N'],
                                                      'q13': ['N'],
                                                      'q14': ['N'],
                                                      'q15': ['N'],
                                                      'q16': ['N'],
                                                      'q17': ['N'],
                                                      'q18': ['N'],
                                                      'q19': ['N'],
                                                      'q2': ['Y'],
                                                      'q20': ['N'],
                                                      'q21': ['skip'],
                                                      'q22': ['skip'],
                                                      'q23': ['skip'],
                                                      'q24': ['skip'],
                                                      'q25': ['skip'],
                                                      'q26': ['skip'],
                                                      'q27': ['skip'],
                                                      'q28': ['skip'],
                                                      'q29': ['skip'],
                                                      'q3': ['N'],
                                                      'q30': ['skip'],
                                                      'q31': ['skip'],
                                                      'q32': ['skip'],
                                                      'q33': ['skip'],
                                                      'q34': ['skip'],
                                                      'q35': ['skip'],
                                                      'q36': ['skip'],
                                                      'q37': ['skip'],
                                                      'q38': ['skip'],
                                                      'q39': ['skip'],
                                                      'q4': ['Y'],
                                                      'q40': ['skip'],
                                                      'q41': ['skip'],
                                                      'q42': ['skip'],
                                                      'q5': ['Y'],
                                                      'q6': ['Y'],
                                                      'q7': ['Y'],
                                                      'q8': ['N'],
                                                      'q9': ['N']},
                               'Communication Scale': {   'ceiling': 'Pass',
                                                          'q1': ['Y'],
                                                          'q10': ['N'],
                                                          'q11': ['N'],
                                                          'q12': ['N'],
                                                          'q13': ['N'],
                                                          'q14': ['N'],
                                                          'q15': ['N'],
                                                          'q16': ['N'],
                                                          'q17': ['N'],
                                                          'q18': ['N'],
                                                          'q19': ['N'],
                                                          'q2': ['Y'],
                                                          'q20': ['N'],
                                                          'q21': ['skip'],
                                                          'q22': ['skip'],
                                                          'q23': ['skip'],
                                                          'q24': ['skip'],
                                                          'q25': ['skip'],
                                                          'q26': ['skip'],
                                                          'q27': ['skip'],
                                                          'q28': ['skip'],
                                                          'q29': ['skip'],
                                                          'q3': ['Y'],
                                                          'q30': ['skip'],
                                                          'q31': ['skip'],
                                                          'q32': ['skip'],
                                                          'q33': ['skip'],
                                                          'q34': ['skip'],
                                                          'q4': ['Y'],
                                                          'q5': ['Y'],
                                                          'q6': ['N'],
                                                          'q7': ['Y'],
                                                          'q8': ['Y'],
                                                          'q9': ['Y']},
                               'Physical Scale': {   'ceiling': 'Pass',
                                                     'q1': ['Y'],
                                                     'q10': ['N'],
                                                     'q11': ['N'],
                                                     'q12': ['N'],
                                                     'q13': ['N'],
                                                     'q14': ['N'],
                                                     'q15': ['N'],
                                                     'q16': ['N'],
                                                     'q17': ['N'],
                                                     'q18': ['N'],
                                                     'q19': ['N'],
                                                     'q2': ['Y'],
                                                     'q20': ['N'],
                                                     'q21': ['skip'],
                                                     'q22': ['skip'],
                                                     'q23': ['skip'],
                                                     'q24': ['skip'],
                                                     'q25': ['skip'],
                                                     'q26': ['skip'],
                                                     'q27': ['skip'],
                                                     'q28': ['skip'],
                                                     'q29': ['skip'],
                                                     'q3': ['Y'],
                                                     'q30': ['skip'],
                                                     'q31': ['skip'],
                                                     'q32': ['skip'],
                                                     'q33': ['skip'],
                                                     'q34': ['skip'],
                                                     'q35': ['skip'],
                                                     'q36': ['skip'],
                                                     'q37': ['skip'],
                                                     'q4': ['N'],
                                                     'q5': ['Y'],
                                                     'q6': ['Y'],
                                                     'q7': ['N'],
                                                     'q8': ['N'],
                                                     'q9': ['N']},
                               'Social-Emotional Scale': {   'ceiling': 'Pass',
                                                             'q1': ['Y'],
                                                             'q10': ['Y'],
                                                             'q11': ['N'],
                                                             'q12': ['N'],
                                                             'q13': ['N'],
                                                             'q14': ['N'],
                                                             'q15': ['N'],
                                                             'q16': ['N'],
                                                             'q17': ['N'],
                                                             'q18': ['N'],
                                                             'q19': ['N'],
                                                             'q2': ['Y'],
                                                             'q20': ['N'],
                                                             'q21': ['skip'],
                                                             'q22': ['skip'],
                                                             'q23': ['skip'],
                                                             'q24': ['skip'],
                                                             'q25': ['skip'],
                                                             'q26': ['skip'],
                                                             'q27': ['skip'],
                                                             'q28': ['skip'],
                                                             'q29': ['skip'],
                                                             'q3': ['Y'],
                                                             'q30': ['skip'],
                                                             'q31': ['skip'],
                                                             'q32': ['skip'],
                                                             'q33': ['skip'],
                                                             'q34': ['skip'],
                                                             'q35': ['skip'],
                                                             'q36': ['skip'],
                                                             'q4': ['Y'],
                                                             'q5': ['N'],
                                                             'q6': ['Y'],
                                                             'q7': ['N'],
                                                             'q8': ['Y'],
                                                             'q9': ['N']}}

def runTestModule(kwargs):
# def runTestModule(env="uat", headless=False, randomResponse=False, directory=None, logToFile=False, logName=None, uploadToS3=False, username=None, password=None):
# def runTestModule(env="uat", headless=False, randomResponse=False, directory=None, input=None, logToFile=False, waitTime=None):
    try:
        try:
            username = kwargs.pop('username')
        except:
            username = None
        
        if username is not None:
            testInfo['username'] = username
        
        try:
            password = kwargs.pop('password')
        except:
            password = None
        
        if password is not None:
            testInfo['password'] = password
        
        try:
            directory = kwargs.pop('directory')
        except:
            directory = None
        
        if directory is None or directory == 'None' or directory == '':
            directory = str(os.getcwd())
        
        try:
            logName = kwargs.pop('logName')
        except:
            logName = None
        
        if logName is None:
            logName = str(os.path.splitext(os.path.basename(str(__file__)))[0])
            
        logNameStamped = str(logName) + (time.strftime("_%F_%T", time.gmtime())).replace(":", "-")

        try:
            if not os.path.isdir(os.path.join(str(directory), str(logNameStamped))):
                os.mkdir(os.path.join(str(directory), str(logNameStamped)))
            
            outputDirectory = os.path.join(str(directory), str(logNameStamped))    
        except:
            logging.exception("Unable to create sub-directory for test case " + str(logNameStamped) + "! Outputting to specified directory instead")
            outputDirectory = str(directory)
        
        try:
            logToFile = bool(kwargs.pop('logToFile'))
        except:
            logToFile = False
        
        try:
            env = kwargs.pop('env')
        except:
            env = "uat"
        
        try:
            headless = kwargs.pop('headless')
        except:
            headless = None
            
        try:
            randomResponse = kwargs.pop('random')
        except:
            randomResponse = None

        if logToFile:
            logging.warning("Setting up logfile at " + os.path.join(str(outputDirectory), str(logNameStamped)+'.log'))
            loggingSetup(output=os.path.join(str(outputDirectory), str(logNameStamped)+'.log'))
        else:
            loggingSetup()
            
        logger = logging.getLogger(str(logNameStamped))
        
        logger.info("Specified output directory is: " + str(outputDirectory))
        runTest(env=env, headless=headless, randomResponse=randomResponse, directory=str(outputDirectory), logName=logger)
        
        # if logToFile:
            # with open(os.path.join(os.path.join(str(directory), str(logName)), str(logName + (time.strftime("_%F_%T", time.gmtime())).replace(":", "-") + ".txt")), 'w', encoding='utf-8') as f:
                # with redirect_stdout(f), redirect_stderr(f):
                    # # runTest(env=env, headless=headless, randomResponse=randomResponse, directory=str(os.path.join(str(directory), str(logName))), input=input, waitTime=waitTime)
                    # loggingPrint("Specified output directory is: " + str(directory))
                    # runTest(env=env, headless=headless, randomResponse=randomResponse, directory=os.path.join(str(directory), str(logName)))
        # else:
            # loggingPrint("Specified output directory is: " + str(directory))
            # runTest(env=env, headless=headless, randomResponse=randomResponse, directory=os.path.join(str(directory), str(logName)))
    finally:    
        try:
            uploadToS3 = bool(kwargs.pop('uploadToS3')) and 'boto3' in sys.modules
        except:
            uploadToS3 = False
        
        try:
            uploadParentDirectory = bool(kwargs.pop('uploadParentDirectory'))
        except:
            uploadParentDirectory = False
        
        if uploadToS3:
            s3 = boto3.resource('s3', region_name='us-west-2')
            bucket = s3.Bucket(uploadBucket)
            
        for subdir, dirs, files in os.walk(str(outputDirectory)):
            for file in files:
                full_path = os.path.join(subdir, file)
                # sometimes downloading a file takes long enough that Chrome doesn't get to rename
                # so we'll clean that up manually
                if os.path.splitext(str(file))[1] == '.crdownload':
                    os.rename(full_path, os.path.splitext(full_path)[0])
                if uploadToS3:
                    with open(full_path, 'rb') as data:
                        mimetypes.add_type('text/plain', '.log')
                        contentType = mimetypes.guess_type(full_path)[0]
                        if 'text' in contentType:
                            # we're explicitly writing all of our text files in UTF-8, so we're confident in this
                            contentType = contentType + '; charset=utf-8'
                        # bucket.put_object(Key=str("output/oes-1.0-automation/" + str(env) + "/" + os.path.basename(directory) + "/" + str(logNameStamped) + "/" + file), Body=data, ContentType=contentType)
                        if uploadParentDirectory:
                            uploadKey = str("output/oes-1.0-automation/" + str(env) + "/" + todaysDate.strftime("%m-%d-%Y") + "/" + os.path.basename(directory) + "/" + str(logNameStamped) + "/" + file)
                        else:
                            uploadKey = str("output/oes-1.0-automation/" + str(env) + "/" + todaysDate.strftime("%m-%d-%Y") + "/" + str(logNameStamped) + "/" + file)
                        bucket.put_object(Key=urllib.parse.quote(uploadKey), Body=data, ContentType=contentType)
                        logger.warning("Files uploaded to S3 at: s3://" + uploadBucket + "/" + uploadKey)

def runTest(env="uat", headless=False, randomResponse=False, directory=None, logName=None):

    if logName is None:
        logName = os.path.join(str(directory), os.path.basename(str(directory)), ".log")

    try:
        username = testInfo['username']
        if username == '':
            username = None
    except:
        username = None
    
    try:
        password = testInfo['password']
        if password == '':
            password = None
    except:
        password = None
    
    if env=="staging":
        loginUrl = "https://platform.stage.wpspublish.com"
    elif env=="uat":
        loginUrl = "https://practitioner-uat.wpspublish.io"
    elif env=="qa":
        loginUrl = "https://practitioner-qa.wpspublish.io"
    elif env=="prod":
        loginUrl = "https://platform.wpspublish.com"
    elif env=="dev":
        loginUrl = "https://practitioner-dev.wpspublish.io"
    elif env=="dev2":
        loginUrl = "https://practitioner-dev2.wpspublish.io"
    elif env=="dev1":
        loginUrl = "https://practitioner-dev1.wpspublish.io"
    elif env=="qa1":
        loginUrl = "https://practitioner-qa1.wpspublish.io"
    elif env=="uat1":
        loginUrl = "https://practitioner-uat1.wpspublish.io"
    elif env=="perf":
        loginUrl = "https://platform.perf.wpspublish.com"
    else:
        loginUrl = env
        
    Prac = oesPractitioner(loginUrl, username=username, password=password, logName=logName)
    logger = Prac.logger
    Prac.headless = headless
    if directory is None or directory == 'None' or directory == '':
        Prac.download_dir = str(os.getcwd())
    else:
        Prac.download_dir = str(directory)
    
    try:
        Prac.setUp()

        Prac.login()
        completedForm1 = ''
        completedForm1 = completeAssessmentForm(env, headless, randomResponse, directory, Prac=Prac)
        completedForm1 = Prac.getFormIdFromAdministrationFormGUID(administrationFormGUID=completedForm1)
        Prac.logout()
        
        Prac.tearDown()
        Prac.setUp()
        
        Prac.login()
        completedForm2 = ''
        completedForm2 = completeAssessmentForm(env, headless, randomResponse, directory, Prac=Prac)
        completedForm2 = Prac.getFormIdFromAdministrationFormGUID(administrationFormGUID=completedForm2)

        if (completedForm1 is not None and completedForm1 != '') and (completedForm2 is not None and completedForm2 != ''):
            try:
                Prac.generateReport(reportType='Parent/Caregiver', formIds=[completedForm1], reportInformation={'title': None, 'description': None})
            except:
                logger.error("Failed to generate Parent/Caregiver report!!!")
                
            Prac.browser.refresh()
            
            try:
                Prac.generateReport(reportType='Intervention', formIds=[completedForm1], reportInformation={'title': None, 'description': None, 'questions': [['Physical', '4'],
                         ['Physical', '7'],
                         ['Physical', '11'],
                         ['Adaptive Behavior', '10'],
                         ['Adaptive Behavior', '38'],
                         ['Social-Emotional', '11'],
                         ['Social-Emotional', '14'],
                         ['Cognitive', '19'],
                         ['Cognitive', '20'],
                         ['Cognitive', '25'],
                         ['Communication', '18'],
                         ['Communication', '19'],
                         ['Communication', '21']]})
            except:
                logger.error("Failed to generate Intervention report!!!")
                
            Prac.browser.refresh()
            
            try:
                Prac.generateReport(reportType='Intervention', formIds=[completedForm1], reportInformation={'title': None, 'description': None, 'questions': "Select All"})
            except:
                logger.error("Failed to generate Intervention report!!!")
                
            Prac.browser.refresh()
            
            try:
                Prac.generateReport(reportType='Rater Comparison', formIds=[completedForm1, completedForm2], reportInformation={'title': None, 'description': None, 'formType': "Standard"})
            except:
                logger.error("Failed to generate Rater Comparison report!!!")
                
            Prac.browser.refresh()
            
            try:
                Prac.generateReport(reportType='Progress', formIds=[completedForm1, completedForm2], reportInformation={'title': None, 'description': None})
            except:
                logger.error("Failed to generate Progress report!!!")
                
        else:
            logger.error('Failed to get all necessary form IDs!!!')
            logger.error("Completed Form 1: " + str(completedForm1))
            logger.error("Completed Form 2: " + str(completedForm2))
            raise
    except:
        try:
            try:
                logger.exception("Regression failed!!!")
            except:
                logging.exception("Regression failed!!!")
            Prac.browser.save_screenshot(os.path.join(str(directory), "regression_failed_" + (time.strftime("_%F_%T", time.gmtime())).replace(":", "-") + ".png"))
        except:
            logging.exception("Saving screenshot failed!!!")
    finally:
        Prac.logout()
        Prac.tearDown()

def completeAssessmentForm(env="uat", headless=False, randomResponse=False, directory=None, Prac=None):
# def runTest(env="uat", headless=False, randomResponse=False, directory=None, input=None, waitTime=None):
    
    logger = Prac.logger
    
    if headless:
        logger.info("Running in headless mode")
    else:
        logger.info("Running in display mode")
    
    if randomResponse:
        logger.info("Running in random response mode")
    else:
        logger.info("Running in set response mode")

    try:
        try:
            if testInfo['administrationdate'] is None or testInfo['administrationdate'] == '' or testInfo['administrationdate'] == 'None':
                logger.warning("Provided Administration Date is empty string, setting to current date in Pacific timezone!!!")
                administrationDate = pytz.utc.localize(dt=datetime.utcnow()).astimezone(pytz.timezone("America/Los_Angeles")).strftime("%m/%d/%Y")
            else:
                administrationDate = testInfo['administrationdate'].split(' ')
                for x in range(len(administrationDate)):
                    if administrationDate[x] in ['year', 'years', 'años', 'año']:
                        adminYears = administrationDate[x-1]
                    elif administrationDate[x] in ['months', 'month', 'meses', 'mes']:
                        adminMonths = administrationDate[x-1]
                    elif administrationDate[x] in ['days', 'day', 'dia', 'dias']:
                        adminDays = administrationDate[x-1]
                
                try:
                    administrationDate = '{d.month}/{d.day}/{d.year}'.format(d=adjustedDateCalculator(yearsAdjust=int(adminYears), monthsAdjust=int(adminMonths), daysAdjust=int(adminDays)))
                except:
                    administrationDate = '{d.month}/{d.day}/{d.year}'.format(d=adjustedDateCalculator(yearsAdjust=adminYears, monthsAdjust=adminMonths, daysAdjust=adminDays))
        except:
            logger.warning("Provided Administration Date is , setting to current date in Pacific timezone!!!")
            administrationDate = pytz.utc.localize(dt=datetime.utcnow()).astimezone(pytz.timezone("America/Los_Angeles")).strftime("%m/%d/%Y")

        logger.info("Administration date has been specified as " + str(administrationDate))
        
        clientAge = adjustedDateCalculator(yearsAdjust=int(int(testInfo['clientageyears'])+int(adminYears)), monthsAdjust=int(int(testInfo['clientagemonths'])+int(adminMonths)), daysAdjust=int(int(testInfo['clientagedays'])+int(adminDays)))
        
        try:
            clientYear = str(clientAge.year)
        except:
            clientYear = None
            
        try:           
            clientMonth = str(clientAge.month)
        except:
            clientMonth = None
            
        try:
            clientDay = str(clientAge.day)
        except:
            clientDay = None
        
        try:
            if testInfo['clientfirstname'] != '':
                clientFirstName = testInfo['clientfirstname']
            else:
                clientFirstName = randomString()
        except:
            clientFirstName = randomString()
            
        try:
            if testInfo['clientlastname'] != '':
                clientLastName = testInfo['clientlastname']
            else:
                clientLastName = randomString()
        except:
            clientLastName = randomString()
        
        try:
            if testInfo['clientcaseid'] != '':
                clientCaseID = testInfo['clientcaseid']
            else:
                clientCaseID = None
        except:
            clientCaseID = None
        
        try:
            if testInfo['clientgender'] != '':
                clientGender = (testInfo['clientgender'][0]).upper() + (testInfo['clientgender'][1:]).lower()
                if clientGender not in ["Female", "Male"]:
                    logger.warning("Invalid client gender option provided! Using random instead")
                    clientGender = None
            else:
                clientGender = None
        except:
            clientGender = None
            
        try:
            if testInfo['clientemail'] != '':
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                if(re.search(regex, testInfo['clientemail'])):  
                    clientEmail = testInfo['clientemail']
                else:  
                    logger.warning("Invalid client email provided! Using random instead")
                    clientEmail = None
            else:
                clientEmail = None
        except:
            clientEmail = None
            
        Prac.createNewClient(
        clientFirstName=clientFirstName,
        clientLastName=clientLastName,
        clientMonth=clientMonth, 
        clientDay=clientDay, 
        clientYear=clientYear,
        clientCaseID=clientCaseID,
        clientEmail=clientEmail,
        clientGender=clientGender
        )
        
        try:
            assessmentType = str(re.sub('[^0-9a-zA-Z]+', ' ', testInfo['assessmenttype'])).lower()
            if assessmentType != '':
                if assessmentType not in ['dp3', 'abas3', 'spm', 'spmp', 'spm2', 'ppascale', 'srs2', 'smalsi', 'casl2', 'opus', 'scq', 'arizona4', 'rcmas2', 'dbc2', 'piersharris3', 'rise', 'caps', 'dp4']:
                    logger.warning("Invalid assessment type provided! Using random instead")
                    assessmentType = None
            else:
                assessmentType = None
        except:
            assessmentType = None
        logger.info("Assessment type has been specified as " + str(assessmentType))        
        
        try:
            assessmentForm = testInfo['assessmentform']
            if assessmentForm == '':
                assessmentForm = None
        except:
            assessmentForm = None
            
        try:
            respondentName = testInfo['respondentname']
            if respondentName == '':
                respondentName = None
        except:
            respondentName = None
        
        try:
            Prac.administerAssessment(assessmentType=assessmentType, assessmentForm=assessmentForm, respondentName=respondentName, administrationDate=administrationDate)
        except:
            logger.error("Failed to administer assessment, attempting to navigate to client before retry...")
            Prac.browser.refresh()
            Prac.navigateToClient(str(clientFirstName + ' ' + clientLastName))
            Prac.administerAssessment(assessmentType=assessmentType, assessmentForm=assessmentForm, respondentName=respondentName, administrationDate=administrationDate)

        Prac.switchToRespondent()
        
        for section in argsListAssessment.keys():
            for field in argsListAssessment[section].keys():
                if field.lower() in ["administration date", "fecha de la administración", 'fecha de hoy']:
                    # administrationDate = argsListAssessment[section][field].split(' ')
                    # for x in range(len(administrationDate)):
                        # if administrationDate[x] in ['year', 'years', 'años', 'año']:
                            # adminYears = administrationDate[x-1]
                        # elif administrationDate[x] in ['months', 'month', 'meses', 'mes']:
                            # adminMonths = administrationDate[x-1]
                        # elif administrationDate[x] in ['days', 'day', 'dia', 'dias']:
                            # adminDays = administrationDate[x-1]
                    
                    #argsListAssessment[section][field] = adjustedDateCalculator(yearsAdjust=adminYears, monthsAdjust=adminMonths, daysAdjust=adminDays).strftime("%m/%d/%Y")
                    try:
                        adminDate = adjustedDateCalculator(yearsAdjust=int(adminYears), monthsAdjust=int(adminMonths), daysAdjust=int(adminDays))
                    except:
                        adminDate = adjustedDateCalculator(yearsAdjust=adminYears, monthsAdjust=adminMonths, daysAdjust=adminDays)
                    
                    if adminDate > todaysDate:
                        argsListAssessment[section][field] = '{d.month}/{d.day}/{d.year}'.format(d=todaysDate)
                    else:
                        argsListAssessment[section][field] = '{d.month}/{d.day}/{d.year}'.format(d=adminDate)
                elif field.lower() in ["date of birth", "fecha de nacimiento"]:
                    #argsListAssessment[section][field] = clientAge.strftime("%m/%d/%Y")
                    argsListAssessment[section][field] = '{d.month}/{d.day}/{d.year}'.format(d=clientAge)
                elif field.lower() in ['parent/caregiver’s name', 'parent/caregiver’s relationship to child']:
                    #argsListAssessment[section][field] = clientAge.strftime("%m/%d/%Y")
                    argsListAssessment[section][field] = randomString()
        
        if assessmentType is None:
            #browser, assessment="dp3", scoreOnly=False, singleView=False, logName=None):
            formResp = oesRespondent(browser=Prac.browser, logName=Prac.logger)
        else:
            formResp = oesRespondent(browser=Prac.browser, assessment=assessmentType, scoreOnly=Prac.scoreOnly, logName=Prac.logger)
        
        logger.info("Populating assessment form fields: " + str(argsListAssessment))
        formResp.navigateToQuestions(demoResponses=argsListAssessment, directory=str(directory))
        
        try:
            waitTime = testInfo['waittime']
            if waitTime == '':
                waitTime = 0.2
        except:
            waitTime = 0.2
        
        if randomResponse:
            formResp.completeAssessmentRandomly(waitTime=float(waitTime))
        else:
            if formResp.singleView:
                submitFound = False
                
                while not submitFound:
                    section = formResp.getCurrentSection()
                    try:
                        qNum = int(formResp.browser.execute_script("return singleSectionList[sectionCounter].ItemAndResponseList[sectionItemCounter].ItemNo;"))
                    except:
                        qNum = 0
                        
                    if qNum > 0:
                        sectionQuestions = questionList[section]
                        try:
                            questionResponseVals = questionList[section][str('q' + str(qNum))]
                            for questionResponseVal in questionResponseVals:
                                logger.info("Answering question number " + str(qNum) + " in section " + str(section) + " with response of " + str(questionResponseVal))
                                if str(questionResponseVal).lower() not in ["skip", "randomanswer"]:
                                    answerSuccess = formResp.answerQuestion(questionNumber=qNum, questionResponse=str(questionResponseVal))
                                    time.sleep(float(waitTime))
                                    if not answerSuccess:
                                        logger.warning("Failed to successfully confirm question response! Trying a second time...")
                                        time.sleep(float(waitTime))
                                        answerSuccess = formResp.answerQuestion(questionNumber=qNum, questionResponse=str(questionResponseVal))
                                        if not answerSuccess:
                                            logger.warning("Failed to successfully confirm question response! Trying one more time...")
                                            time.sleep(float(waitTime))
                                            answerSuccess = formResp.answerQuestion(questionNumber=qNum, questionResponse=str(questionResponseVal))
                                            if not answerSuccess:
                                                try:
                                                    logger.error("Failed to successfully confirm question response three times!!! Attempting to save screenshot...")
                                                    Prac.browser.save_screenshot(os.path.join(str(directory), "response_failed_" + str(qNum) + (time.strftime("_%F_%T", time.gmtime())).replace(":", "-") + ".png"))
                                                except:
                                                    logging.exception("Saving screenshot failed!!!")
                                elif questionResponseVal == "randomAnswer":
                                    formResp.answerQuestion(questionNumber=qNum)
                                    time.sleep(float(waitTime))
                        except:
                            logger.exception("Question/response is missing or invalid; answering question randomly instead!")
                            formResp.answerQuestion(questionNumber=qNum)
                            time.sleep(float(waitTime))

                    try:
                        pageNavButton = formResp.getPageNavButton("next")
                        if pageNavButton.get_attribute("value") in formResp.submitTranslations:
                            logger.info("Submit button found! Disregarding any remaining responses...")
                            submitFound = True
                        else:
                            logger.info("Navigating to next page...")
                            formResp.nextPage()
                    except:
                        if Prac.scoreOnly:
                            logger.info("Reached end of assessment! Disregarding any remaining responses...")
                            submitFound = True
                        else:
                            logger.warning("Error checking assessment form navigation; may not have loaded correctly!")

            else:
                for b in questionList.keys(): 
                    section = formResp.getCurrentSection()
                    logger.info("Answering questions in section: " + str(section))
                    
                    questions = sorted({int(k[1:]):v for k,v in questionList[section].items() if any (regex_match(k) for regex_match in [re.compile("^q[0-9]+$").match])}.keys())
                    q = 0
                    # submitFound = False
                    
                    while q < len(questions):
                        numQuestions = len(formResp.getQuestionsInPage())
                        logger.info("Number of questions in page: " + str(numQuestions))
                        if int(numQuestions) > 0:
                            for i in range(1, numQuestions+1):
                                q += 1
                                try:
                                    questionResponseVals = questionList[section][str('q' + str(questions[q-1]))]
                                    for questionResponseVal in questionResponseVals:
                                        logger.info("Answering question number " + str(q) + " with response of " + str(questionResponseVal))
                                        if str(questionResponseVal).lower() not in ["skip", "randomanswer"]:
                                            answerSuccess = formResp.answerQuestion(questionNumber=i, questionResponse=str(questionResponseVal))
                                            time.sleep(float(waitTime))
                                            if not answerSuccess:
                                                logger.warning("Failed to successfully confirm question response! Trying a second time...")
                                                time.sleep(float(waitTime))
                                                answerSuccess = formResp.answerQuestion(questionNumber=i, questionResponse=str(questionResponseVal))
                                                if not answerSuccess:
                                                    logger.warning("Failed to successfully confirm question response! Trying one more time...")
                                                    time.sleep(float(waitTime))
                                                    answerSuccess = formResp.answerQuestion(questionNumber=i, questionResponse=str(questionResponseVal))
                                                    if not answerSuccess:
                                                        try:
                                                            logger.error("Failed to successfully confirm question response three times!!! Attempting to save screenshot...")
                                                            Prac.browser.save_screenshot(os.path.join(str(directory), "response_failed_" + str(i) + (time.strftime("_%F_%T", time.gmtime())).replace(":", "-") + ".png"))
                                                        except:
                                                            logging.exception("Saving screenshot failed!!!")
                                        elif questionResponseVal == "randomAnswer":
                                            formResp.answerQuestion(questionNumber=i)
                                            time.sleep(float(waitTime))
                                except:
                                    logger.exception("Question/response is missing or invalid; answering question randomly instead!")
                                    formResp.answerQuestion(questionNumber=i)
                                    time.sleep(float(waitTime))
                        else:
                            logger.info("No questions found on page")
                        
                        try:
                            pageNavButton = formResp.getPageNavButton("next")
                            if pageNavButton.get_attribute("value") in formResp.submitTranslations:
                                logger.info("Submit button found! Disregarding any remaining responses...")
                                # submitFound = True
                            else:
                                logger.info("Navigating to next page...")
                                formResp.nextPage()
                        except:
                            if Prac.scoreOnly:
                                logger.info("Reached end of assessment! Disregarding any remaining responses...")
                                # submitFound = True
                            else:
                                logger.warning("Error checking assessment form navigation; may not have loaded correctly!")
                        finally:
                            q += len(questions)
            
        if not Prac.scoreOnly:
            formResp.submit()
            
        formResp.browser.close()
        
        Prac.switchToPractitioner()
        Prac.browser.refresh()
        
        try:
            try:
                validateForm = testInfo['validateform']
                if validateForm == '' or validateForm is None:
                    validateForm = True
            except:
                validateForm = True
                
            if validateForm:
                try:
                    validateFormMessage = testInfo['validateformmessage']
                    if validateFormMessage == '':
                        validateFormMessage = None
                except:
                    validateFormMessage = None
                    
                Prac.selectByAdministrationFormGUID(administrationFormGUID=formResp.administrationFormGUID)
                
                # if Prac.scoreOnly:
                    # try:
                        # Prac.selectPendingForm(id=formResp.administrationFormGUID)
                    # except:
                        # Prac.selectPendingForm(formEntry=-1)
                # else:
                    # try:
                        # Prac.selectCompleteForm(id=formResp.administrationFormGUID)
                    # except:
                        # Prac.selectCompleteForm(formEntry=0)
                
                Prac.validateForm(expectedResponse=validateFormMessage, demoResponses=argsListValidation)
        except:
            logger.warning("Validation encountered an error, refreshing page and attempting one more time...")
            try:
                Prac.browser.refresh()
                
                Prac.selectByAdministrationFormGUID(administrationFormGUID=formResp.administrationFormGUID)
                        
                if validateForm:
                    Prac.validateForm(expectedResponse=validateFormMessage, demoResponses=argsListValidation, medianValues=medianValues)
            except:                      
                try:
                    logger.error("Validation failed!!!")
                    Prac.browser.save_screenshot(os.path.join(str(directory), "regression_validation_failed_" + (time.strftime("_%F_%T", time.gmtime())).replace(":", "-") + ".png"))
                except:
                    logging.exception("Saving screenshot failed!!!")

            
        try:
            try:
                scoreForm = bool(testInfo['scoreform'])
                if scoreForm == '' or scoreForm is None:
                    scoreForm = False
            except:
                scoreForm = False
                
            if scoreForm:
                Prac.scoreForm(expectedResponse=validateFormMessage, demoResponses=argsListValidation)
        except:
            logger.warning("Scoring encountered an error, refreshing page and attempting one more time...")
            try:
                Prac.browser.refresh()
                
                sleepInt = random.randint(5, 10)
                logger.warning("Randomizing sleep to avoid deadlock, num. seconds: " + str(sleepInt))
                time.sleep(int(sleepInt))
                
                Prac.selectByAdministrationFormGUID(administrationFormGUID=formResp.administrationFormGUID)
                        
                if scoreForm:
                    # Trying to randomize the wait time a bit to avoid another possible deadlock...
                    sleepInt = random.randint(5, 10)
                    logger.warning("Randomizing sleep to avoid deadlock, num. seconds: " + str(sleepInt))
                    time.sleep(int(sleepInt))
                    Prac.scoreForm(expectedResponse=validateFormMessage, demoResponses=argsListValidation)
            except:
                try:
                    logger.error("Scoring failed!!!")
                    Prac.browser.save_screenshot(os.path.join(str(directory), str(testInfo['assessmenttype']) + "_regression_failed_save_" + (time.strftime("_%F_%T", time.gmtime())).replace(":", "-") + ".png"))
                except:
                    logging.exception("Saving screenshot failed!!!")
                
                try:
                    form = Prac.browser.find_element(By.XPATH, "//*[@class='cannotScoreErrorMsg']")
                except:
                    form = None
                
                if form is not None:
                    logger.error("Licensing message has appeared! Please add licenses for this form and re-run!")
                    raise

        try:
            try:
                isDeleteClient = testInfo['deleteclient']
                if isDeleteClient == '' or isDeleteClient is None:
                    isDeleteClient = False
            except:
                isDeleteClient = False
                
            if isDeleteClient:
                Prac.deleteClient(clientFirstName + " " + clientLastName)
        except:
            logger.warning("Deleting client failed!!!")
        
        return formResp.administrationFormGUID
        
    except Exception as err:
        try:
            logger.exception("Fatal error attempting to complete assessment!!!")
        except:
            logging.exception("Fatal error attempting to complete assessment!!!")
        Prac.browser.save_screenshot(os.path.join(str(directory), "regression_exception_" + (time.strftime("_%F_%T", time.gmtime())).replace(":", "-") + ".png"))
        Prac.logout()
        Prac.tearDown()
        raise

    # loggingPrint("Test completed!\r\n")
    
if __name__ == "__main__":
    
    short_options = "he:rd:lu"
    long_options = ["headless", "env=", "random", "directory=", "log-to-file", "upload", "username=", "password="]
    # short_options = "he:rd:i:lw:"
    # long_options = ["headless", "env=", "random", "directory=", "input=", "log-to-file", "wait-time="]
    # "output=",
    
    # Get full command-line arguments
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    env = "uat"
    headless = False
    randomResponse = False
    directory = None
    logToFile = False
    uploadToS3 = False
    username = None
    password = None
# waitTime = None
    
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
        sys.exit(2)
    
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--headless"):
            headless = True
        elif current_argument in ("-e", "--env"):
            env = current_value
        elif current_argument in ("-d", "--directory"):
            directory = current_value
        # elif current_argument in ("-w", "--wait-time"):
            # waitTime = current_value
        elif current_argument in ("-r", "--random"):
            randomResponse = True
        elif current_argument in ("-l", "--log-to-file"):
            logToFile = True
        elif current_argument in ("-u", "--upload") and 'boto3' in sys.modules:
            uploadToS3= True
        elif current_argument in ("--username"):
            username = str(current_value)
        elif current_argument in ("--password"):
            password = str(current_value)

            #print (("Enabling special output mode (%s)") % (current_value))

    if directory is None or directory == 'None' or directory == '':
        directory = str(os.getcwd())
        
    testModuleArgs = {'env': env, 'headless': headless, 'random': randomResponse, 'directory': str(directory), 'logToFile': logToFile, 'uploadToS3': uploadToS3, 'username': username, 'password': password}
    
    if uploadToS3:
        logging.warning("S3 upload is currently enabled")
        # s3 = boto3.resource('s3', region_name='us-west-2')
        # bucket = s3.Bucket(uploadBucket)
        # bucket.put_object(Key=str("output/oes-1.0-automation/" + str(env) + "/" + os.path.basename(directory) + "/"))
    
    if logToFile:
        logging.warning("Logging to file is enabled; each test case will log to file and console")
    
    if headless:
        logging.warning("Headless mode is enabled; browser sessions will not be displayed!")
    
    runTestModule(testModuleArgs)
