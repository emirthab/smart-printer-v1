<h1 align="center">Smart Printer V1</h1>

<p align="center">
  <a href="https://github.com/emirthab/smart-printer-v1">
    <img src="https://github.com/emirthab/smart-printer-v1/blob/main/static/img/animated-printer.gif?raw=true" alt="Smart Printer V1" width="300">
  </a>
</p>
 
## Introduction:

:large_blue_circle: It is an application that I made with python flask to provide convenience to all businesses that provide smart printer output services.

## Usage :

* ### Install requirements:
```
python -m pip install -r requirements.txt
```

* ### Run Application:
```
python app.py
```
## Features:

:large_blue_circle: Order creation by scanning QR code.  

:large_blue_circle: Link creation and remote order creation. (with bitly api)  

:large_blue_circle: Viewing the files in the order via google documents and opening them ready for printing.  

:large_blue_circle: Note field for customer. (can be removed from settings)  

:large_blue_circle: Variants for files in the order. (number of copies, page structure, etc.)  

:large_blue_circle: Access from different networks without the need to open a port, thanks to the ngrok router service embedded in Python.  

:large_blue_circle: Local storage of order files.  

:large_blue_circle: Flexible settings to suit your wishes.  

:large_blue_circle: Changeable logo.  

## How It Works:

* The application starts working on ngrok according to your request. If you wish, you can run it on your own domain without using ngrok.  
By default, you can login to the application panel via "http://127.0.0.1:8080".   
* If no changes have been made, the default username is "admin" and the password is "admin". You can change the administrator information from the settings.   
* When you come to the QR code tab, there is a constantly renewed QR code on the screen for a certain period of time. When this QR code is read from any device, the application automatically generates a key and directs the device to the page with that key. Your customers can also reach this page by creating a link without reading the QR code.   
* When the page is opened, the client is asked to upload a file. Multiple files can be uploaded and you can specify the file formats that can be uploaded from the settings tab.  
* After the files are uploaded, the customer is asked to select a variant. (number of copies, extra notes, etc.) After the files are uploaded successfully, they are reflected in your admin panel. 

<h3 align="left">Order Creation</h1>
<p align="left">
    <img src="https://github.com/emirthab/smart-printer-v1/blob/main/screenshots/3.png" height="400">
    <img src="https://github.com/emirthab/smart-printer-v1/blob/main/screenshots/2.png" height="400">
    <img src="https://github.com/emirthab/smart-printer-v1/blob/main/screenshots/0.png" height="400">
</p>

<h3 align="left">QR Code</h1>
<p align="left">
    <img src="https://github.com/emirthab/smart-printer-v1/blob/main/screenshots/6.png" height="420">
</p>

<h3 align="left">Orders</h1>
<p align="left">
    <img src="https://github.com/emirthab/smart-printer-v1/blob/main/screenshots/7.png" height="420">
</p>

<h3 align="left">Settings</h1>
<p align="left">
    <img src="https://github.com/emirthab/smart-printer-v1/blob/main/screenshots/4.png" height="420">
</p>

<h3 align="left">Links</h1>
<p align="left">
    <img src="https://github.com/emirthab/smart-printer-v1/blob/main/screenshots/5.png" height="420">
</p>
