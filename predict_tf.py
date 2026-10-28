"""加载 TensorFlow 模型识别本地图片，不要求 CUDA。"""

import argparse
import json
from pathlib import Path

import numpy as np

from tf_data import ROOT, preprocess_image
from tf_model import load_model


def main():
    parser = argparse.ArgumentParser(description="使用 TensorFlow 模型识别图片")
    parser.add_argument("images", nargs="*", type=Path)
    parser.add_argument("--model", type=Path, default=ROOT / "artifacts" / "model.keras")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    paths = args.images or [ROOT / f"img{i}.png" for i in range(1, 4)]
    batch = np.stack([preprocess_image(path) for path in paths])
    outputs = load_model(args.model)(batch, training=False).numpy()
    probabilities = np.exp(outputs)
    results = []
    for path, scores in zip(paths, probabilities):
        prediction = int(scores.argmax())
        results.append({"image": str(path), "prediction": prediction, "probabilities": scores.tolist()})
        print(f"{path.name}：预测 {prediction}，置信度 {scores[prediction]:.2%}")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
