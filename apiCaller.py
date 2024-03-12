import os
import openai
import urllib.request
import time
import numpy as np
import cv2
import PIL


openai.api_key = ""

userPrompt = input('My name is Lawrence (Bastard2), what should i draw?: ')

apiResponse = openai.images.generate(
  model = "dall-e-2",
  prompt = userPrompt,
  size = "512x512",
  quality = "standard",
  n = 1,
)

try:
    filename ='aiGenerated_'+str(userPrompt)+".jpg"
    image_url = apiResponse.data[0].url
    urllib.request.urlretrieve(image_url, filename)
    print('Image Generated & Saved')
except:
    print("Error: Failed to Generate Image")

aiGenerated = cv2.imread(filename)
cv2.imshow(userPrompt, aiGenerated)

cv2.waitKey(0)