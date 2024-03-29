# https://towardsdatascience.com/simple-plagiarism-detection-in-python-2314ac3aee88
import re

import nltk
import numpy as np
import plotly.graph_objects as go
from nltk.lm import WittenBellInterpolated
from nltk.tokenize import word_tokenize
from nltk.util import everygrams, pad_sequence
from scipy.ndimage import gaussian_filter


def check_plagarism(data1, data2):
    nltk.download("punkt")
    # Training data file
    train_data_file = "../../testing.txt"
    with open(train_data_file, "w") as out:
        out.write(data1)
    # read training data
    with open(train_data_file) as f:
        train_text = f.read().lower()
    # apply preprocessing (remove text inside square and curly brackets and rem punc)
    train_text = re.sub(r"\[.*\]|\{.*\}", "", train_text)
    train_text = re.sub(r"[^\w\s]", "", train_text)
    # set ngram number
    n = 4
    # pad the text and tokenize
    training_data = list(
        pad_sequence(word_tokenize(train_text), n, pad_left=True, left_pad_symbol="<s>")
    )
    # generate ngrams
    ngrams = list(everygrams(training_data, max_len=n))
    # print("Number of ngrams:", len(ngrams))
    # build ngram language models
    model = WittenBellInterpolated(n)
    model.fit([ngrams], vocabulary_text=training_data)
    # testing data file
    test_data_file = "../../testing2.txt"
    with open(test_data_file, "w") as out:
        out.write(data2)
    # Read testing data
    with open(test_data_file) as f:
        test_text = f.read().lower()
    # test_text = data2.lower()
    test_text = re.sub(r"[^\w\s]", "", test_text)

    # Tokenize and pad the text
    testing_data = list(
        pad_sequence(word_tokenize(test_text), n, pad_left=True, left_pad_symbol="<s>")
    )
    # print("Length of test data:", len(testing_data))

    # assign scores
    scores = []
    for i, item in enumerate(testing_data[n - 1 :]):
        s = model.score(item, testing_data[i : i + n - 1])
        scores.append(s)

    scores_np = np.array(scores)

    # set width and height
    width = 8
    height = np.ceil(len(testing_data) / width).astype("int32")
    # print("Width, Height:", width, ",", height)

    score = sum(scores_np) / len(scores_np) * 100
    score = round(score, 4)
    plagarized = score > 20
    # print("Plagarism Score: "+str(score)+"%\nPlagarized: "+str(plagarized))
    # copy scores to rectangular blank array
    a = np.zeros(width * height)
    a[: len(scores_np)] = scores_np
    diff = len(a) - len(scores_np)
    # apply gaussian smoothing for aesthetics
    a = gaussian_filter(a, sigma=1.0)
    # reshape to fit rectangle
    a = a.reshape(-1, width)
    # format labels
    labels = [
        " ".join(testing_data[i : i + width])
        for i in range(n - 1, len(testing_data), width)
    ]
    labels_individual = [x.split() for x in labels]
    labels_individual[-1] += [""] * diff
    labels = [f"{x:60.60}" for x in labels]

    # course heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=a,
            x0=0,
            dx=1,
            y=labels,
            zmin=0,
            zmax=1,
            customdata=labels_individual,
            hovertemplate="%{customdata} <br><b>Score:%{z:.3f}<extra></extra>",
            colorscale="burg",
        )
    )
    fig.update_layout(
        {"height": height * 28, "width": 1000, "font": {"family": "Courier New"}}
    )
    fig["layout"]["yaxis"]["autorange"] = "reversed"
    fig.write_image("plagarism.png")
    import base64

    image_data = open("plagarism.png", "rb").read()
    encoded = base64.b64encode(image_data)  # Creates a bytes object
    encoded = "data:image/png;base64,{}".format(str(encoded).strip("b'").strip("'"))
    # delete file
    import os

    os.remove("plagarism.png")
    return [score, plagarized, encoded]
