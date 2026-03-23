from flask import Flask, render_template, request
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("uploads", exist_ok=True)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    preview = ""
    plots = []   # move outside POST

    if request.method == "POST":

        file = request.files['file']

        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath)
        preview = df.to_html()

        num_cols = df.select_dtypes(include="number")
        cat_cols = df.select_dtypes(include="object")

        # Numeric plots
        for num_col in num_cols[:3]:
            safe_name = num_col.replace(" ", "_")
            plt.figure()
            plt.hist(df[num_col])
            plt.title(num_col)
            plt.savefig(f"static/plots/{safe_name}.png")
            plt.close()
            plots.append(f"plots/{safe_name}.png")

        # Categorical plots
        for cat_col in cat_cols[:2]:
            safe_name = cat_col.replace(" ", "_")

            # skip useless columns
            if df[cat_col].nunique() > 20:
                continue

            plt.figure()
            df[cat_col].value_counts().head(5).plot(kind="bar")
            plt.title(cat_col)
            plt.savefig(f"static/plots/{safe_name}.png")
            plt.close()
            plots.append(f"plots/{safe_name}.png")
            
    return render_template("index.html", preview=preview, plots=plots)

app.run(debug=True)