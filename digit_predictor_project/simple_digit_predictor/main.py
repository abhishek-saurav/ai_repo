import tensorflow as tf
import matplotlib.pyplot as plt

print("Loading MNIST dataset...")
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

print("Training samples : " + str(x_train.shape[0]))
print("Test samples     : " + str(x_test.shape[0]))
print("Image shape      : " + str(x_train.shape[1:]))

print("Normalizing pixel values from 0-255 to 0-1...")
x_train = x_train / 255.0
x_test = x_test / 255.0

print("Building the neural network model...")
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
model.add(tf.keras.layers.Dense(128, activation="relu"))
model.add(tf.keras.layers.Dense(10, activation="softmax"))

model.summary()

print("Compiling the model...")
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("Training the model for 5 epochs...")
history = model.fit(x_train, y_train, epochs=5, validation_split=0.1)

print("Evaluating on test set...")
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print("Test accuracy : " + str(round(test_acc, 4)))
print("Test loss     : " + str(round(test_loss, 4)))

print("Making predictions on test images...")
predictions = model.predict(x_test)

print("Displaying first 10 predictions...")
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
fig.suptitle("Simple Digit Predictor - First 10 Predictions", fontsize=14)

i = 0
for row in range(2):
    for col in range(5):
        ax = axes[row][col]
        ax.imshow(x_test[i], cmap="binary")
        predicted = predictions[i].argmax()
        actual = y_test[i]
        if predicted == actual:
            color = "green"
        else:
            color = "red"
        ax.set_title("Pred: " + str(predicted) + "  True: " + str(actual), color=color, fontsize=9)
        ax.axis("off")
        i = i + 1

plt.tight_layout()
plt.savefig("predictions_sample.png", dpi=150)
plt.show()
print("Saved: predictions_sample.png")

print("Plotting training history...")
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 4))
fig2.suptitle("Training History", fontsize=14)

axes2[0].plot(history.history["accuracy"], label="Train accuracy")
axes2[0].plot(history.history["val_accuracy"], label="Val accuracy")
axes2[0].set_xlabel("Epoch")
axes2[0].set_ylabel("Accuracy")
axes2[0].set_title("Accuracy over Epochs")
axes2[0].legend()

axes2[1].plot(history.history["loss"], label="Train loss")
axes2[1].plot(history.history["val_loss"], label="Val loss")
axes2[1].set_xlabel("Epoch")
axes2[1].set_ylabel("Loss")
axes2[1].set_title("Loss over Epochs")
axes2[1].legend()

plt.tight_layout()
plt.savefig("training_history.png", dpi=150)
plt.show()
print("Saved: training_history.png")
