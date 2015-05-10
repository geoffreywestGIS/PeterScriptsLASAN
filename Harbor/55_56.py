__author__ = 'GeoffreyWest'


__author__ = 'Geoffrey West'
#Peter2Email
import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import logging
import logging.handlers



class TlsSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            import string # for tls add this line
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            string.join(self.toaddrs, ","),
                            self.getSubject(record),
                            formatdate(), msg)
            if self.username:
                smtp.ehlo() # for tls add this line
                smtp.starttls() # for tls add this line
                smtp.ehlo() # for tls add this line
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

logger = logging.getLogger()

gm = TlsSMTPHandler(("smtp.gmail.com", 587), 'geoffreywestgis@gmail.com', ['geoffreywestgis@gmail.com'], 'Peter Error West LA found!', ('geoffreywestgis@gmail.com', 'pythonheat1'))
gm.setLevel(logging.ERROR)

logger.addHandler(gm)





try:
    def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
        assert type(send_to)==list
        assert type(files)==list

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach( MIMEText(text) )

        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(f,"rb").read() )
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

        #Set Email smtp parameters
        smtp = smtplib.SMTP('smtp.gmail.com:587')
        smtp.starttls()
        smtp.login('geoffreywestgis@gmail.com', 'pythonheat1')
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()



    #Send Field to Text File
    import arcpy

    #Define Local Parameters
    SDEFeatureClass = "C:\Users\Administrator\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to localhost_SCData_sa.sde\SCData.DBO.SO_SC_55_56"
    LocalFGDB = "C:\PeterText.gdb"
    PeterTable = "C:\PeterText.gdb\Table_55_56"
    Outable = "Table_55_56"
    expression = 'Trim([NUMBERCYLA]) & ",SB,"& Trim([RESOLUTION_CODE] ) & ",,,CSP Truck,CleanStreets, "&",Driver,"& [DATE] &","'
    #Selection Query
    Harborselection = "PtrText IS NULL AND RESOLUTION_CODE <> '0' AND RESOLUTION_CODE IS NOT NULL  AND Prior_RESOLUTION_CODE = '56'"


    #Deletes old FC
    # if arcpy.Exists(row.getValue(PeterTable)):
    #     arcpy.Delete_management(row.getValue(PeterTable))

    if arcpy.Exists(PeterTable):
        arcpy.Delete_management(PeterTable)

    #Sends Feature Class to Table with Where Clause
    arcpy.TableToTable_conversion(SDEFeatureClass, LocalFGDB, Outable, Harborselection)

    arcpy.AddField_management(PeterTable, "DATE", "DATE")
    arcpy.AddField_management(PeterTable, "CleanStreetsPeter", "TEXT")

    dateExpression = "Date"
    arcpy.CalculateField_management(PeterTable, "DATE", dateExpression)

    #Calculates Field with expression for Peter Text File
    arcpy.CalculateField_management(PeterTable, "CleanStreetsPeter", expression)

    #Search Cursor to extract Peter Text Field
    myOutputFile = open("C:\PeterScripts\CleanStreets\Peter.txt", 'w')
    rows = arcpy.da.SearchCursor(PeterTable, ["CleanStreetsPeter"])



    for row in rows:
        myOutputFile.write(str(row[0]) + '\n')
    del row, rows
    myOutputFile.close()


    import time
    date= time.strftime("%m/%d/%Y")
    print date

    ATTACHMENTS = ["C:\PeterScripts\CleanStreets\Peter.txt"]
    send_from='geoffreywestgis@gmail.com'
    send_to=['geoffreywestgis@gmail.com','sal.aguilar@lacity.org']
    subject ='Clean Streets Peter.Txt' + ' ' + date
    text = 'Attached' + ' ' + date
    send_mail(send_from, send_to, subject, text, files=ATTACHMENTS)

except:
    logger.exception("Something has gone wrong!")





