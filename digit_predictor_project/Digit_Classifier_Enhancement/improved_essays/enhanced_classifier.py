import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# Save all visualizations into the sibling visualizations/ folder
VIS_DIR = os.path.join(os.path.dirname(__file__), '..', 'visualizations')
os.makedirs(VIS_DIR, exist_ok=True)


def save_fig(name):
    path = os.path.join(VIS_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f"Saved: {path}")


# ── 1. Load MNIST ─────────────────────────────────────────────────────────────
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

print(f"Training samples : {x_train.shape[0]}")
print(f"Test samples     : {x_test.shape[0]}")

# ── 2. Normalize ──────────────────────────────────────────────────────────────
x_train = x_train / 255.0
x_test  = x_test  / 255.0

# ── 3. Reshape to 4-D for ImageDataGenerator: (N, 28, 28, 1) ─────────────────
x_train_4d = x_train.reshape(-1, 28, 28, 1)
x_test_4d  = x_test.reshape(-1,  28, 28, 1)

# ── 4. Data Augmentation ──────────────────────────────────────────────────────
# Artificially increases training variety by applying random transforms.
datagen = ImageDataGenerator(
    rotation_range=10,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,
)
datagen.fit(x_train_4d)

# ── 5. Build a deeper model with LeakyReLU ────────────────────────────────────
# Extra hidden layer + LeakyReLU avoids dying-neuron problem of plain ReLU.
leaky = tf.keras.layers.LeakyReLU(alpha=0.1)

model = models.Sequential([
    layers.Flatten(input_shape=(28, 28, 1)),
    layers.Dense(256, activation=tf.keras.layers.LeakyReLU(alpha=0.1)),
    layers.Dense(128, activation=tf.keras.layers.LeakyReLU(alpha=0.1)),
    layers.Dense(64,  activation=tf.keras.layers.LeakyReLU(alpha=0.1)),
    layers.Dense(10,  activation='softmax'),
])

model.summary()

# ── 6. Compile with RMSprop ───────────────────────────────────────────────────
model.compile(
    optimizer='rmsprop',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

# ── 7. Train for 10 epochs with augmented data ────────────────────────────────
history = model.fit(
    datagen.flow(x_train_4d, y_train, batch_size=32),
    epochs=10,
    validation_data=(x_test_4d, y_test),
)

# ── 8. Evaluate ───────────────────────────────────────────────────────────────
test_loss, test_acc = model.evaluate(x_test_4d, y_test, verbose=0)
print(f"\nTest accuracy : {test_acc:.4f}")
print(f"Test loss     : {test_loss:.4f}")

# ── 9. Make predictions ───────────────────────────────────────────────────────
predictions = model.predict(x_test_4d)
predicted_labels = predictions.argmax(axis=1)
confidence      = predictions.max(axis=1)

# ── 10. Visualize a grid of 15 correct predictions ───────────────────────────
correct_idx = np.where(predicted_labels == y_test)[0][:15]

fig, axes = plt.subplots(3, 5, figsize=(13, 8))
fig.suptitle("Correct Predictions (green = high confidence)", fontsize=13)
for ax, i in zip(axes.flat, correct_idx):
    ax.imshow(x_test[i], cmap='binary')
    ax.set_title(f"Pred:{predicted_labels[i]}  Conf:{confidence[i]:.2f}", fontsize=8, color='green')
    ax.axis('off')
plt.tight_layout()
save_fig("correct_predictions.png")
plt.show()

# ── 11. Visualize 15 wrong predictions ───────────────────────────────────────
wrong_idx = np.where(predicted_labels != y_test)[0][:15]

fig, axes = plt.subplots(3, 5, figsize=(13, 8))
fig.suptitle("Wrong Predictions — Pred vs True (red)", fontsize=13)
for ax, i in zip(axes.flat, wrong_idx):
    ax.imshow(x_test[i], cmap='binary')
    ax.set_title(f"Pred:{predicted_labels[i]} True:{y_test[i]}", fontsize=8, color='red')
    ax.axis('off')
plt.tight_layout()
save_fig("wrong_predictions.png")
plt.show()

# ── 12. Training curves ───────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Enhanced Classifier — Training History (10 epochs)", fontsize=13)

ax1.plot(history.history['accuracy'],     label='Train', marker='o')
ax1.plot(history.history['val_accuracy'], label='Val',   marker='o')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.set_title('Accuracy')
ax1.legend()

ax2.plot(history.history['loss'],     label='Train', marker='o')
ax2.plot(history.history['val_loss'], label='Val',   marker='o')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.set_title('Loss')
ax2.legend()

plt.tight_layout()
save_fig("training_history.png")
plt.show()

# ── 13. Confusion matrix ──────────────────────────────────────────────────────
cm = tf.math.confusion_matrix(y_test, predicted_labels).numpy()

fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(cm, interpolation='nearest', cmap='Blues')
plt.colorbar(im, ax=ax)
ax.set_title("Confusion Matrix — Enhanced Classifier", fontsize=13)
ax.set_xlabel("Predicted Digit")
ax.set_ylabel("True Digit")
ax.set_xticks(range(10))
ax.set_yticks(range(10))
for r in range(10):
    for c in range(10):
        ax.text(c, r, str(cm[r, c]),
                ha='center', va='center',
                color='white' if cm[r, c] > cm.max() / 2 else 'black',
                fontsize=8)
plt.tight_layout()
save_fig("confusion_matrix.png")
plt.show()

print(f"\nAll visualizations saved to: {os.path.abspath(VIS_DIR)}")
