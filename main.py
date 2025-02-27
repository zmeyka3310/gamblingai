import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from datetime import datetime
import data_processing  # Import the data processing functions

# --- Configuration ---
CSV_FILE_PATH = '/home/zmeyka/repos/gamblingai/historicaldata/HDaapl5y.csv'  # Replace with your CSV file path
CLOSE_PRICE_COLUMN = 'Close/Last'
SEQUENCE_LENGTH = 10  # Length of input sequence for the RNN
TEST_SIZE = 0.2  # Proportion of data to use for testing
LEARNING_RATE = 0.001
EPOCHS = 50
BATCH_SIZE = 32


def build_rnn_model(input_shape):
    """Builds an LSTM-based RNN model."""
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))  # First LSTM layer
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))  # Second LSTM layer
    model.add(Dropout(0.2))
    model.add(Dense(units=1))  # Output layer
    return model


def train_model(model, X_train, y_train, epochs, batch_size, learning_rate):
    """Trains the RNN model."""
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mse')
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    return model


def predict_next_value(model, last_sequence, scaler):
    """Predicts the next value based on the last sequence."""
    # Reshape the last sequence to be [1, sequence_length, 1] which is what the model expects
    last_sequence_reshaped = last_sequence.reshape((1, SEQUENCE_LENGTH, 1))
    predicted_value = model.predict(last_sequence_reshaped)
    # Inverse transform to get the actual value
    predicted_value = scaler.inverse_transform(predicted_value)
    return predicted_value[0, 0]


def main():
    """Main function to load, preprocess, train, and predict."""
    data, df = data_processing.load_and_preprocess_data(CSV_FILE_PATH, CLOSE_PRICE_COLUMN)

    if data is None:
        print("Data loading or preprocessing failed.  Exiting.")
        return  # Exit if data loading/preprocessing failed


    # Scale the data
    data, scaler = data_processing.scale_data(data)


    # Create sequences
    X, y = data_processing.create_sequences(data, SEQUENCE_LENGTH)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, shuffle=False)

    # Build the RNN model
    model = build_rnn_model((SEQUENCE_LENGTH, 1))

    # Train the model
    model = train_model(model, X_train, y_train, EPOCHS, BATCH_SIZE, LEARNING_RATE)

    # Get the last sequence from the original scaled data
    last_sequence = data[-SEQUENCE_LENGTH:]

    # Predict the next value
    predicted_price = predict_next_value(model, last_sequence, scaler)

    # Get the last date from the original dataframe
    last_date = df.index[-1]

    # Calculate the next day
    next_date = last_date + pd.Timedelta(days=1)

    print(f"Predicted closing price for {next_date.strftime('%Y-%m-%d')}: ${predicted_price:.2f}")

if __name__ == "__main__":
    main()
