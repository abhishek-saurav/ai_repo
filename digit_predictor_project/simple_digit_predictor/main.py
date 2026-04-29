import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# ── 1. Load MNIST dataset ─────────────────────────────────────────────────────
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

print(f"Training samples : {x_train.shape[0]}")
print(f"Test samples     : {x_test.shape[0]}")
print(f"Image shape      : {x_train.shape[1:]}")

# ── 2. Normalize pixel values from 0–255 to 0–1 ──────────────────────────────
x_train, x_test = x_train / 255.0, x_test / 255.0

# ── 3. Build the neural network ───────────────────────────────────────────────
# Flatten converts each 28×28 image into a 784-element vector.
# Dense(128, relu) is a hidden layer that learns digit features.
# Dense(10, softmax) outputs probability scores for digits 0–9.
model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax'),
])

model.summary()

# ── 4. Compile ────────────────────────────────────────────────────────────────
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

# ── 5. Train for 5 epochs ─────────────────────────────────────────────────────
history = model.fit(x_train, y_train, epochs=5, validation_split=0.1)

# ── 6. Evaluate on the test set ───────────────────────────────────────────────
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\nTest accuracy : {test_acc:.4f}")
print(f"Test loss     : {test_loss:.4f}")

# ── 7. Make predictions ───────────────────────────────────────────────────────
predictions = model.predict(x_test)

# ── 8. Visualize the first 10 test images with their predicted labels ─────────
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
fig.suptitle("Simple Digit Predictor — First 10 Predictions", fontsize=14)

for i, ax in enumerate(axes.flat):
    ax.imshow(x_test[i], cmap='binary')
    predicted = predictions[i].argmax()
    actual = y_test[i]
    color = 'green' if predicted == actual else 'red'
    ax.set_title(f"Pred: {predicted}  True: {actual}", color=color, fontsize=9)
    ax.axis('off')

plt.tight_layout()
plt.savefig("predictions_sample.png", dpi=150)
plt.show()
print("Saved: predictions_sample.png")

# ── 9. Plot training accuracy and loss curves ─────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("Training History", fontsize=14)

ax1.plot(history.history['accuracy'],     label='Train accuracy')
ax1.plot(history.history['val_accuracy'], label='Val accuracy')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.set_title('Accuracy over Epochs')
ax1.legend()

ax2.plot(history.history['loss'],     label='Train loss')
ax2.plot(history.history['val_loss'], label='Val loss')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.set_title('Loss over Epochs')
ax2.legend()

plt.tight_layout()
plt.savefig("training_history.png", dpi=150)
plt.show()
print("Saved: training_history.png")
