# FortSight AI: Optional Machine Learning Architecture

This document outlines the architecture, data collection strategy, feature engineering, and model serving setup for the optional ML components in FortSight AI. These features are not required for MVP but provide advanced capabilities.

## 1. ML Service Architecture

The ML subsystem is designed to be **loosely coupled** with the core FortSight AI functionality. If ML models are unavailable, the core app (visibility calculations, generic queries) must continue functioning without interruption using fallback mechanisms.

### Components
- **Model Storage (`/models`)**: Trained models (e.g., ONNX or TensorFlow Lite formats) are stored in this directory. They should be versioned (e.g., `fort_classifier_v1.onnx`).
- **Inference Services (`backend/app/services/ml/`)**: Abstraction layers that load models into memory and provide prediction functions. They handle input preprocessing and output parsing.
- **API Endpoints (`backend/app/api/v1/endpoints/ml.py`)**: Dedicated routes for ML features so that client applications can asynchronously query them without blocking core rendering.
- **Model Monitoring**: In production, inferences should be logged to track accuracy drift.

## 2. Feature Engineering Templates

### Visibility Confidence Model
Predicts the confidence (0-1) of a calculated visibility result.
- **Features**:
  - `distance_km`: Continuous float. Distance between observer and target.
  - `dem_resolution_m`: Continuous float (e.g., 30m vs 90m DEM).
  - `terrain_ruggedness`: Continuous float. Standard deviation of elevation along the Line of Sight (LOS).
  - `viewing_angle`: Continuous float. Angle of elevation/depression to the target.
- **Target**: `is_actually_visible` (Binary classification for training, outputting probability as confidence).

### Trek Difficulty Prediction
Predicts difficulty of a trail (Easy, Medium, Hard).
- **Features**:
  - `elevation_gain_m`: Continuous float.
  - `distance_km`: Continuous float.
  - `terrain_type`: Categorical (e.g., Rocky, Forest, Steps). One-hot encoded.
  - `average_gradient`: Continuous float.

## 3. Data Collection Strategy

### Fort Image Recognition & Landmark Recognition
- **Sources**: Crowdsourced user uploads, public domain tourist images, historical archives.
- **Labels**: Image classified by fort name (e.g., "Rajgad", "Torna") and landmark type ("Machi", "Darwaza").
- **Augmentation**: Ensure robustness against different lighting conditions by applying synthetic rotations, brightness adjustments, and blurring during training.
- **Storage**: Store raw images in cloud storage (e.g., S3) outside the main repository, with a metadata database linking S3 URIs to labels.

### Visibility Ground Truth
- **Sources**: User feedback ("Could you actually see X from here? Yes/No").
- **Process**: Compare the user's ground truth against the engine's prediction to build a dataset of True Positives, False Positives, etc.

## 4. Training Pipeline Outline

The training pipeline for the models (e.g., Random Forest for Visibility Confidence, MobileNet for Image Classification) should follow these steps:
1. **Data Extraction**: Scripts query the main database (or S3) to pull training data.
2. **Preprocessing**: Scaling numerical features, one-hot encoding categorical features, resizing images (224x224 RGB).
3. **Training**: Use frameworks like `scikit-learn` for tabular data and `TensorFlow/Keras` for images. Use an 80/20 train/validation split.
4. **Evaluation**: Generate Precision, Recall, F1 scores, and Confusion Matrices.
5. **Serialization**: Export the trained model to a portable format (ONNX or Joblib).

## 5. Model Serving Setup

For this scaffolding, we assume local inference using `onnxruntime` or `joblib`/`pickle`.
- **Loading**: Models are loaded lazily upon the first request or eagerly at FastAPI startup via lifespan events.
- **Fallback**: If a model file is missing or inference fails, the services catch the exception and return a structured fallback response (e.g., `{"error": "Model unavailable", "fallback": true}`).

## 6. Integration Documentation

To enable these features:
1. Train the models using the provided script templates (e.g., `scripts/ml/train_visibility_confidence.py`).
2. Save the models into `backend/models/`.
3. The API endpoints in `/api/v1/ml/` will automatically start using the models for predictions.
4. Update the frontend UI to display confidence scores or image upload components when these endpoints are reachable.
