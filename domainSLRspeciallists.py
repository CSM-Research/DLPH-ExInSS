import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ======================
# CONTROLES DE ESTILO
# ======================
FONT_FAMILY = "Times New Roman"
TITLE_FONT_SIZE = 25
AXIS_LABEL_FONT_SIZE = 20
TICK_FONT_SIZE = 20
LEGEND_FONT_SIZE = 20
VALUE_FONT_SIZE = 20

# ======================
# CONFIGURAÇÃO GLOBAL
# ======================
plt.rcParams["font.family"] = FONT_FAMILY

# ======================
# ARQUIVO E SHEETS
# ======================
file_path = "dataForChart.xlsx"

domain_df = pd.read_excel(file_path, sheet_name="domainExpertAssistance")
ss_df = pd.read_excel(file_path, sheet_name="SSExpertAssistance")

# ======================
# LIKERT
# ======================
likert_map = {
    1: "Strongly Disagree",
    2: "Disagree",
    3: "Agree",
    4: "Strongly Agree"
}

likert_order = [1, 2, 3, 4]
labels = list(likert_map.values())

# Tons de cinza (escuro → claro)
gray_colors = ["#4D4D4D", "#7F7F7F", "#B2B2B2", "#D9D9D9"]

# Texto branco para áreas escuras
text_colors = ["white", "white", "black", "black"]

def likert_counts(df):
    return pd.DataFrame({
        likert_map[v]: df.apply(lambda x: (x == v).sum())
        for v in likert_order
    })

domain_counts = likert_counts(domain_df)
ss_counts = likert_counts(ss_df)

criteria = domain_counts.index
y = np.arange(len(criteria))

# ======================
# PLOT (VERTICAL)
# ======================
fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharey=True)

for ax, counts, title in zip(
    axes,
    [domain_counts, ss_counts],
    ["(a) Domain Expert Assistance", "(b) SS Expert Assistance"]
):
    left = np.zeros(len(criteria))

    for label, color, txt_color in zip(labels, gray_colors, text_colors):
        bars = ax.barh(
            y,
            counts[label],
            left=left,
            color=color,
            edgecolor="black",
            label=label
        )

        # Valores dentro das barras
        for bar in bars:
            width = bar.get_width()
            if width > 0:
                ax.text(
                    bar.get_x() + width / 2,
                    bar.get_y() + bar.get_height() / 2,
                    int(width),
                    ha="center",
                    va="center",
                    fontsize=VALUE_FONT_SIZE,
                    color=txt_color
                )

        left += counts[label].values

    ax.set_title(title, fontsize=TITLE_FONT_SIZE)
    ax.set_xlabel("Frequency", fontsize=AXIS_LABEL_FONT_SIZE)
    ax.set_yticks(y)
    ax.set_yticklabels(criteria, fontsize=TICK_FONT_SIZE)
    ax.tick_params(axis="x", labelsize=TICK_FONT_SIZE)
    ax.invert_yaxis()

# ======================
# LEGENDA GLOBAL (FORA)
# ======================
handles, legend_labels = axes[0].get_legend_handles_labels()

fig.legend(
    handles,
    legend_labels,
    loc="lower center",
    ncol=4,
    fontsize=LEGEND_FONT_SIZE,
    frameon=False
)

# Espaço para legenda
plt.tight_layout(rect=[0, 0.08, 1, 1])

plt.show()
