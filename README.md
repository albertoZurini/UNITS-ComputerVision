# Traffic Light Detection and Distance Estimation

This project aims to detect traffic lights, classify their colors, and estimate their distances using a calibrated camera. The pipeline involves camera calibration, object detection with YOLOv11, color classification with MobilenetV2, and distance estimation based on geometric principles.

---

## Project Goals

1. **Camera Calibration and Undistortion**  
   - Calibrate the camera and undistort images to eliminate distortions.
   - Use a checkerboard to accurately estimate distances.

2. **Traffic Light Detection**  
   - Employ YOLOv11 to detect traffic lights in images.

3. **Traffic Light Classification**  
   - Fine-tune a MobilenetV2 model to classify the traffic light's color.

4. **Distance Estimation**  
   - Estimate the distance to traffic lights based on image geometry and camera calibration.

---

## Steps and Methods

### Camera Calibration and Distance Estimation
1. **Checkerboard Calibration**  
   - A checkerboard with known dimensions is used for precise calibration.
   - Images were taken at various distances (300mm to 2000mm, with 100mm steps).  
   - **Hypotheses Tested:**
     - Perspective has a linear relationship between object size and distance.
     - Distance estimation accuracy compared to ground truth (measured with a ruler).

2. **Distance Estimation Methods**  
   - Used a known side length of the checkerboard and calculated distance using the formula:
     ```
     Distance = (Known Length * Focal Length) / Measured Length
     ```
   - Employed linear regression to refine results and average out errors.  
   - Compared results to translation and rotation vectors obtained via OpenCV's `SolvePnP` method.

3. **Results**  
   - Achieved accurate distance measurements within a 5cm confidence range.
   - Verified linear relationships between ground truth and estimated distances.

---

### Traffic Light Detection
- **YOLOv11**  
  - Used YOLOv11 for object detection.  
  - Bounding boxes, classes, and accuracy scores were extracted for further processing.

---

### Traffic Light Classification
- **Model**: MobilenetV2 fine-tuned with PyTorch.  
- **Process**:  
  1. Freeze layers of the pretrained model.  
  2. Prepare the dataset and data loader.  
  3. Train the model on the dataset.  
  4. Export the trained model for inference.  

- **Dataset**:  
  - Used the [Carla Traffic Lights Dataset](https://www.kaggle.com/datasets/sachsene/carla-traffic-lights-images).  
  - Despite its low quality, the dataset allowed testing of real-world classification performance.

---

### Traffic Light Distance Estimation
- Distance estimation was tested in real-world scenarios using video frames and known ground truth distances.  
- Results demonstrate the capability to estimate traffic light distances based on their size in the image.

---

## Full Pipeline
1. Input Image  
2. Object Detection (YOLOv11)  
3. Object Classification (MobilenetV2)  
4. Distance Estimation (Checkerboard-derived formula).  

---

## Performance
- Achieved ~15 FPS on an RTX 3060 laptop, showcasing the computational limitations of the system.

---

## Resources
- **Code**: [UNITS-ComputerVision Repository](https://github.com/albertoZurini/UNITS-ComputerVision)  
- **Demo**: [YouTube Video](https://youtu.be/03zHheRwvPo)

---

## References
- OpenCV Camera Calibration: [Docs](https://docs.opencv.org/4.x/d5/d1f/calib3d_solvePnP.html)  
- MobilenetV2 Fine-tuning: [PyTorch Models](https://pytorch.org/vision/main/models/mobilenetv2.html)  
- Distance Estimation Reference: [StackOverflow](https://stackoverflow.com/questions/14038002/opencv-how-to-calculate-distance-between-camera-and-object-using-image)
