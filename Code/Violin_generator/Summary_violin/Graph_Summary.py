import fitz  # PyMuPDF
import io
import matplotlib.pyplot as plt
from PIL import Image

# ==== 需要合并的 6 份 PDF 文件路径（请按实际文件名修改）====
pdf_files = [
    "3.Flanker Letter(Congruent vs. Incongruent).pdf",
    "3.Flanker Number(Congruent vs. Incongruent).pdf",
    "3.Stroop(Congruent vs. Incongruent).pdf",
    "4.Flanker Letter(4 Condition Comparisons).pdf",
    "4.Flanker Number(4 Condition Comparisons).pdf",
    "Flanker_Letter_Comparison.pdf"
]

# ==== 1) 将 PDF 首页转为图像（存到列表中） ====
pixmaps = []
for pdf in pdf_files:
    doc = fitz.open(pdf)
    page = doc.load_page(0)       # 只读取第 1 页
    # dpi=200 可以根据需要改大/改小
    pix = page.get_pixmap(dpi=300)
    pixmaps.append(pix)
    doc.close()

# ==== 2) 用 Matplotlib 在 2×3 网格里展示这些图像 ====
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(24, 15))  # 可调节大小
axs = axs.flatten()  # 让 axs 变成一维，方便用索引 [0..5]

for i, ax in enumerate(axs):
    # 把 Pixmap 转换成 PIL Image
    img_data = pixmaps[i].tobytes("png")        # 得到 PNG 字节流
    img = Image.open(io.BytesIO(img_data))      # 转成 PIL Image
    ax.imshow(img)    # 可按需加标题
    ax.axis("off")                              # 不显示坐标轴

plt.tight_layout()

# ==== 3) 保存为 PDF 或 PNG ====
plt.savefig("merged_6_pdfs.pdf", dpi=300, bbox_inches='tight')  # 输出 PDF
# 如果想再存个 PNG，也可以加一句:
# plt.savefig("merged_6_pdfs.png", dpi=300, bbox_inches='tight')

plt.show()
