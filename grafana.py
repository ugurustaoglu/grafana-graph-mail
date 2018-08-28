# -*- coding: latin5 -*-
import sys
sys.path.append("C:\\bim\\AvailabilityReport\\venv\\Lib\\site-packages")
import json
import requests
import time
import logging
import logging.handlers
import AvailabilityReport
import SendMail
import os
import datetime
from availability_logger import LoggerWriter

logger = logging.getLogger('AvailabilityGraphSender')
logger.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler("c:\\BIM\\AvailabilityGraphSender.log", maxBytes=5000000, backupCount=3)
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
sys.stdout = LoggerWriter(logger.debug)
sys.stderr = LoggerWriter(logger.warning)

logger.info('-------------------------------------------------------------------')
logger.info('---------------AvailabilityReport Script Started-------------------')
logger.info('-------------------------------------------------------------------')
current_milli_time = lambda: int(round(time.time() * 1000))
one_week_ago = current_milli_time() - 604800000
current_readable=(datetime.datetime.fromtimestamp(current_milli_time() / 1000.0).strftime('%d.%m'))
one_week_ago_readable=(datetime.datetime.fromtimestamp(one_week_ago/1000).strftime('%d.%m'))
week=one_week_ago_readable+"-"+current_readable

logger.info('Querying Database')
cursor = AvailabilityReport.connecttodb()
cursor.execute("SELECT ProjectName,MailAddress FROM xxx WHERE EmailFlag=1")
logger.info('Records Fetched')
for row in cursor.fetchall():
    ProjectName=row[0].strip()
    Emails=MailAddress=row[1].strip().split(";")
    logger.info('Getting Graphs For: '+ ProjectName)
    graphs = [2,6,10]
    graph_names =[]
    for graph_id in graphs:
        HOST = "http://xxx/render/d-solo/N7MIcPNmz/xxx?panelId="\
        +str(graph_id)+"&orgId=1&var-UserName="+ProjectName+"&var-environment=All&var-project=All&var-TestStep=All&" \
        "var-Endpoint=All&from="+str(one_week_ago)+"&to="+str(current_milli_time())+\
        "&width=500&height=250&tz=UTC%2B03%3A00"
        response = requests.get(HOST)
        if response.status_code == 200:
            graph_path="c:\\BIM\\AvailabilityReport\\"+ProjectName+"_"+str(graph_id)+".png"
            with open(graph_path, 'wb') as f:
                logger.info('Writing Graph To disk: ' +ProjectName+"_"+str(graph_id))
                f.write(response.content)
                logger.info('Graph Saved: ' +ProjectName+"_"+str(graph_id))
                graph_names.append(graph_path)

    SendMail.sendemail("xxx <xxx@xxx.com.tr>",Emails,graph_names,ProjectName,week)
cursor.close()
del cursor
