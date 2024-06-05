import cv2
import numpy as np

# Load the generated image and the mask
generated_image = cv2.imread('path_to_generated_image.jpg')
mask = cv2.imread('path_to_mask.png', cv2.IMREAD_GRAYSCALE)

# Create an inverse mask
inverse_mask = cv2.bitwise_not(mask)

# Extract the generated polygon area using the mask
generated_part = cv2.bitwise_and(generated_image, generated_image, mask=mask)

# Extract the surrounding area by using the inverse mask
surrounding_area = cv2.bitwise_and(generated_image, generated_image, mask=inverse_mask)

# Compute the mean color and brightness of the surrounding area
mean_color_surrounding = cv2.mean(surrounding_area, mask=inverse_mask)[:3]

# Convert the generated part to HSV
hsv_generated_part = cv2.cvtColor(generated_part, cv2.COLOR_BGR2HSV)

# Split the HSV image into individual channels
h, s, v = cv2.split(hsv_generated_part)

# Adjust the value channel to match the average brightness of the surrounding area
mean_brightness_surrounding = cv2.mean(v, mask=mask)[0]
v = cv2.add(v, int(mean_brightness_surrounding - cv2.mean(v, mask=mask)[0]))

# Merge the adjusted channels back into an HSV image
adjusted_hsv_part = cv2.merge([h, s, v])

# Convert the adjusted HSV image back to BGR
adjusted_part = cv2.cvtColor(adjusted_hsv_part, cv2.COLOR_HSV2BGR)

# Adjust the color to match the surrounding area
adjusted_part = cv2.addWeighted(adjusted_part, 0.5, np.full_like(adjusted_part, mean_color_surrounding), 0.5, 0)

# Apply Gaussian blur to feather the edges of the adjusted area
feathered_part = cv2.GaussianBlur(adjusted_part, (21, 21), 0)

# Retain the original image's other parts using the inverse mask
background = cv2.bitwise_and(generated_image, generated_image, mask=inverse_mask)

# Blend the background with the adjusted and feathered generated area
blended_image = cv2.add(background, feathered_part)

# Save or display the result
cv2.imwrite('path_to_save_image.jpg', blended_image)
cv2.imshow('Blended Image', blended_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
