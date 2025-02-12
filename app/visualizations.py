import matplotlib.pyplot as plt
import squarify
import io

def plot_treemap(exposure):
    labels = list(exposure.keys())
    sizes = list(exposure.values())

    plt.figure(figsize=(6, 6))
    squarify.plot(sizes=sizes, label=labels, alpha=0.7)
    plt.axis("off")

    img_io = io.BytesIO()
    plt.savefig(img_io, format="png", bbox_inches="tight")
    img_io.seek(0)
    return img_io