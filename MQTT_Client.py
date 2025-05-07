import tkinter as tk
from tkinter import font
import paho.mqtt.client as mqtt
import threading
from datetime import datetime

# ----- Configuration -----
DEFAULT_BROKER = "test.mosquitto.org"
DEFAULT_PORT = 1883
DEFAULT_TOPIC = "temp"

# ----- Global State -----
mqtt_client = None
mqtt_thread = None


# ----- MQTT Callbacks -----
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        update_status("✅ Connected")
        update_log("Connected to MQTT broker")
        client.subscribe(userdata["topic"])
    else:
        update_status(f"❌ Connect failed (code {rc})")
        update_log(f"Connection failed: {rc}")


def on_message(client, userdata, msg):
    message = msg.payload.decode()
    update_log(f"📨 {message}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        update_status("❌ Disconnected unexpectedly")
        update_log("Disconnected unexpectedly")
    else:
        update_status("🔌 Disconnected")
        update_log("Disconnected from MQTT broker")


# ----- Utility -----
def update_log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_box.config(state=tk.NORMAL)
    log_box.insert(tk.END, f"{timestamp} {msg}\n")
    log_box.see(tk.END)
    log_box.config(state=tk.DISABLED)


def update_status(msg):
    status_var.set(msg)


# ----- MQTT Logic -----
def connect():
    global mqtt_client, mqtt_thread

    if mqtt_client:
        update_status("⚠️ Already connected")
        return

    broker = broker_var.get().strip()
    topic = topic_var.get().strip()
    try:
        port = int(port_var.get())
    except ValueError:
        update_status("❌ Invalid port")
        return

    if not broker or not topic:
        update_status("❌ Broker and topic required")
        return

    update_status("🔌 Connecting...")

    def mqtt_worker():
        global mqtt_client
        mqtt_client = mqtt.Client(userdata={"topic": topic})
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.on_disconnect = on_disconnect
        try:
            mqtt_client.connect(broker, port, 60)
            mqtt_client.loop_forever()
        except Exception as e:
            update_status("❌ Connection error")
            update_log(f"Connection error: {str(e)}")
            mqtt_client = None

    mqtt_thread = threading.Thread(target=mqtt_worker, daemon=True)
    mqtt_thread.start()


def disconnect():
    global mqtt_client
    if mqtt_client:
        try:
            mqtt_client.disconnect()
        except:
            pass
        mqtt_client = None
        update_status("🔌 Disconnected")
        update_log("Disconnected from MQTT broker")


def publish_message():
    global mqtt_client
    message = message_var.get().strip()
    topic = publish_topic_var.get().strip()

    if not mqtt_client:
        update_status("❌ Not connected")
        return
    if not message:
        update_status("⚠️ Message empty")
        return

    mqtt_client.publish(topic, message)
    update_log(f"📤 Published: '{message}' to '{topic}'")


# ----- GUI Setup -----
root = tk.Tk()
root.title("MQTT Client")
root.geometry("800x500")
root.configure(bg="#2e2e2e")

# Fonts and Colors
label_font = font.Font(family="Arial", size=12)
entry_font = font.Font(family="Arial", size=12)
log_font = font.Font(family="Courier New", size=11)
accent_color = "#00ffcc"
fg_color = "#ffffff"
bg_color = "#3e3e3e"
entry_bg = "#1e1e1e"
entry_fg = "#00ff00"

# ----- Frames -----
# Connection Frame
conn_frame = tk.LabelFrame(root, text="Connection Settings", bg=bg_color, fg=accent_color, font=label_font, padx=10,
                           pady=10)
conn_frame.pack(fill=tk.X, padx=20, pady=10)

# Broker
tk.Label(conn_frame, text="Broker:", bg=bg_color, fg=fg_color, font=label_font).grid(row=0, column=0, sticky="w")
broker_var = tk.StringVar(value=DEFAULT_BROKER)
tk.Entry(conn_frame, textvariable=broker_var, font=entry_font, bg=entry_bg, fg=entry_fg,
         insertbackground=entry_fg).grid(row=0, column=1, sticky="we")

# Port
tk.Label(conn_frame, text="Port:", bg=bg_color, fg=fg_color, font=label_font).grid(row=0, column=2, sticky="w",
                                                                                   padx=(10, 0))
port_var = tk.StringVar(value=str(DEFAULT_PORT))
tk.Entry(conn_frame, textvariable=port_var, font=entry_font, bg=entry_bg, fg=entry_fg, width=6,
         insertbackground=entry_fg).grid(row=0, column=3, sticky="w")

# Topic
tk.Label(conn_frame, text="Topic:", bg=bg_color, fg=fg_color, font=label_font).grid(row=1, column=0, sticky="w", pady=5)
topic_var = tk.StringVar(value=DEFAULT_TOPIC)
tk.Entry(conn_frame, textvariable=topic_var, font=entry_font, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg).grid(
    row=1, column=1, columnspan=3, sticky="we")

# Connect/Disconnect Buttons
btn_frame = tk.Frame(conn_frame, bg=bg_color)
btn_frame.grid(row=2, column=0, columnspan=4, sticky="we", pady=5)

tk.Button(btn_frame, text="Connect", command=connect, bg="#4CAF50", fg="black", font=label_font, width=12).pack(
    side=tk.LEFT, padx=(0, 10))
tk.Button(btn_frame, text="Disconnect", command=disconnect, bg="#f44336", fg="white", font=label_font, width=12).pack(
    side=tk.LEFT)

status_var = tk.StringVar(value="Not connected")
tk.Label(btn_frame, textvariable=status_var, bg=bg_color, fg=accent_color, font=label_font).pack(side=tk.RIGHT,
                                                                                                 padx=(10, 0))

conn_frame.grid_columnconfigure(1, weight=1)

# Publish Frame
publish_frame = tk.LabelFrame(root, text="Publish Message", bg=bg_color, fg=accent_color, font=label_font, padx=10,
                              pady=5)
publish_frame.pack(fill=tk.X, padx=20, pady=5)

# Publish Topic
tk.Label(publish_frame, text="Publish Topic:", bg=bg_color, fg=fg_color, font=label_font).grid(row=0, column=0,
                                                                                               sticky="w")
publish_topic_var = tk.StringVar(value=DEFAULT_TOPIC)
tk.Entry(publish_frame, textvariable=publish_topic_var, font=entry_font, bg=entry_bg, fg=entry_fg,
         insertbackground=entry_fg).grid(row=0, column=1, sticky="we", columnspan=2)

# Message
tk.Label(publish_frame, text="Message:", bg=bg_color, fg=fg_color, font=label_font).grid(row=1, column=0, sticky="w")
message_var = tk.StringVar()
tk.Entry(publish_frame, textvariable=message_var, font=entry_font, bg=entry_bg, fg=entry_fg,
         insertbackground=entry_fg).grid(row=1, column=1, sticky="we")

# Publish Button
tk.Button(publish_frame, text="Publish", command=publish_message, bg=accent_color, fg="black", font=label_font,
          width=12).grid(row=1, column=2, padx=10)

publish_frame.grid_columnconfigure(1, weight=1)

# Log Frame
log_frame = tk.LabelFrame(root, text="Message Log", bg=bg_color, fg=accent_color, font=label_font, padx=10, pady=5)
log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))

log_box = tk.Text(log_frame, font=log_font, bg="#1e1e1e", fg="#00ff00", state=tk.DISABLED, wrap=tk.WORD)
log_box.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

log_scroll = tk.Scrollbar(log_frame, command=log_box.yview)
log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
log_box.config(yscrollcommand=log_scroll.set)

# ----- Start Log -----
update_log("Not connected")

# ----- Handle Exit -----
root.protocol("WM_DELETE_WINDOW", lambda: (disconnect() if mqtt_client else None, root.destroy()))
root.mainloop()
