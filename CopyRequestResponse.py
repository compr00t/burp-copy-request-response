from burp import IBurpExtender, IContextMenuFactory, IHttpRequestResponse
from java.io import PrintWriter
from java.util import ArrayList
from javax.swing import JMenuItem
from java.awt import Toolkit
from java.awt.datatransfer import StringSelection
from javax.swing import JOptionPane
from urllib import unquote
import subprocess
import tempfile
import threading
import time

class BurpExtender(IBurpExtender, IContextMenuFactory, IHttpRequestResponse):

    CUT_TEXT = [ord(c) for c in "[...]"]

    def registerExtenderCallbacks(self, callbacks):
        callbacks.setExtensionName("Copy HTTP Request & Response")

        stdout = PrintWriter(callbacks.getStdout(), True)
        stderr = PrintWriter(callbacks.getStderr(), True)

        self.helpers = callbacks.getHelpers()
        self.callbacks = callbacks
        callbacks.registerContextMenuFactory(self)

    # Implement IContextMenuFactory
    def createMenuItems(self, invocation):
        self.context = invocation
        menuList = ArrayList()

        menuList.add(JMenuItem("Copy Request & Response",
                actionPerformed=self.copyRequestPartialResponsePartial))
        return menuList

    def copyRequestPartialResponsePartial(self, event):
        httpTraffic = self.context.getSelectedMessages()[0]
        httpRequest = httpTraffic.getRequest()
        httpResponse = httpTraffic.getResponse()
        httpRequestBodyOffset = self.helpers.analyzeRequest(httpRequest).getBodyOffset()
        httpResponseBodyOffset = self.helpers.analyzeResponse(httpResponse).getBodyOffset()

        httpRequestHeader = httpRequest[0:httpRequestBodyOffset]
        httpRequestBody = httpRequest[httpRequestBodyOffset:]

        httpResponseHeader = httpResponse[0:httpResponseBodyOffset]
        httpResponseBody = httpResponse[httpResponseBodyOffset:]

        # Convert from byte array to array of strings
        httpRequestHeader = self.helpers.bytesToString(httpRequestHeader).replace('\r\n', '\n').splitlines()
        httpRequestBody = self.helpers.bytesToString(httpRequestBody).replace('\r\n', '\n')

        httpResponseHeader = self.helpers.bytesToString(httpResponseHeader).replace('\r\n', '\n').splitlines()
        httpResponseBody = self.helpers.bytesToString(httpResponseBody).replace('\r\n', '\n')

        # Get first line
        httpRequestHeaderFiltered = httpRequestHeader[0]

        for i in httpRequestHeader:
            if i.startswith('Host'):
                httpRequestHeaderFiltered += "\r\n"
                httpRequestHeaderFiltered += i
            elif i.startswith('Connection'):
                httpRequestHeaderFiltered += "\r\n"
                httpRequestHeaderFiltered += i
            elif i.startswith('Content-Type'):
                httpRequestHeaderFiltered += "\r\n"
                httpRequestHeaderFiltered += i
            elif i.startswith('Cookie'):
                httpRequestHeaderFiltered += "\r\n"
                httpRequestHeaderFiltered += i

        if not httpRequestBody:
            httpRequest = httpRequestHeaderFiltered
        else:
            httpRequest = httpRequestHeaderFiltered + "\r\n\r\n" + httpRequestBody

        httpRequest = unquote(httpRequest).decode('utf8')

        httpResponseHeaderFiltered = httpResponseHeader[0]

        for i in httpResponseHeader:
            if i.startswith('Host'):
                httpResponseHeaderFiltered += "\r\n"
                httpResponseHeaderFiltered += i
            elif i.startswith('Connection'):
                httpResponseHeaderFiltered += "\r\n"
                httpResponseHeaderFiltered += i
            elif i.startswith('Content-Type'):
                httpResponseHeaderFiltered += "\r\n"
                httpResponseHeaderFiltered += i
            elif i.startswith('Cookie'):
                httpResponseHeaderFiltered += "\r\n"
                httpResponseHeaderFiltered += i

        if not httpResponseBody:
            httpResponse = httpResponseHeaderFiltered
        else:
            httpResponse = httpResponseHeaderFiltered + "\r\n  \r\n" + httpResponseBody

        httpResponse = unquote(httpResponse).decode('utf8')

        data = "Als Proof of Concept kann dazu nachfolgender Request genutzt werden:\r\n  \r\n```\r\n" + httpRequest + "\r\n```" + "\r\n  \r\nDie Applikation beantwortet dies daraufhin mit folgender Response:\r\n  \r\n" + "```\r\n" + httpResponse + "\r\n```"
        self.copyToClipboard(data)

    def copyToClipboard(self, data):
        systemClipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
        transferText = StringSelection(data)
        systemClipboard.setContents(transferText, None)
