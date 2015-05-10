__author__ = 'GeoffreyWest'

import arcpy
import logging
import logging
import logging.handlers

SCDE5556= "C:\Users\Administrator\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to localhost_SCData_sa.sde\SCData.DBO.SO_SC_55_56"
SOSC = "C:\Users\Administrator\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to localhost_SCData_sa.sde\SCData.DBO.SO_SC"
Clause=  "PlannedDate = CONVERT(DATE, GETDATE()) AND RESOLUTION_CODE  IN ( '55', '56')"

# Clause2= "NUMBERCYLA > 'SR07885524' AND RESOLUTION_CODE  IN ( '55', '56')"

Copy = "C:\CleanStreets_55_56.gdb\Copied_55_56"

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

gm = TlsSMTPHandler(("smtp.gmail.com", 587), 'geoffreywestgis@gmail.com', ['geoffreywestgis@gmail.com'], 'Error in Clean Streets Append Script Found!', ('geoffreywestgis@gmail.com', 'pythonheat1'))
gm.setLevel(logging.ERROR)

logger.addHandler(gm)




try:

    if arcpy.Exists(Copy):
                arcpy.Delete_management(Copy)

    arcpy.FeatureClassToFeatureClass_conversion(SOSC, "C:\CleanStreets_55_56.gdb", "Copied_55_56", Clause)

    arcpy.AddField_management(Copy, "DATE", "DATE")

    dateExpression = "Date"

    arcpy.CalculateField_management(Copy, "DATE", dateExpression)

    fname = "Zero"
    Zero = 0
    arcpy.AddField_management(Copy, "Zero", "TEXT")
    arcpy.CalculateField_management(Copy, fname, Zero)
    arcpy.CalculateField_management(Copy, "Prior_RESOLUTION_CODE", "RESOLUTION_CODE")
    arcpy.CalculateField_management(Copy, "RESOLUTION_CODE", "Zero")

    arcpy.CalculateField_management(Copy, fname, Zero)

    arcpy.Append_management(Copy, SCDE5556, "NO_TEST")

    print "success"

except:
    logger.exception("Something has gone wrong!")













