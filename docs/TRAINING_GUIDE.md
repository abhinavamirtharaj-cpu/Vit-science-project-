# Training the Model with External Data

## Overview
The SCIVIT sentiment analysis system can be trained with your own emotion/sentiment datasets. The training pipeline supports **13 different CSV/TSV formats** and automatically consolidates them into a unified training dataset.

## 🚀 Quick Start

### Step 1: Place Your Training Files
Copy your CSV files to either location:
```bash
/workspaces/SCIVIT-Draft/training_data/
# or
/tmp/
```

### Step 2: Run the Training Pipeline
```bash
cd /workspaces/SCIVIT-Draft
python train_with_external_data.py
```

That's it! The system will:
- ✅ Automatically detect all supported file formats
- ✅ Process and consolidate the data
- ✅ Map emotions to sentiment categories
- ✅ Train the Markov Chain prediction model
- ✅ Generate transition probabilities
- ✅ Save the trained model to `data/data_trained.csv`

---

## 📋 Supported File Formats

The training system automatically processes these formats:

| # | File Name | Format | Key Columns |
|---|-----------|--------|-------------|
| 1 | conversation_text.csv | Emotion labels | text, emotion_label, conversation_id |
| 2 | emotion_dataset_v5_clean.csv | Sentence emotion | sentence, emotion, cleaned_text |
| 3 | Test_Data.csv | Subtitle emotion | Subtitle, Emotion |
| 4 | test.tsv | Multi-label (TSV) | text, Joy, Fear, Anger, Sadness, Disgust, Surprise |
| 5 | data.csv | Numeric labels | text, labels (0-7) |
| 6 | final_dataset (1).csv | Text emotion | text, emotion |
| 7 | DATA.txt | Text format | text;emotion (semicolon-separated) |
| 8 | Emotion_classify_Data.csv | Comment emotion | Comment, Emotion |
| 9 | text_emotion.csv | Twitter sentiment | content, sentiment, author |
| 10 | text_emotion (1).csv | Twitter sentiment | Same as above |
| 11 | emotion_tweets.csv | Tweet emotion | Tweet, Emotion |
| 12 | test_predictions_full.csv | Predictions | originaltweet, sentiment_category |
| 13 | eng.csv | Multi-label | text, Anger, Fear, Joy, Sadness, Surprise |

---

## 🎯 Emotion → Sentiment Mapping

Your emotion labels are automatically mapped to these sentiment categories:

### Very Positive
- joy, happiness, love, excitement, enthusiasm, admiration, gratitude

### Positive  
- fun, amusement, approval, caring, relief, pride, optimism

### Neutral
- neutral, surprise, confusion, curiosity

### Negative
- anger, annoyance, disgust, disappointment, embarrassment, worry, guilt

### Very Negative
- sadness, fear, hate, grief, shame, despair

### Sarcastic
- sarcasm, sarcastic (context-dependent)

---

## 📊 Training Process

The pipeline follows these steps:

```
1. File Discovery
   └─→ Scans training_data/ and /tmp/ for CSV files

2. Format Detection
   └─→ Identifies file format and selects appropriate processor

3. Data Extraction
   └─→ Extracts text and emotion labels

4. Emotion Mapping
   └─→ Converts emotions to sentiment categories

5. Consolidation
   └─→ Combines all datasets, removes duplicates

6. Model Training
   └─→ Builds Markov Chain transition probabilities

7. Validation
   └─→ Tests predictions on sample data

8. Save Model
   └─→ Writes to data/data_trained.csv
```

---

## 🔧 Advanced Usage

### Option 1: Programmatic Training
```python
from train_with_external_data import main as train_model

# Trains with all files in training_data/ and /tmp/
success = train_model()
```

### Option 2: Custom File Paths
```python
from preprocess_training_data import consolidate_all_datasets, EMOTION_TO_SENTIMENT

file_mappings = {
    '/path/to/your/file.csv': process_emotion_dataset,
    # Add more files...
}

df = consolidate_all_datasets(file_mappings)
```

### Option 3: Add New Emotion Mappings
Edit `preprocess_training_data.py`:
```python
EMOTION_TO_SENTIMENT = {
    'your_emotion': 'Very Positive',
    'custom_label': 'Negative',
    # Add your mappings...
}
```

---

## ✅ Validation

After training, test the model:

```bash
# Run comprehensive tests
python run_train_and_test.py

# Or test interactively
python run_system.py
```

### Expected Output:
```
TRAINING SENTIMENT PREDICTION MODEL
====================================
✓ Training data saved to: data/data_trained.csv
✓ Model successfully trained!

📊 Learned Sentiment Transitions:

  From 'Very Negative':
    → Sarcastic            (45.2% probability)
    → Very Negative        (28.1% probability)
    → Negative             (18.3% probability)

  From 'Positive':
    → Very Positive        (52.7% probability)
    → Positive             (31.4% probability)
    → Neutral              (12.9% probability)
```

---

## 📈 Training Statistics

The system provides detailed statistics:

- **Total samples collected**: All records from your files
- **Duplicates removed**: Based on message text
- **Final dataset size**: Unique training samples
- **Sentiment distribution**: Percentage breakdown by category
- **Transition probabilities**: Learned patterns for each sentiment

---

## 🐛 Troubleshooting

### No files found?
```bash
# Check if files are in the right location
ls /workspaces/SCIVIT-Draft/training_data/
ls /tmp/*.csv

# Run the setup helper
python setup_training_files.py
```

### Wrong format?
The system auto-detects formats, but ensure:
- CSV files have headers
- Emotion/sentiment columns are properly named
- Text columns contain actual text (not empty)

### Low accuracy?
- Provide more training data
- Ensure emotion labels are consistent
- Check sentiment distribution (avoid class imbalance)

---

## 📝 Example: Complete Workflow

```bash
# 1. Copy your files
cp ~/Downloads/*.csv /workspaces/SCIVIT-Draft/training_data/

# 2. Verify files are detected
python setup_training_files.py

# 3. Train the model
python train_with_external_data.py

# 4. Test predictions
python run_train_and_test.py

# 5. Use in production
python ui_io/UI.py
```

---

## 🎓 How the Model Works

The system uses a **Markov Chain** approach:

1. **Analyzes sentiment transitions** in your data
   - Example: "Negative" → "Sarcastic" (60%)
   
2. **Builds probability matrices**
   - For each sentiment, tracks what typically comes next
   
3. **Predicts future sentiment**
   - Given current state, suggests most likely next state
   
4. **Combines with real-time analysis**
   - Node 1: TextBlob sentiment analysis
   - Node 2: Markov Chain prediction (YOUR TRAINED MODEL)
   - Node 3: Combined decision with sarcasm detection

---

## 🔐 Data Privacy

- All training happens locally in your container
- No data is sent to external servers
- Trained model is stored in `data/data_trained.csv`
- You can delete training files after model is built

---

## 📞 Support

Need help? Check:
- [QUICK_START.md](QUICK_START.md) - Getting started guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical details

---

## ✨ What's Next?

After training:
1. ✅ Model is ready for real-time predictions
2. ✅ Integrated with the web interface
3. ✅ Analyzes chat sentiment patterns
4. ✅ Detects mood transitions
5. ✅ Identifies sarcasm and volatility

**Your emotion data is now powering intelligent sentiment analysis!** 🎉
