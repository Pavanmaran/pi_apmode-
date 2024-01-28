from flask import Flask, render_template
from gpiozero import LED  # Uncomment this line if you are using GPIO
import time
import random
import subprocess

app = Flask(__name__)

# Set up LED
#led = LED(17)  # Replace with the GPIO pin you're using

# Function to generate a random value
def get_random_value():
    return random.randint(0, 20)

# Function to configure the Raspberry Pi as an Access Point
def configure_ap_mode():
    subprocess.run(['sudo', 'systemctl', 'stop', 'hostapd'])
    subprocess.run(['sudo', 'systemctl', 'stop', 'dnsmasq'])

    subprocess.run(['sudo', 'cp', '/etc/dhcpcd.conf', '/etc/dhcpcd.conf.bak'])
    subprocess.run(['sudo', 'cp', '/etc/dnsmasq.conf', '/etc/dnsmasq.conf.bak'])
    subprocess.run(['sudo', 'cp', '/etc/default/hostapd', '/etc/default/hostapd.bak'])
    
    subprocess.run(['sudo', 'cp', 'config/dhcpcd_ap.conf', '/etc/dhcpcd.conf'])
    subprocess.run(['sudo', 'cp', 'config/dnsmasq_ap.conf', '/etc/dnsmasq.conf'])
    subprocess.run(['sudo', 'cp', 'config/hostapd_ap.conf', '/etc/hostapd/hostapd.conf'])

    subprocess.run(['sudo', 'systemctl', 'unmask', 'hostapd'])
    subprocess.run(['sudo', 'systemctl', 'enable', 'hostapd'])
    subprocess.run(['sudo', 'systemctl', 'enable', 'dnsmasq'])

    subprocess.run(['sudo', 'systemctl', 'start', 'hostapd'])
    subprocess.run(['sudo', 'systemctl', 'start', 'dnsmasq'])

# Home route
@app.route('/')
def home():
    return render_template('index_ap_gpiozero.html', state='OFF', random_value=get_random_value())

# Light on route
@app.route('/lighton')
def light_on():
    #led.on()
    return render_template('index_ap_gpiozero.html', state='ON', random_value=get_random_value())

# Light off route
@app.route('/lightoff')
def light_off():
    #led.off()
    return render_template('index_ap_gpiozero.html', state='OFF', random_value=get_random_value())

# Value route
@app.route('/value')
def get_value():
    return render_template('index_ap_gpiozero.html', state='OFF', random_value=get_random_value())

if __name__ == '__main__':
    # Configure Raspberry Pi as an Access Point
    configure_ap_mode()

    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=80)
