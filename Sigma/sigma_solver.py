import tensorflow as tf
from keras import backend as K
from differential_evolution import differential_evolution
from PIL import Image
import helper
import numpy as np
from tensorflow.keras.models import load_model
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# get vuln image
img = Image.open('dog.png').convert('RGB')
numpy_img = np.asarray(img)

class SigmaNet:
    def __init__(self):
        self.name = 'sigmanet'
        self.model_filename = 'sigmanet.h5'
        try:
            self._model = load_model(self.model_filename)
            print('Successfully loaded', self.name)
        except (ImportError, ValueError, OSError):
            print('Failed to load', self.name)

    def color_process(self, imgs):
        if imgs.ndim < 4:
            imgs = np.array([imgs])
        imgs = imgs.astype('float32')
        mean = [125.307, 122.95, 113.865]
        std = [62.9932, 62.0887, 66.7048]
        for img in imgs:
            for i in range(3):
                img[:, :, i] = (img[:, :, i] - mean[i]) / std[i]
        return imgs

    def predict(self, img):
        processed = self.color_process(img)
        return self._model.predict(processed)

    def predict_one(self, img):
        confidence = self.predict(img)[0]
        predicted_class = np.argmax(confidence)
        return class_names[predicted_class]

def perturb_image(xs, img):
    # If this function is passed just one perturbation vector,
    # pack it in a list to keep the computation the same
    if xs.ndim < 2:
        xs = np.array([xs])

    # Copy the image n == len(xs) times so that we can 
    # create n new perturbed images
    tile = [len(xs)] + [1]*(xs.ndim+1)
    imgs = np.tile(img, tile)

    # Make sure to floor the members of xs as int types
    xs = xs.astype(int)
    result = []

    for x,img in zip(xs, imgs):
        # Split x into an array of 5-tuples (perturbation pixels)
        # i.e., [[x,y,r,g,b], ...]
        pixels = np.split(x, len(x) // 5)
        for pixel in pixels:
            # At each pixel's x,y position, assign its rgb value
            x_pos, y_pos, *rgb = pixel
            result.append([x_pos, y_pos, *rgb])
            img[x_pos, y_pos] = rgb

    return imgs, result

def attack_success(x, img, target_class, model, targeted_attack):
    # Perturb the image with the given pixel(s) and get the prediction of the model
    attack_image, result = perturb_image(x, img)

    confidence = model.predict(attack_image)[0]
    predicted_class = np.argmax(confidence)
    
    # If the prediction is what we want (misclassification or 
    # targeted classification), return True
    print('Confidence:', confidence[target_class])
    if ((targeted_attack and predicted_class == target_class) or
        (not targeted_attack and predicted_class != target_class)):
        return True
    # NOTE: return None otherwise (not False), due to how Scipy handles its callback function

def predict_classes(xs, img, target_class, model, minimize=True):
    # Perturb the image with the given pixel(s) x and get the prediction of the model
    imgs_perturbed, result = perturb_image(xs, img)
    predictions = model.predict(imgs_perturbed)[:,target_class]
    # This function should always be minimized, so return its complement if needed
    return predictions if minimize else 1 - predictions

def attack(model, target=None, maxiter=200, popsize=400):

    # Change the target class based on whether this is a targeted attack or not
    targeted_attack = 'airplane'
    target_class = target if targeted_attack else 'dog'
    
    # Define bounds for a flat vector of x,y,r,g,b values
    # For more pixels, repeat this layout
    bounds = [(0,32), (0,32), (0,256), (0,256), (0,256)] * 5 # 5 pixels
    
    # Population multiplier, in terms of the size of the perturbation vector x
    popmul = max(1, popsize // len(bounds))
    
    # Format the predict/callback functions for the differential evolution algorithm
    def predict_fn(xs):
        return predict_classes(xs, numpy_img, target_class, 
                               model, target is None)
    
    def callback_fn(x, convergence):
        return attack_success(x, numpy_img, target_class, 
                              model, targeted_attack)
    
    # Call Scipy's Implementation of Differential Evolution
    attack_result = differential_evolution(
        predict_fn, bounds, maxiter=maxiter, popsize=popmul,
        recombination=1, atol=-1, callback=callback_fn, polish=False)

    # Calculate some useful statistics to return from this function
    attack_image, result = perturb_image(attack_result.x, numpy_img)
    attack_image = attack_image[0]
    prior_probs = model.predict_one(numpy_img)
    predicted_probs = model.predict_one(attack_image)
    predicted_class = np.argmax(predicted_probs)
    actual_class = 'dog'
    success = predicted_class != actual_class
    print("[prior_probs]", prior_probs)
    print("[predicted_probs]", predicted_probs)
    print("[actual_class]", actual_class)

    # Show the best attempt at a solution (successful or not)
    helper.plot_image(attack_image, class_names.index(actual_class), class_names, predicted_class)

    return [predicted_probs, result]
    
def main():

  target_class = 0 # correspond to the first class (airplane)
  model = SigmaNet() # model

  print('Attacking with target', class_names[target_class])
  attack(model, target_class)
  
if __name__ == "__main__":
  main()
