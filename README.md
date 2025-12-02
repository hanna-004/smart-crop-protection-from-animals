#  Smart Crop Protection from Animals  
### AI-Based Animal Intrusion Detection using YOLO & Computer Vision

This project is an AI-powered **real-time animal intrusion detection system** designed to help farmers protect agricultural fields from crop damage. It uses **YOLO-based object detection** and **Computer Vision** techniques to identify animals entering farmland and trigger alerts for quick response.

---

##  Features
- Real-time animal intrusion detection  
- YOLO-based object detection  
- Works with live video feed or CCTV footage  
- Detects multiple animals (cow, goat, dog, etc.)  
- Helps reduce crop damage and increases farm safety  
- Simple and efficient AI solution for smart farming  

---

##  Tech Stack
- **Python**  
- **OpenCV**  
- **YOLOv5/YOLOv8**  
- **NumPy**  
- **Torch / TensorFlow**  
- **Matplotlib**

---
## 📸 Demo Output  

### 🐾 Animal Detection Output  
![Detection Output](detection_output.png)

### 📧 Email Alert Screenshot  
![Email Sent](email_sent-Copy.png)


## Project Structure
```text
animal-intrusion-alert/
│── program.py # Main program
│── requirements.txt # All required Python libraries
│── README.md # Project documentation
│── detection_output.png # output of the project

```
---

##  Features

- **Real-time Animal Detection** using YOLOv8  
- **Email Alerts** with the detected animal image  
- **Automatic Phone Call Alerts** using Twilio  
- Filters out unwanted objects(chair, bottle, etc.)  
- Live webcam detection  
- Fast and lightweight (uses YOLOv8n)  

---

## How It Works

1. Camera captures live video  
2. YOLOv8 detects animals  
3. If an animal is detected:  
   -  Email is sent with photo  
   - Phone call is made after 15 seconds  
4. Detection is shown on screen  

---

## Install Dependencies
```bash
pip install -r requirements.txt
```
## Run the Project
```bash
python animal_alert.py
```
