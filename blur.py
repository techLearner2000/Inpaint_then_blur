import cv2
import numpy as np

# 加载生成的图片和掩码
generated_image = cv2.imread('path_to_generated_image.jpg')
mask = cv2.imread('path_to_mask.png', cv2.IMREAD_GRAYSCALE)

# 创建一个反向的掩码
inverse_mask = cv2.bitwise_not(mask)

# 提取生成区域
generated_part = cv2.bitwise_and(generated_image, generated_image, mask=mask)

# 对生成区域进行高斯模糊处理，以羽化边缘
blurred_generated_part = cv2.GaussianBlur(generated_part, (21, 21), 0)

# 调整颜色和亮度（根据需要）
hsv_image = cv2.cvtColor(blurred_generated_part, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv_image)
v = cv2.equalizeHist(v)
hsv_image = cv2.merge([h, s, v])
adjusted_part = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

# 将处理后的生成区域与原图融合
# 保留原图的其他部分
background = cv2.bitwise_and(generated_image, generated_image, mask=inverse_mask)
# 融合背景和处理后的生成区域
blended_image = cv2.add(background, adjusted_part)

# 保存或显示结果
cv2.imwrite('path_to_save_image.jpg', blended_image)
cv2.imshow('Blended Image', blended_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
