from imutils import paths
import numpy as np

from solve_captcha import load_captcha_model, solve_captcha

MODEL_FILENAME = "model/captcha_model.txt"
MODEL_LABELS_FILENAME = "model/model_labels.txt"
CAPTCHA_IMAGES_TEST = "test"

model = load_captcha_model(MODEL_FILENAME, MODEL_LABELS_FILENAME)

captcha_image_files = list(paths.list_images(CAPTCHA_IMAGES_TEST))
captcha_image_files = np.random.choice(captcha_image_files, size=(10,), replace=False)

for image_file in captcha_image_files:

    captcha_text = solve_captcha(image_file, model)

    if captcha_text == "":
        continue

    print("CAPTCHA text is: {} for {}".format(captcha_text, image_file))
