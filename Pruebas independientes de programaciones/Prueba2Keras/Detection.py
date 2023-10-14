import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical

# Load the MNIST dataset
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Preprocess the data
train_images = train_images.astype('float32') / 255
test_images = test_images.astype('float32') / 255
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# Define the neural network model
model = Sequential()
model.add(Flatten(input_shape=(28, 28)))
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_images, train_labels, epochs=5, batch_size=128)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(test_images, test_labels)
print(f"Test accuracy: {test_accuracy}")

# Function to detect numbers in cropped images
def detect_number(image):
    # Preprocess the input image
    image = image.reshape(1, 28, 28).astype('float32') / 255

    # Use the trained model to predict the number
    prediction = model.predict(image)
    number = np.argmax(prediction)

    return number

# Generate a cropped image with a number (for demonstration)
cropped_image = test_images[0][5:20, 5:20]

# Display the cropped image
plt.imshow(cropped_image, cmap='gray')
plt.show()

# Detect the number in the cropped image
detected_number = detect_number(cropped_image)
print(f"Detected number: {detected_number}")