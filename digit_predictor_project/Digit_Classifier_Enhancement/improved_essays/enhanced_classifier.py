import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

VIS_DIR = os.path.join(os.path.dirname(__file__), "..", "visualizations")
os.makedirs(VIS_DIR, exist_ok=True)

print("Loading MNIST dataset...")
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

print("Training samples : " + str(x_train.shape[0]))
print("Test samples     : " + str(x_test.shape[0]))

print("Normalizing pixel values...")
x_train = x_train / 255.0
x_test = x_test / 255.0

print("Reshaping data to 4D for ImageDataGenerator...")
x_train_4d = x_train.reshape(-1, 28, 28, 1)
x_test_4d = x_test.reshape(-1, 28, 28, 1)

print("Setting up data augmentation...")
datagen = ImageDataGenerator(
    rotation_range=10,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1
)
datagen.fit(x_train_4d)

print("Building deeper neural network with LeakyReLU...")
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28, 1)))
model.add(tf.keras.layers.Dense(256, activation=tf.keras.layers.LeakyReLU(alpha=0.1)))
model.add(tf.keras.layers.Dense(128, activation=tf.keras.layers.LeakyReLU(alpha=0.1)))
model.add(tf.keras.layers.Dense(64, activation=tf.keras.layers.LeakyReLU(alpha=0.1)))
model.add(tf.keras.layers.Dense(10, activation="softmax"))

model.summary()

print("Compiling with RMSprop optimizer...")
model.compile(
    optimizer="rmsprop",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("Training for 10 epochs with augmented data...")
history = model.fit(
    datagen.flow(x_train_4d, y_train, batch_size=32),
    epochs=10,
    validation_data=(x_test_4d, y_test)
)

print("Evaluating on test set...")
test_loss, test_acc = model.evaluate(x_test_4d, y_test, verbose=0)
print("Test accuracy : " + str(round(test_acc, 4)))
print("Test loss     : " + str(round(test_loss, 4)))

print("Making predictions...")
predictions = model.predict(x_test_4d)
predicted_labels = predictions.argmax(axis=1)
confidence = predictions.max(axis=1)

print("Plotting correct predictions...")
correct_idx = np.where(predicted_labels == y_test)[0][:15]

fig1, axes1 = plt.subplots(3, 5, figsize=(13, 8))
fig1.suptitle("Correct Predictions", fontsize=13)
j = 0
for row in range(3):
    for col in range(5):
        ax = axes1[row][col]
        idx = correct_idx[j]
        ax.imshow(x_test[idx], cmap="binary")
        ax.set_title("Pred:" + str(predicted_labels[idx]) + " Conf:" + str(round(confidence[idx], 2)), fontsize=8, color="green")
        ax.axis("off")
        j = j + 1

plt.tight_layout()
save_path1 = os.path.join(VIS_DIR, "correct_predictions.png")
plt.savefig(save_path1, dpi=150, bbox_inches="tight")
plt.show()
print("Saved: " + save_path1)

print("Plotting wrong predictions...")
wrong_idx = np.where(predicted_labels != y_test)[0][:15]

fig2, axes2 = plt.subplots(3, 5, figsize=(13, 8))
fig2.suptitle("Wrong Predictions - Pred vs True", fontsize=13)
k = 0
for row in range(3):
    for col in range(5):
        ax = axes2[row][col]
        idx = wrong_idx[k]
        ax.imshow(x_test[idx], cmap="binary")
        ax.set_title("Pred:" + str(predicted_labels[idx]) + " True:" + str(y_test[idx]), fontsize=8, color="red")
        ax.axis("off")
        k = k + 1

plt.tight_layout()
save_path2 = os.path.join(VIS_DIR, "wrong_predictions.png")
plt.savefig(save_path2, dpi=150, bbox_inches="tight")
plt.show()
print("Saved: " + save_path2)

print("Plotting training curves...")
fig3, axes3 = plt.subplots(1, 2, figsize=(13, 5))
fig3.suptitle("Enhanced Classifier - Training History (10 epochs)", fontsize=13)

axes3[0].plot(history.history["accuracy"], label="Train", marker="o")
axes3[0].plot(history.history["val_accuracy"], label="Val", marker="o")
axes3[0].set_xlabel("Epoch")
axes3[0].set_ylabel("Accuracy")
axes3[0].set_title("Accuracy")
axes3[0].legend()

axes3[1].plot(history.history["loss"], label="Train", marker="o")
axes3[1].plot(history.history["val_loss"], label="Val", marker="o")
axes3[1].set_xlabel("Epoch")
axes3[1].set_ylabel("Loss")
axes3[1].set_title("Loss")
axes3[1].legend()

plt.tight_layout()
save_path3 = os.path.join(VIS_DIR, "training_history.png")
plt.savefig(save_path3, dpi=150, bbox_inches="tight")
plt.show()
print("Saved: " + save_path3)

print("Plotting confusion matrix...")
cm = tf.math.confusion_matrix(y_test, predicted_labels).numpy()

fig4, ax4 = plt.subplots(figsize=(10, 8))
im = ax4.imshow(cm, interpolation="nearest", cmap="Blues")
plt.colorbar(im, ax=ax4)
ax4.set_title("Confusion Matrix - Enhanced Classifier", fontsize=13)
ax4.set_xlabel("Predicted Digit")
ax4.set_ylabel("True Digit")
ax4.set_xticks(range(10))
ax4.set_yticks(range(10))

for r in range(10):
    for c in range(10):
        if cm[r, c] > cm.max() / 2:
            text_color = "white"
        else:
            text_color = "black"
        ax4.text(c, r, str(cm[r, c]), ha="center", va="center", color=text_color, fontsize=8)

plt.tight_layout()
save_path4 = os.path.join(VIS_DIR, "confusion_matrix.png")
plt.savefig(save_path4, dpi=150, bbox_inches="tight")
plt.show()
print("Saved: " + save_path4)

print("\nAll visualizations saved to: " + os.path.abspath(VIS_DIR))
