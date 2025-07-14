import pandas as pd
import plotly.graph_objects as go

def load_data():
    metrics = pd.read_csv("../data/metrics.csv")
    channel = pd.read_csv("../data/channel_acquisition.csv", parse_dates=["date"])
    arr     = pd.read_csv("../data/arr_movement.csv")
    funnel  = pd.read_csv("../data/funnel_data.csv")
    cohort  = pd.read_csv("../data/cohort_data.csv")
    return metrics, channel, arr, funnel, cohort

def create_dashboard(metrics, channel, arr, funnel, cohort, output="../outputs/dashboard.html"):
    # ── Row 1: Indicators ───────────────────────────────────────────────────────
    indicator_figs = []
    for i, row in metrics.iterrows():
        prefix = "" if pd.isna(row["prefix"]) else row["prefix"]
        suffix = "" if pd.isna(row["suffix"]) else row["suffix"]
        indicator_figs.append(
            go.Figure(go.Indicator(
                mode="number",
                title={
                    "text": f"<b>{str(row['metric']).upper()}</b>",
                    "font": {"size": 12}
                },
                value=row["value"],
                number={
                    "prefix": prefix,
                    "suffix": suffix,
                    "font": {"size": 32, "weight": "bold"}
                }
            )).update_layout(
                height=70,
                margin=dict(t=10, b=0, l=10, r=10),
                template="plotly_white",
            )
        )

    # ── Row 2 Col 1–3: Stacked area chart ─────────────────────────────────────
    # Subset of dates for x-axis labels, skipping the first N and last N
    N = 2  # Number of dates to skip at start and end
    tick_dates = channel["date"][N:-N:3] if len(channel["date"]) > 2*N else channel["date"][::3]
    area_fig = go.Figure()
    for ch in [c for c in channel.columns if c != "date"]:
        area_fig.add_trace(
            go.Scatter(
                x=channel["date"],
                y=channel[ch],
                name=ch,
                stackgroup="one",
                hoverinfo="x+y"
            )
        )
    area_fig.update_xaxes(
        tickmode="array",
        tickvals=tick_dates,
        ticktext=[d.strftime("%b %Y") for d in tick_dates]
    )
    area_fig.update_yaxes(title_text="New Customers", showticklabels=False)
    area_fig.update_layout(
        template="plotly_white",
        showlegend=True,
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
        margin=dict(l=10, r=10, t=60, b=10),
        height=450,
        title=dict(
            text="<b>Channel Acquisition Trends</b>",
            x=0.01,
            xanchor="left",
            y=0.97,
            yanchor="top",
            font=dict(size=18)
        )
    )

    # ── Row 2 Col 3-5: Waterfall chart ───────────────────────────────────────────
    waterfall_fig = go.Figure(go.Waterfall(
        x=arr["category"].tolist(),
        y=arr["value"].tolist(),
        measure=arr["measure"].tolist(),
        connector={"line":{"color": "rgba(0, 0, 0, 0.15)"}}
    ))
    waterfall_fig.update_xaxes(tickangle=-45)
    waterfall_fig.update_yaxes(tickformat="~s")
    waterfall_fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=60, b=10),
        height=450,
        title=dict(
            text="<b>ARR Movement Analysis</b>",
            x=0.01,
            xanchor="left",
            y=0.97,
            yanchor="top",
            font=dict(size=18)
        )
    )

    # ── Row 3 Col 1–2: Sankey diagram ─────────────────────────────────────────
    labels = list(pd.unique(funnel[["source","target"]].values.ravel()))
    src = funnel["source"].apply(lambda x: labels.index(x)).tolist()
    tgt = funnel["target"].apply(lambda x: labels.index(x)).tolist()
    sankey_fig = go.Figure(go.Sankey(
        node=dict(label=labels, pad=15, thickness=20),
        link=dict(source=src, target=tgt, value=funnel["value"].tolist())
    ))
    sankey_fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=60, b=10),
        height=350,
        title=dict(
            text="<b>Customer Acquisition Funnel</b>",
            x=0.01,
            xanchor="left",
            y=0.97,
            yanchor="top",
            font=dict(size=18)
        )
    )

    # ── Row 3 Col 3-5: Heatmap ─────────────────────────────────────────────────
    cohort_columns = cohort.columns[1:13]
    cohort_matrix = cohort.set_index("cohort")[cohort_columns].values
    heatmap_fig = go.Figure(go.Heatmap(
        z=cohort_matrix,
        x=cohort_columns.tolist(),
        y=cohort["cohort"].tolist(),
        colorbar={"title":"Retention %"},
        zmin=40, zmax=100
    ))
    heatmap_fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=60, b=10),
        height=350,
        xaxis=dict(
            side="top",
            ticks="outside",
            ticklen=6,
            tickcolor="#ecf0f7",
            tickangle=0
        ),
        yaxis=dict(
            showticklabels=False
        ),
        title=dict(
            text="<b>Cohort Retention Analysis</b>",
            x=0.01,
            xanchor="left",
            y=0.97,
            yanchor="top",
            font=dict(size=18)
        )
    )

    # Custom HTML for dashboard layout
    custom_html = f"""
<style>
.card {{
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 2px 12px rgba(50,50,93,0.07), 0 1.5px 4px rgba(0,0,0,0.07);
    padding: 18px;
    margin: 2px;
    transition: box-shadow 0.2s;
}}
.card:hover {{
    box-shadow: 0 4px 24px rgba(50,50,93,0.13), 0 3px 8px rgba(0,0,0,0.13);
}}
.nested-card {{
    background: #f4f4f4;
    border-radius: 8px;
    padding: 6px 8px;
    position: relative;
    font-size: 12px;
    text-align: center;
    color: #666;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}}
.positive {{
    color: #27ae60;
    font-weight: bold;
    font-family: "Open Sans", verdana, arial, sans-serif;
}}
.negative {{
    color: #c0392b;
    font-weight: bold;
    font-family: "Open Sans", verdana, arial, sans-serif;
}}
.dashboard-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: 0.15fr 0.4fr 0.45fr;
    gap: 12px;
    width: 100%;
    max-width: 1600px;
    margin: auto;
}}
</style>
<div class="dashboard-grid">
    <!-- Row 1: Indicator Cards -->
    {''.join([
        f'''
        <div class="card" style="grid-row:1;grid-column:{i+1};">
            {indicator_figs[i].to_html(full_html=False, include_plotlyjs='cdn' if i==0 else False, default_height='250px')}
            <div class="nested-card">
                <span class="{('positive' if pd.notna(metrics.iloc[i]['delta']) and float(metrics.iloc[i]['delta']) > 0 else 'negative') if pd.notna(metrics.iloc[i]['delta']) and float(metrics.iloc[i]['delta']) != 0 else ''}">
                    {
                        '%.1f%%' % float(metrics.iloc[i]['delta']) if pd.notna(metrics.iloc[i]['delta']) and str(metrics.iloc[i]['suffix']) == 'M'
                        else f"{str(metrics.iloc[i]['prefix']) if pd.notna(metrics.iloc[i]['prefix']) else ''}{str(metrics.iloc[i]['delta']) if pd.notna(metrics.iloc[i]['delta']) else ''}{str(metrics.iloc[i]['suffix']) if pd.notna(metrics.iloc[i]['suffix']) else ''}"
                    }
                </span>
            </div>
        </div>
        ''' for i in range(5)
    ])}
    <!-- Row 2: Area and Waterfall Charts -->
    <div class="card" style="grid-row:2;grid-column:1/4;">
        {area_fig.to_html(full_html=False, include_plotlyjs=False, default_height='450px')}
    </div>
    <div class="card" style="grid-row:2;grid-column:4/6;">
        {waterfall_fig.to_html(full_html=False, include_plotlyjs=False, default_height='350px')}
    </div>
    <!-- Row 3: Sankey and Heatmap -->
    <div class="card" style="grid-row:3;grid-column:1/3;">
        {sankey_fig.to_html(full_html=False, include_plotlyjs=False, default_height='350px')}
    </div>
    <div class="card" style="grid-row:3;grid-column:3/6;">
        {heatmap_fig.to_html(full_html=False, include_plotlyjs=False, default_height='350px')}
    </div>
</div>
"""

    with open(output, "w") as f:
        f.write(custom_html)

if __name__ == "__main__":
    metrics, channel, arr, funnel, cohort = load_data()
    create_dashboard(metrics, channel, arr, funnel, cohort)
    print("Dashboard created successfully!")

