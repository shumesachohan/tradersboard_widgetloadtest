import datetime
import functools
import os
import json
import logging
import platform
import smtplib
from ssl import Options
import traceback
from typing import Counter
from urllib.parse import urlencode
import cv2
from firebase import upload_to_firebase
import numpy as np
import threading
import time
from email.message import EmailMessage
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# from login import video_filename

# from signup import video_signup_filename


# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
widget_video_filename = f"widget_test_run.avi"
# video_filename = f"trader_gpt_login_tests.avi"




# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# video_signup_filename = f"tradergpt_signupflow_tests.avi"


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"tradergpt_log_.log"

# firebase_video_url = upload_to_firebase(video_filename, f"videos/{video_filename}")
# firebase_video_url_signup = upload_to_firebase(video_signup_filename ,f'videos/{video_signup_filename}')



firebase_log_file = "https://restapipro-9a75a.appspot.com/logs/tradergpt_log.log"
firebase_network_upload ="https://restapipro-9a75a.appspot.com/networks/login_end_with_requests_and_console.json"
firebase_element_upload ="https://restapipro-9a75a.appspot.com/unfound_elements/missing_elements.csv"


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    



# def generate_testng_style_report_login(test_results, output_file="login_tests_report.html", video_url=firebase_video_url,log_file= firebase_log_file,network_file=firebase_network_upload,element_file=firebase_element_upload):
#     passed = sum(1 for r in test_results if r.get("status") == "PASS")
#     failed = sum(1 for r in test_results if r.get("status") == "FAIL")
    
#     chart_data = {
#         "labels": ["Passed", "Failed"],
#         "values": [passed, failed]
#     }

#     # Ensuring data is correctly formatted
#     chart_data = {
#         "labels": chart_data.get("labels", ["Passed", "Failed"]),
#         "values": chart_data.get("values", [0, 0])
#     }

#     chart_section = f"""
#     <div style="max-width: 300px; margin: 20px auto;">
#         <canvas id="resultChart" width="300" height="300"></canvas>
#     </div>
#     <script>
#         const ctx = document.getElementById('resultChart').getContext('2d');
#         new Chart(ctx, {{
#             type: 'doughnut',
#             data: {{
#                 labels: {json.dumps(chart_data["labels"])},
#                 datasets: [{{
#                     label: 'Test Summary',
#                     data: {json.dumps(chart_data["values"])},
#                     backgroundColor: ['#8BC34A', '#F44336'],
#                     borderWidth: 2,
#                     borderColor: '#ffffff',
#                     hoverOffset: 15
#                 }}]
#             }},
#             options: {{
#                 responsive: true,
#                 plugins: {{
#                     legend: {{
#                         position: 'bottom',
#                         labels: {{
#                             color: '#333',
#                             font: {{
#                                 size: 14
#                             }}
#                         }}
#                     }}
#                 }}
#             }}
#         }});
#     </script>
#     """

#     bugs_section = "<h2>❌ Failed Tests</h2><ul>"
#     for result in test_results:
#        if result.get("status") == "FAIL":

#         bugs_section += f"<li><b>{result['name']}</b>: {result.get('message', 'No message')}</li>"
#         bugs_section += "</ul>"


#     video_html = ""
#     if video_url:
#         video_html += f"""
#         <h3>🎥 Test Recording</h3>
#         <a href="{video_url}" target="_blank">Click here to watch the video</a><br><br>
#         """
    
#     if network_file:
#         if network_file.startswith("http"):
#             video_html += f"""
#             <h3>📄 Log File</h3>
#             <a href="{network_file}" target="_blank">Click here to view the log file</a><br><br>
#             """
#         elif os.path.exists(log_file):
#             with open(network_file, "r", encoding="utf-8") as lf:
#                 log_content = lf.read()
#                 video_html += f"""
#                 <h3>📄 Log File</h3>
#                 <pre style='max-height: 300px; overflow-y: auto; background: #eee; padding: 10px; border-radius: 5px;'>{log_content}</pre><br><br>
#                 """
#         else:
#             video_html += f"""
#             <h3>📄 Log Network File</h3>
#             <p style='color: red;'>Log file not found at the given path: {network_file}</p>
#             """

     
#         if log_file.startswith("http"):
#             video_html += f"""
#             <h3>📄 Log File</h3>
#             <a href="{log_file}" target="_blank">Click here to view the log file</a><br><br>
#             """
#         elif os.path.exists(log_file):
#             with open(log_file, "r", encoding="utf-8") as lf:
#                 log_content = lf.read()
#                 video_html += f"""
#                 <h3>📄 Log File</h3>
#                 <pre style='max-height: 300px; overflow-y: auto; background: #eee; padding: 10px; border-radius: 5px;'>{log_content}</pre><br><br>
#                 """
#         else:
#             video_html += f"""
#             <h3>📄 Log File</h3>
#             <p style='color: red;'>Log file not found at the given path: {log_file}</p>
#             """
            
            
#         if element_file.startswith("http"):
#             video_html += f"""
#             <h3>📄 Log File</h3>
#             <a href="{element_file}" target="_blank">Click here to view the unfound elements file</a><br><br>
#             """
#         elif os.path.exists(element_file):
#             with open(element_file, "r", encoding="utf-8") as lf:
#                 log_content = lf.read()
#                 video_html += f"""
#                 <h3>📄 Log File</h3>
#                 <pre style='max-height: 300px; overflow-y: auto; background: #eee; padding: 10px; border-radius: 5px;'>{log_content}</pre><br><br>
#                 """
#         else:
#             video_html += f"""
#             <h3>📄 Log File</h3>
#             <p style='color: red;'>Log file not found at the given path: {element_file}</p>
#             """

#     tests_section = "<h2>📋 All Test Results</h2>" + video_html
#     tests_section += "<table border='1' cellpadding='5'><tr><th>Test Name</th><th>Expected Output</th><th>Actual Output</th><th>Result</th><th>Duration (s)</th><th>Provided Data</th><th>Start Time</th><th>End Time</th><th>Description</th></tr>"

#     for result in test_results:
#         # Determine the result
#         expected_output = result.get('expected_output', 'N/A')
#         actual_output = result.get('actual_output', 'N/A')
#         result_boolean = "PASS" if expected_output == actual_output else "FAIL"

#         status_color = 'green' if result_boolean == "PASS" else 'red'
        
#         tests_section += f"""
#         <tr>
#             <td>{result['name']}</td>
#             <td>{expected_output}</td>
#             <td>{actual_output}</td>
#             <td style='color:{status_color}'>{result_boolean}</td>
#             <td>{result.get('duration', 0)}</td>
#             <td>{result.get('provided_data', '')}</td>
#             <td>{result.get('start_time')}</td>
#             <td>{result.get('end_time')}</td>
#             <td>{result.get('description', '')}</td>
#         </tr>
#         """
#     tests_section += "</table>"

#     html_content = f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#            <title>Business Avenue Test Report</title>
#         <link rel="icon" type="image/png" href="C:\projects\poc\WhatsApp Image 2025-05-09 at 10.28.57_4aae6d67.jpg">
#         <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#         <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&display=swap" rel="stylesheet">
#         <style>
#             body {{
#                 margin: 0;
#                 font-family: 'Poppins', sans-serif;
#                 background: #f7f9fc;
#             }}
#             #sidebar {{
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 width: 80px;
#                 height: 100%;
#                 background: #2f3542;
#                 padding-top: 30px;
#                 display: flex;
#                 flex-direction: column;
#                 align-items: center;
#             }}
#             #sidebar li {{
#                 font-size: 24px;
#                 padding: 20px 0;
#                 color: #ffffff;
#                 cursor: pointer;
#                 position: relative;
#             }}
#             #sidebar li:hover {{
#                 background: #57606f;
#                 width: 100%;
#                 text-align: center;
#             }}
#             #sidebar li::after {{
#                 content: attr(title);
#                 position: absolute;
#                 left: 90px;
#                 top: 10px;
#                 background: #2f3542;
#                 color: #fff;
#                 padding: 4px 10px;
#                 border-radius: 4px;
#                 opacity: 0;
#                 white-space: nowrap;
#                 pointer-events: none;
#                 transition: opacity 0.3s;
#             }}
#             #sidebar li:hover::after {{
#                 opacity: 1;
#             }}
#             #main {{
#                 margin-left: 100px;
#                 padding: 30px;
#             }}
#             .report-section {{
#                 display: none;
#                 animation: fadeIn 0.5s ease-in;
#             }}
#             @keyframes fadeIn {{
#                 from {{ opacity: 0; transform: translateY(10px); }}
#                 to {{ opacity: 1; transform: translateY(0); }}
#             }}
#             canvas {{
#                 background: #fff;
#                 border-radius: 15px;
#                 box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#             }}
#             h2, h3 {{
#                 color: #2c3e50;
#             }}
#             ul {{
#                 padding-left: 20px;
#             }}
#             li {{
#                 margin-bottom: 10px;
#             }}
#             table {{
#                 width: 100%;
#                 border-collapse: collapse;
#                 background: white;
#                 border-radius: 10px;
#                 box-shadow: 0 4px 10px rgba(0,0,0,0.05);
#                 overflow: hidden;
#             }}
#             table th, table td {{
#                 padding: 12px 15px;
#                 text-align: left;
#             }}
#             table th {{
#                 background-color: #f1f1f1;
#             }}
#             tr:nth-child(even) {{
#                 background-color: #f9f9f9;
#             }}
#             video {{
#                 border-radius: 12px;
#                 box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#             }}
#         </style>
#     </head>
#     <body>
    
#         <div id="sidebar">
#             <ul>
#                 <li onclick="showSection('systemInfo')" title="System Info">🛠️</li>
#                 <li onclick="showSection('testsSection')" title="Test Results">📋</li>
#                 <li onclick="showSection('chartSection')" title="Chart">📊</li>
#                 <li onclick="showSection('bugsSection')" title="Bugs">❌</li>
              
#             </ul>
#         </div>
#         <div id="main">
#             <div id="testsSection" class="report-section">{tests_section}</div>
#             <div id="chartSection" class="report-section">{chart_section}</div>
#             <div id="bugsSection" class="report-section">{bugs_section}</div>
#             <div id="systemInfo" class="report-section">
#                 <h3 style="text-align:center; margin-top: 40px;">🛠️ System Information</h3>
#                 <table border='1' cellpadding='5' style='margin: 0 auto; width: 80%; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); overflow: hidden;'>
#                     <tr><th>Property</th><th>Value</th></tr>
#                     <tr><td><strong>Tester</strong></td><td>Barira</td></tr>
#                     <tr><td><strong>Department</strong></td><td>Automation</td></tr>
#                     <tr><td><strong>Testing Website</strong></td><td>Buypass Business Avenue Login Flow</td></tr>
#                     <tr><td><strong>Browser</strong></td><td>Chrome</td></tr>
#                     <tr><td><strong>System</strong></td><td>Windows</td></tr>
#                 </table>
#             </div>
#         </div>

#         <script>
#             function showSection(id) {{
#                 document.querySelectorAll('.report-section').forEach(el => el.style.display = 'none');
#                 document.getElementById(id).style.display = 'block';
#             }}
#             // Default view
#             showSection('chartSection');
#         </script>
#     </body>
#     </html>
#     """

#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write(html_content)

#     print(f"✅ Report with video generated: {output_file}")
    
  
# def generate_testng_style_report_signup(test_results, output_file="signup_tests_report.html", video_url=firebase_video_url_signup,log_file= firebase_log_file,network_file=firebase_network_upload,element_file=firebase_element_upload):
#     passed = sum(1 for r in test_results if r.get("status") == "PASS")
#     failed = sum(1 for r in test_results if r.get("status") == "FAIL")
    
#     chart_data = {
#         "labels": ["Passed", "Failed"],
#         "values": [passed, failed]
#     }

#     # Ensuring data is correctly formatted
#     chart_data = {
#         "labels": chart_data.get("labels", ["Passed", "Failed"]),
#         "values": chart_data.get("values", [0, 0])
#     }

#     chart_section = f"""
#     <div style="max-width: 300px; margin: 20px auto;">
#         <canvas id="resultChart" width="300" height="300"></canvas>
#     </div>
#     <script>
#         const ctx = document.getElementById('resultChart').getContext('2d');
#         new Chart(ctx, {{
#             type: 'doughnut',
#             data: {{
#                 labels: {json.dumps(chart_data["labels"])},
#                 datasets: [{{
#                     label: 'Test Summary',
#                     data: {json.dumps(chart_data["values"])},
#                     backgroundColor: ['#8BC34A', '#F44336'],
#                     borderWidth: 2,
#                     borderColor: '#ffffff',
#                     hoverOffset: 15
#                 }}]
#             }},
#             options: {{
#                 responsive: true,
#                 plugins: {{
#                     legend: {{
#                         position: 'bottom',
#                         labels: {{
#                             color: '#333',
#                             font: {{
#                                 size: 14
#                             }}
#                         }}
#                     }}
#                 }}
#             }}
#         }});
#     </script>
#     """

#     bugs_section = "<h2>❌ Failed Tests</h2><ul>"
#     for result in test_results:
#         if result.get("status") == "FAIL":
#             bugs_section += f"<li><b>{result['name']}</b>: {result.get('message', 'No message')}</li>"
#     bugs_section += "</ul>"

    
#     video_html = ""
#     if video_url:
#         video_html += f"""
#         <h3>🎥 Test Recording</h3>
#         <a href="{video_url}" target="_blank">Click here to watch the video</a><br><br>
#         """
        
#     if network_file:
#         if network_file.startswith("http"):
#             video_html += f"""
#             <h3>📄 Log File</h3>
#             <a href="{network_file}" target="_blank">Click here to view the Network file</a><br><br>
#             """
#         elif os.path.exists(network_file):
#             with open(network_file, "r", encoding="utf-8") as lf:
#                 log_content = lf.read()
#                 video_html += f"""
#                 <h3>📄 Log File</h3>
#                 <pre style='max-height: 300px; overflow-y: auto; background: #eee; padding: 10px; border-radius: 5px;'>{log_content}</pre><br><br>
#                 """
#         else:
#             video_html += f"""
#             <h3>📄 Log Network File</h3>
#             <p style='color: red;'>Log file not found at the given path: {network_file}</p>
#             """    
    
#     if log_file:
#         if log_file.startswith("http"):
#             video_html += f"""
#             <h3>📄 Log File</h3>
#             <a href="{log_file}" target="_blank">Click here to view the log file</a><br><br>
#             """
#         elif os.path.exists(log_file):
#             with open(log_file, "r", encoding="utf-8") as lf:
#                 log_content = lf.read()
#                 video_html += f"""
#                 <h3>📄 Log File</h3>
#                 <pre style='max-height: 300px; overflow-y: auto; background: #eee; padding: 10px; border-radius: 5px;'>{log_content}</pre><br><br>
#                 """
#         else:
#             video_html += f"""
#             <h3>📄 Log File</h3>
#             <p style='color: red;'>Log file not found at the given path: {log_file}</p>
#             """
            
              
#         if element_file.startswith("http"):
#             video_html += f"""
#             <h3>📄 Log File</h3>
#             <a href="{element_file}" target="_blank">Click here to view the unfound elements file</a><br><br>
#             """
#         elif os.path.exists(element_file):
#             with open(element_file, "r", encoding="utf-8") as lf:
#                 log_content = lf.read()
#                 video_html += f"""
#                 <h3>📄 Log File</h3>
#                 <pre style='max-height: 300px; overflow-y: auto; background: #eee; padding: 10px; border-radius: 5px;'>{log_content}</pre><br><br>
#                 """
#         else:
#             video_html += f"""
#             <h3>📄 Log File</h3>
#             <p style='color: red;'>Log file not found at the given path: {element_file}</p>
#             """            
            
            
#     tests_section = "<h2>📋 All Test Results</h2>" + video_html
#     tests_section += "<table border='1' cellpadding='5'><tr><th>Test Name</th><th>Expected Output</th><th>Actual Output</th><th>Result</th><th>Duration (s)</th><th>Provided Data</th><th>Start Time</th><th>End Time</th><th>Description</th></tr>"

#     for result in test_results:
#         # Determine the result
#         expected_output = result.get('expected_output', 'N/A')
#         actual_output = result.get('actual_output', 'N/A')
#         result_boolean = "PASS" if expected_output == actual_output else "FAIL"

#         status_color = 'green' if result_boolean == "PASS" else 'red'
        
#         tests_section += f"""
#         <tr>
#             <td>{result['name']}</td>
#             <td>{expected_output}</td>
#             <td>{actual_output}</td>
#             <td style='color:{status_color}'>{result_boolean}</td>
#             <td>{result.get('duration', 0)}</td>
#             <td>{result.get('provided_data', '')}</td>
#             <td>{result.get('start_time')}</td>
#             <td>{result.get('end_time')}</td>
#             <td>{result.get('description', '')}</td>
#         </tr>
#         """
#     tests_section += "</table>"

#     html_content = f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#            <title>Business Avenue Test Report</title>
#         <link rel="icon" type="image/png" href="C:\projects\poc\WhatsApp Image 2025-05-09 at 10.28.57_4aae6d67.jpg">
#         <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#         <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&display=swap" rel="stylesheet">
#         <style>
#             body {{
#                 margin: 0;
#                 font-family: 'Poppins', sans-serif;
#                 background: #f7f9fc;
#             }}
#             #sidebar {{
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 width: 80px;
#                 height: 100%;
#                 background: #2f3542;
#                 padding-top: 30px;
#                 display: flex;
#                 flex-direction: column;
#                 align-items: center;
#             }}
#             #sidebar li {{
#                 font-size: 24px;
#                 padding: 20px 0;
#                 color: #ffffff;
#                 cursor: pointer;
#                 position: relative;
#             }}
#             #sidebar li:hover {{
#                 background: #57606f;
#                 width: 100%;
#                 text-align: center;
#             }}
#             #sidebar li::after {{
#                 content: attr(title);
#                 position: absolute;
#                 left: 90px;
#                 top: 10px;
#                 background: #2f3542;
#                 color: #fff;
#                 padding: 4px 10px;
#                 border-radius: 4px;
#                 opacity: 0;
#                 white-space: nowrap;
#                 pointer-events: none;
#                 transition: opacity 0.3s;
#             }}
#             #sidebar li:hover::after {{
#                 opacity: 1;
#             }}
#             #main {{
#                 margin-left: 100px;
#                 padding: 30px;
#             }}
#             .report-section {{
#                 display: none;
#                 animation: fadeIn 0.5s ease-in;
#             }}
#             @keyframes fadeIn {{
#                 from {{ opacity: 0; transform: translateY(10px); }}
#                 to {{ opacity: 1; transform: translateY(0); }}
#             }}
#             canvas {{
#                 background: #fff;
#                 border-radius: 15px;
#                 box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#             }}
#             h2, h3 {{
#                 color: #2c3e50;
#             }}
#             ul {{
#                 padding-left: 20px;
#             }}
#             li {{
#                 margin-bottom: 10px;
#             }}
#             table {{
#                 width: 100%;
#                 border-collapse: collapse;
#                 background: white;
#                 border-radius: 10px;
#                 box-shadow: 0 4px 10px rgba(0,0,0,0.05);
#                 overflow: hidden;
#             }}
#             table th, table td {{
#                 padding: 12px 15px;
#                 text-align: left;
#             }}
#             table th {{
#                 background-color: #f1f1f1;
#             }}
#             tr:nth-child(even) {{
#                 background-color: #f9f9f9;
#             }}
#             video {{
#                 border-radius: 12px;
#                 box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#             }}
#         </style>
#     </head>
#     <body>
    
#         <div id="sidebar">
#             <ul>
#                 <li onclick="showSection('systemInfo')" title="System Info">🛠️</li>
#                 <li onclick="showSection('testsSection')" title="Test Results">📋</li>
#                 <li onclick="showSection('chartSection')" title="Chart">📊</li>
#                 <li onclick="showSection('bugsSection')" title="Bugs">❌</li>
                
#             </ul>
#         </div>
#         <div id="main">
#             <div id="testsSection" class="report-section">{tests_section}</div>
#             <div id="chartSection" class="report-section">{chart_section}</div>
#             <div id="bugsSection" class="report-section">{bugs_section}</div>
#             <div id="systemInfo" class="report-section">
#                 <h3 style="text-align:center; margin-top: 40px;">🛠️ System Information</h3>
#                 <table border='1' cellpadding='5' style='margin: 0 auto; width: 80%; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); overflow: hidden;'>
#                     <tr><th>Property</th><th>Value</th></tr>
#                     <tr><td><strong>Tester</strong></td><td>Barira</td></tr>
#                     <tr><td><strong>Department</strong></td><td>Automation</td></tr>
#                     <tr><td><strong>Testing Website</strong></td><td>Buypass Business Avenue Signup Flow</td></tr>
#                     <tr><td><strong>Browser</strong></td><td>Chrome</td></tr>
#                     <tr><td><strong>System</strong></td><td>Windows</td></tr>
#                 </table>
#             </div>
#         </div>

#         <script>
#             function showSection(id) {{
#                 document.querySelectorAll('.report-section').forEach(el => el.style.display = 'none');
#                 document.getElementById(id).style.display = 'block';
#             }}
#             // Default view
#             showSection('chartSection');
#         </script>
#     </body>
#     </html>
#     """

#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write(html_content)

#     print(f"✅ Report with video generated: {output_file}")  
    
load_dotenv()
def send_test_email_login(test_results,firebase_video_url):
    try:
        if os.getenv("ENVIRONMENT") != "production":
            logging.info("🔒 Not in production environment. Email not sent.")
            return

        EMAIL_USER = os.getenv("EMAIL_USER")
        EMAIL_PASS = os.getenv("EMAIL_PASS")

        if not EMAIL_USER or not EMAIL_PASS:
            logging.error("❌ EMAIL_USER or EMAIL_PASS environment variables are not set.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = EmailMessage()
        msg['Subject'] = f'🧪 {now} | TraderGPT Automation | TraderGPT Login Test Report'
        msg['From'] = f"TraderGPT Automation <{EMAIL_USER}>"
        msg['To'] = 'ghazanfarbarira@gmail.com'

        total = len(test_results)
        passed = sum(1 for r in test_results if r["status"] == "PASS")
        failed = total - passed

        test_rows = ""
        for result in test_results:
            color = "green" if result["status"] == "PASS" else "red"
            message = result.get("message", "—").replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
            # description = result.get("description", "—").replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')

            if result["status"] == "PASS":
                test_rows += f"""
                <tr>
                    <td>{result['name']}</td>
                    <td style='color:{color}'>{result['status']}</td>
                    <td>—</td>
                </tr>
                """
            else:
                test_rows += f"""
                <tr>
                    <td>{result['name']}</td>
                    <td style='color:{color}'>{result['status']}</td>
                   <td>
    
    <hr style='border:0; border-top:1px solid #ccc;'>
    <pre style='white-space:pre-wrap; font-size:13px; color:#990000;'>{message}</pre>
</td>

                </tr>
                """

        html_summary = f"""
        <html>
        <body>
            <h2>📋 TraderGPT Login Flow Automation Summary</h2>
            <p><b>Total Tests:</b> {total}<br>
               <b>Passed:</b> {passed}<br>
               <b>Failed:</b> {failed}</p>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr><th>Test Name</th><th>Result</th><th>Description</th></tr>
                {test_rows}
            </table>
            <p>🎥 <a href="{firebase_video_url}" target="_blank">Watch Test Video</a></p>
            <p>📄 <a href="https://storage.googleapis.com/restapipro-9a75a.appspot.com/logs/tradergpt_log.log" target="_blank">Test Logs</a></p>
            <p>📄 <a href="https://storage.googleapis.com/restapipro-9a75a.appspot.com/network_logs/network_logs/login_end_tradergpt_with_requests_and_console.json" target="_blank">Network Logs</a></p>
            <p>📄 <a href="https://storage.googleapis.com/restapipro-9a75a.appspot.com/unfound_elementsunfound_elements/tradergpt_missing_elements.csv" target="_blank">Unfound Elements</a></p>
        </body>
        </html>
        """

        msg.set_content("📋 Login test summary report attached as HTML.")
        msg.add_alternative(html_summary, subtype='html')

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
         smtp.ehlo()
         smtp.starttls()
         smtp.login(EMAIL_USER, EMAIL_PASS)
         smtp.send_message(msg)

        logging.info("✅ Login email sent successfully")

    except Exception:
        logging.error("❌ Email failed:", exc_info=True)



# def send_test_email_signup(test_results):
#     try:
#         if os.getenv("ENVIRONMENT") != "production":
#             logging.info("🔒 Not in production environment. Email not sent.")
#             return

#         EMAIL_USER = os.getenv("EMAIL_USER")
#         EMAIL_PASS = os.getenv("EMAIL_PASS")

#         if not EMAIL_USER or not EMAIL_PASS:
#             logging.error("❌ EMAIL_USER or EMAIL_PASS not set in environment variables.")
#             return

#         now = datetime.now().strftime("%Y-%m-%d %H:%M")

#         msg = EmailMessage()

#         msg['Subject'] = f'🧪 {now} | TraderGPT Automation | TraderGPT SignUp Test Report'
#         msg['From'] = f"TraderGPT Automation <{EMAIL_USER}>"
#         msg['To'] = 'ghazanfarbarira@gmail.com'

#         total = len(test_results)
#         passed = sum(1 for r in test_results if r["status"] == "PASS")
#         failed = total - passed

#         test_rows = ""
#         for result in test_results:
#             color = "green" if result["status"] == "PASS" else "red"
#             message = result.get("message", "—").replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
#             # description = result.get("description", "—").replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')

#             if result["status"] == "PASS":
#                 test_rows += f"""
#                 <tr>
#                     <td>{result['name']}</td>
#                     <td style='color:{color}'>{result['status']}</td>
#                     <td>—</td>
#                 </tr>
#                 """
#             else:
#                 test_rows += f"""
#                 <tr>
#                     <td>{result['name']}</td>
#                     <td style='color:{color}'>{result['status']}</td>
                    
#     <hr style='border:0; border-top:1px solid #ccc;'>
#     <pre style='white-space:pre-wrap; font-size:13px; color:#990000;'>{message}</pre>
# </td>
#                 </tr>
#                 """

#         html_summary = f"""
#         <html>
#         <body>
#             <h2>📋 TraderGPT Signup Flow Automation Summary</h2>
#             <p><b>Total Tests:</b> {total}<br>
#                <b>Passed:</b> {passed}<br>
#                <b>Failed:</b> {failed}</p>
#             <table border="1" cellpadding="5" cellspacing="0">
#                 <tr><th>Test Name</th><th>Result</th><th>Description</th></tr>
#                 {test_rows}
#             </table>
#             <p>🎥 <a href="https://storage.googleapis.com/restapipro-9a75a.appspot.com/videos/tradergpt_signupflow.avi" target="_blank">Watch Test Video</a>(may take a few minutes to upload)</p>
#             <p>📄 <a href="https://storage.googleapis.com/restapipro-9a75a.appspot.com/logs/tradergpt_log.log" target="_blank">Test Logs</a></p>
#             <p>📄 <a href="https://storage.googleapis.com/restapipro-9a75a.appspot.com/network_logs/network_logs/signup_end_tradergpt_with_requests_and_console.json" target="_blank">Network Logs</a></p>
#             <p>📄 <a href="https://storage.googleapis.com/restapipro-9a75a.appspot.com/unfound_elementsunfound_elements/tradergpt_missing_elements.csv" target="_blank">Unfound Elements</a></p>
#         </body>
#         </html>
#         """

#         msg.set_content("📋 Signup test summary report attached as HTML.")
#         msg.add_alternative(html_summary, subtype='html')

        
#         with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#          smtp.ehlo()
#          smtp.starttls()
#          smtp.login(EMAIL_USER, EMAIL_PASS)
#          smtp.send_message(msg)

#         logging.info("✅ Signup email sent successfully.")

#     except Exception:
#         logging.error("❌ Signup email failed:", exc_info=True)



def send_test_slack_login(test_results,firebase_video_url):
    try:
        if os.getenv("ENVIRONMENT") != "production":
            logging.info("🔒 Not in production environment. Slack message not sent.")
            return

        webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if not webhook_url:
            logging.error("❌ SLACK_WEBHOOK_URL environment variable not set.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        total = len(test_results)
        passed = sum(1 for r in test_results if r["status"] == "PASS")
        failed = total - passed

        failed_tests = "\n".join(
            f"• `{r['name']}` - ❌ {r.get('message', 'No error')}" 
            for r in test_results if r["status"] != "PASS"
        ) or "None 🎉"

        slack_text = (
            f"*🧪 TraderGPT Login Test Report — {now}*\n"
            f"*Total:* {total} | *✅ Passed:* {passed} | *❌ Failed:* {failed}\n\n"
            f"*Failed Tests:*\n{failed_tests}\n\n"
            f"> 🎥 <{firebase_video_url}|Watch Test Video>\n"

            f"> 📄 <https://storage.googleapis.com/restapipro-9a75a.appspot.com/logs/{log_filename}|Test Logs>({get_timestamp()})\n"
            f"> 📄 <https://storage.googleapis.com/restapipro-9a75a.appspot.com/network_logs/network_logs/login_end_tradergpt_with_requests_and_console.json|Network Logs>({get_timestamp()})\n"
            f"> 📄 <https://storage.googleapis.com/restapipro-9a75a.appspot.com/unfound_elementsunfound_elements/tradergpt_missing_elements.csv|Unfound Elements>({get_timestamp()})"
        )

        response = requests.post(webhook_url, json={"text": slack_text})
        if response.status_code == 200:
            logging.info("✅ Slack message sent successfully")
        else:
            logging.error(f"❌ Failed to send Slack message. Status code: {response.status_code}, Response: {response.text}")

    except Exception:
        logging.error("❌ Error sending Slack message:", exc_info=True)
        
        
        
        
     

def send_test_slack_signup(test_results,firebase_video_url_signup):
    try:
        if os.getenv("ENVIRONMENT") != "production":
            logging.info("🔒 Not in production environment. Slack message not sent.")
            return

        webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if not webhook_url:
            logging.error("❌ SLACK_WEBHOOK_URL environment variable not set.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        total = len(test_results)
        passed = sum(1 for r in test_results if r["status"] == "PASS")
        failed = total - passed

        failed_tests = "\n".join(
            f"• `{r['name']}` - ❌ {r.get('message', 'No error')}" 
            for r in test_results if r["status"] != "PASS"
        ) or "None 🎉"

        slack_text = (
            f"*🧪 TraderGPT Signup Test Report — {now}*\n"
            f"*Total:* {total} | *✅ Passed:* {passed} | *❌ Failed:* {failed}\n\n"
            f"*Failed Tests:*\n{failed_tests}\n\n"
           f"> 🎥 <{firebase_video_url_signup}|Watch Test Video>\n"
                 f"> 📄 <https://storage.googleapis.com/restapipro-9a75a.appspot.com/logs/{log_filename}|Test Logs>({get_timestamp()})\n"
            f"> 📄 <https://storage.googleapis.com/restapipro-9a75a.appspot.com/network_logs/network_logs/signup_end_tradergpt_with_requests_and_console.json|Network Logs>({get_timestamp()})\n"
            f"> 📄 <https://storage.googleapis.com/restapipro-9a75a.appspot.com/unfound_elementsunfound_elements/tradergpt_missing_elements.csv|Unfound Elements>({get_timestamp()})"
        )

        response = requests.post(webhook_url, json={"text": slack_text})
        if response.status_code == 200:
            logging.info("✅ Slack message sent successfully")
        else:
            logging.error(f"❌ Failed to send Slack message. Status code: {response.status_code}, Response: {response.text}")

    except Exception:
        logging.error("❌ Error sending Slack message:", exc_info=True) 
def send_whatsapp_message(chat_id: str, message: str):
    """
    Sends WhatsApp message using UltraMsg API
    """

    try:
        # Safety check
        if os.getenv("ENVIRONMENT") != "production":
            logging.info("🔒 Not in production environment. WhatsApp message not sent.")
            return

        INSTANCE_ID = os.getenv("INSTANCE_ID")
        TOKEN = os.getenv("TOKEN")

        if not INSTANCE_ID or not TOKEN:
            logging.error("❌ UltraMsg credentials not set.")
            return

        url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"

        payload = urlencode({
            "token": TOKEN,
            "to": chat_id,   # single number OR group id
            "body": message
        })

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(
            url,
            data=payload,
            headers=headers,
            timeout=20
        )

        if response.status_code == 200:
            logging.info("✅ WhatsApp message sent successfully")
        else:
            logging.error(
                f"❌ WhatsApp failed | {response.status_code} | {response.text}"
            )

    except Exception:
        logging.error("❌ Error sending WhatsApp message", exc_info=True)

def send_whatsapp_signup_report(
    test_results: list,
    firebase_video_url_signup: str,
    log_filename: str
):
    """
    Sends Signup Test Report to WhatsApp group
    """

    try:
        if os.getenv("ENVIRONMENT") != "production":
            logging.info("🔒 Not in production environment. WhatsApp message not sent.")
            return

        chat_id = os.getenv("CHAT_ID")
        if not chat_id:
            logging.error("❌ CHAT_ID not set in environment")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        total = len(test_results)
        passed = sum(1 for r in test_results if r.get("status") == "PASS")
        failed = total - passed

        failed_tests = "\n".join(
            f"- {r.get('name', 'Unknown')} ❌ {r.get('message', 'No error')}"
            for r in test_results if r.get("status") != "PASS"
        ) or "None 🎉"

        whatsapp_text = (
            f"🧪 TraderGPT Signup Test Report\n"
            f"🕒 {now}\n\n"
            f"📊 Summary\n"
            f"Total: {total}\n"
            f"✅ Passed: {passed}\n"
            f"❌ Failed: {failed}\n\n"
            f"❌ Failed Tests:\n{failed_tests}\n\n"
            f"🎥 Video: {firebase_video_url_signup}\n"
            f"📄 Logs: https://storage.googleapis.com/restapipro-9a75a.appspot.com/logs/{log_filename}"
        )

        send_whatsapp_message(chat_id, whatsapp_text)

    except Exception:
        logging.error("❌ Error sending WhatsApp signup report", exc_info=True)

def send_whatsapp_login_report(
    test_results: list,
    firebase_video_url_login: str,
    log_filename: str
):
    """
    Sends Login Test Report to WhatsApp group
    """

    try:
        # ✅ Environment check
        env = os.getenv("ENVIRONMENT", "").strip().lower()
        if env != "production":
            logging.info("🔒 Not in production environment. WhatsApp message not sent.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        if not test_results:
            logging.warning("⚠ No test results provided.")
            return

        total = len(test_results)

        # ✅ Robust PASS detection (case + spaces safe)
        passed_count = sum(
            1 for r in test_results
            if str(r.get("status", "")).strip().upper() == "PASS"
        )

        failed_count = total - passed_count

        # ✅ Decide chat_id based on failure
        if failed_count > 0:
            chat_id = os.getenv("FAILURE_GROUP_CHAT_ID")
            if not chat_id:
                logging.error("❌ FAILURE_GROUP_CHAT_ID not set in environment")
                return
        else:
            chat_id = os.getenv("CHAT_ID")
            if not chat_id:
                logging.error("❌ CHAT_ID not set in environment")
                return

        # ✅ Build failed tests list safely
        failed_tests = "\n".join(
            f"🔴 *{r.get('name', 'Unknown')}* ❌ {r.get('message', 'No error')}"
            for r in test_results
            if str(r.get("status", "")).strip().upper() != "PASS"
        )

        if not failed_tests:
            failed_tests = "None 🎉"

        # ✅ Add strong warning header if failure exists
        header = "🚨🚨 CRITICAL FAILURE 🚨🚨\n\n" if failed_count > 0 else ""

        whatsapp_text = (
            f"{header}"
            f"🧪 TraderGPT Login Test Report\n"
            f"🕒 {now}\n\n"
            f"📊 Summary\n"
            f"Total: {total}\n"
            f"✅ Passed: {passed_count}\n"
            f"❌ Failed: {failed_count}\n\n"
            f"❌ Failed Tests:\n{failed_tests}\n\n"
            f"🎥 Video: {firebase_video_url_login}\n"
            f"📄 Logs: https://storage.googleapis.com/restapipro-9a75a.appspot.com/logs/{log_filename}"
        )

        logging.info(f"📤 Sending WhatsApp report to chat_id: {chat_id}")
        logging.info(f"📊 Total: {total}, Passed: {passed_count}, Failed: {failed_count}")

        send_whatsapp_message(chat_id.strip(), whatsapp_text)

    except Exception:
        logging.error("❌ Error sending WhatsApp login report", exc_info=True)

def send_whatsapp_widget_report(warnings: list):
    """
    Sends WhatsApp message for slow / problematic widgets only.
    Each warning should include widget name and API info.
    No video or full logs are sent.
    """

    try:
        # ✅ Environment check
        env = os.getenv("ENVIRONMENT", "").strip().lower()
        if env != "production":
            logging.info("🔒 Not in production environment. WhatsApp message not sent.")
            return

        if not warnings:
            logging.info("✅ No warnings detected. Nothing to send.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        # ✅ Build message with all warnings
        warning_text = "\n".join(warnings)

        whatsapp_text = (
            f"🧪 Tradersboard Widget Page Warnings\n"
            f"🕒 {now}\n\n"
            f"{warning_text}"
        )

        # ✅ Get WhatsApp chat ID from env
        chat_id = os.getenv("CHAT_ID")
        if not chat_id:
            logging.error("❌ CHAT_ID not set in environment")
            return

        logging.info(f"📤 Sending Widget Warnings WhatsApp message to chat_id: {chat_id}")
        send_whatsapp_message(chat_id.strip(), whatsapp_text)

    except Exception:
        logging.error("❌ Error sending WhatsApp widget warnings", exc_info=True)
