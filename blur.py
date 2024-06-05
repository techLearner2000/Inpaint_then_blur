import cv2
import numpy as np

# 加载生成的图片
generated_image = cv2.imread('path_to_generated_image.jpg')

# 假设我们需要对整个图像进行处理以使其更自然
# 对边缘进行高斯模糊处理，以羽化边缘
blurred_image = cv2.GaussianBlur(generated_image, (21, 21), 0)

# 调整颜色和亮度（根据需要）
# 这里可以使用直方图均衡化或其他方法
# 示例：将图像转换为HSV颜色空间，调整亮度和饱和度
hsv_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv_image)
v = cv2.equalizeHist(v)
hsv_image = cv2.merge([h, s, v])
adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

# 添加噪声
noise = np.random.normal(0, 25, adjusted_image.shape).astype(np.uint8)
noisy_image = cv2.add(adjusted_image, noise)

# 保存或显示结果
cv2.imwrite('path_to_save_image.jpg', noisy_image)
cv2.imshow('Processed Image', noisy_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
