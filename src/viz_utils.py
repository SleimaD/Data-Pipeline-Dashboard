
from __future__ import annotations

import altair as alt
import pandas as pd
from typing import Iterable, Optional, Union

# Tiny viz helper so we don't repeat chart code in the app.
# Goal: consistent bar charts

def bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    *,
    x_sort: Optional[Union[str, Iterable]] = None,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    label_angle: int = 0,
) -> alt.Chart:

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            # Keep x labels readable and ordered t
            x=alt.X(f"{x}:O", sort=x_sort, axis=alt.Axis(title=x_title or x, labelAngle=label_angle)),
            # Y is quantitative (numbers).
            y=alt.Y(f"{y}:Q", axis=alt.Axis(title=y_title or y)),
        )
    )

    if title:
        chart = chart.properties(title=title)

    return chart
