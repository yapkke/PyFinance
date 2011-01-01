"""Handle Quicken XML files
"""
import datetime
import pyfinance.pyf as pyf

class tag_transaction:
    """Tagged statement transaction
    with format
       <Tag>Value<Tag>Value...

    @author ykk
    @date Dec 2010
    """
    def __init__(self, stmttrn):
        """Initialize
        """
        self.__content = {}
        for x in stmttrn.replace('\r','').\
                replace('\n','').split("<"):
            y = x.split(">")
            if (len(x) == 0):
                pass
            elif (len(y) == 2):
                self.__content[y[0]] = y[1]
            else:
                print "Warning: Unknown tag/value ="+x

    def get(self, tag):
        """Get value of tag
        """
        try:
            return self.__content[tag]
        except KeyError:
            return None

    def __str__(self):
        """Return string
        """
        return str(self.__content)

class qfx(pyf.account):
    """Quicken OFX file (QFX)
     
    @author ykk
    @date Dec 2010
    """
    def __init__(self, filename):
        """Initialize
        """
        pyf.account.__init__(self)

        #Read file
        content = ""
        fileRef = open(filename, "r")
        for line in fileRef:
            content += line
        fileRef.close()
        
        #Extract content
        self._content = []
        content = content[content.find("<STMTTRN>"):]
        content = content[:content.rfind("</STMTTRN>")+10]
        while (len(content) != 0):
            i = content.find("</STMTTRN>")
            self._content.append(tag_transaction(content[9:i]))
            content = content[i+10:]

class CitiCardQFX(qfx):
    """QFX from CitiCard

    @author ykk
    @date Dec 2010
    """
    def __init__(self, filename):
        """Initialize
        """
        qfx.__init__(self,filename)

        for x in self._content:
            self.transactions.append(pyf.transaction(\
                    self.__getdate(x.get("DTPOSTED")),
                    float(x.get("TRNAMT")),
                    x.get("NAME"),
                    x.get("TRNTYPE")))

    def __getdate(self, string):
        """Parse date
        """
        return datetime.date(int(string[0:4]),
                             int(string[4:6]),
                             int(string[6:8]))
                             
class ChaseQFX(qfx):
    """QFX from Chase

    @author ykk
    @date Jan 2010
    """
    def __init__(self, filename):
        """Initialize
        """
        qfx.__init__(self,filename)

        for x in self._content:
            self.transactions.append(pyf.transaction(\
                    self.__getdate(x.get("DTPOSTED")),
                    float(x.get("TRNAMT")),
                    x.get("NAME"),
                    x.get("TRNTYPE")))

    def __getdate(self, string):
        """Parse date
        """
        return datetime.date(int(string[0:4]),
                             int(string[4:6]),
                             int(string[6:8]))
                             
