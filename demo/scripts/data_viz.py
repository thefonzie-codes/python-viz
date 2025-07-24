import pandas as pd
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Load Data ---
with open('data/retention_kpi.json', 'r') as f:
    retention_kpi = json.load(f)
student_composition_df = pd.read_csv('data/student_composition.csv')
retention_by_school_df = pd.read_csv('data/retention_by_school.csv')
district_withdrawals_df = pd.read_csv('data/district_withdrawals.csv')
withdrawal_reasons_df = pd.read_csv('data/withdrawal_reasons.csv')

# --- Color and Style Definitions ---
BACKGROUND_COLOR = '#F8F9FA'
PLOT_BACKGROUND_COLOR = '#FFFFFF'
FONT_FAMILY = "Arial, sans-serif"
FONT_COLOR = "#555"
TITLE_FONT_COLOR = "#333"
MAIN_BLUE = 'rgb(42, 175, 221)'

REASON_COLORS = {
    'Elementary With': '#014B86',
    'EXP CAN\'T RET': '#F77E24',
    'OTHER (UNKNOWN)': '#8DC63F',
    'Enroll In Other': '#62C0DD',
    'Transferred to': '#522D80',
    'ADMIN WITHDRAW': '#ADD8E6', # A light blue for this minor category
    'HOME SCHOOLING': '#BACB1F'  # Not in data, but defined for completeness
}

# --- Create Subplots ---
fig = make_subplots(
    rows=2, cols=2,
    specs=[
        [{"type": "xy"}, {"type": "bar"}],
        [{"type": "domain"}, {"type": "bar"}]
    ],
    subplot_titles=(
        "<b>STUDENT RETENTION</b>",
        "<b>RETENTION BY SCHOOL</b>",
        "<b>TOP WITHDRAWAL REASONS</b>",
        "<b>DISTRICT WITHDRAWALS</b>"
    ),
    vertical_spacing=0.15,
    horizontal_spacing=0.05
)

# --- Plot 1: Student Retention ---
fig.add_trace(go.Bar(
    y=student_composition_df['Category'],
    x=student_composition_df['Count'],
    orientation='h',
    marker_color=MAIN_BLUE,
    text=[f"{x/1000:.1f}K" for x in student_composition_df['Count']],
    textposition='outside',
    insidetextanchor='end',
    textfont=dict(color=FONT_COLOR, size=12),
    width=0.4
), row=1, col=1)

fig.add_annotation(
    text=f"<b>{retention_kpi['retention_rate']}%</b>",
    align='left', x=0.05, y=0.8, xref="paper", yref="paper",
    showarrow=False, font=dict(size=48, color=MAIN_BLUE), row=1, col=1
)
fig.add_annotation(
    text="Retention",
    align='left', x=0.05, y=0.7, xref="paper", yref="paper",
    showarrow=False, font=dict(size=16, color=FONT_COLOR), row=1, col=1
)


# --- Plot 2: Retention by School ---
fig.add_trace(go.Bar(
    x=retention_by_school_df['Campus'],
    y=retention_by_school_df['RetentionRate'],
    marker_color=MAIN_BLUE,
    text=[f"{r}%" for r in retention_by_school_df['RetentionRate']],
    textposition='auto',
    insidetextfont=dict(color='white', size=12, family=FONT_FAMILY)
), row=1, col=2)


# --- Plot 3: Top Withdrawal Reasons ---
pie_data = withdrawal_reasons_df[withdrawal_reasons_df['Percentage'] > 0].copy()
# Shorten labels for legend display
pie_data['LegendLabel'] = pie_data['Reason'].str.replace(' \(UNKNOWN\)', ' (U...').str.replace('CAN\'T RET', 'CAN\'...').str.replace('Elementary With', 'Elementar...')
fig.add_trace(go.Pie(
    labels=pie_data['LegendLabel'],
    values=pie_data['Percentage'],
    hole=0.4,
    marker_colors=[REASON_COLORS.get(r, '#ccc') for r in pie_data['Reason']],
    textinfo='percent',
    textfont=dict(size=12, color='white'),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    insidetextorientation='radial',
), row=2, col=1)


# --- Plot 4: District Withdrawals ---
months_order = ['August', 'September', 'October', 'November', 'December', 'January', 'February', 'March', 'April']
reason_order = list(REASON_COLORS.keys())

# Create a pivot table to ensure all months/reasons are present for stacking
pivot_df = district_withdrawals_df.pivot_table(
    index='Month', columns='Reason', values='Count', aggfunc='sum'
).fillna(0)
pivot_df = pivot_df.reindex(months_order) # Sort months correctly

for reason in reason_order:
    if reason in pivot_df.columns:
        fig.add_trace(go.Bar(
            name=reason,
            x=pivot_df.index,
            y=pivot_df[reason],
            marker_color=REASON_COLORS[reason]
        ), row=2, col=2)

# Add total labels on top of stacked bars
totals = pivot_df.sum(axis=1)
fig.add_trace(go.Scatter(
    x=totals.index,
    y=totals,
    text=totals.astype(int),
    mode='text',
    textposition='top center',
    textfont=dict(color=FONT_COLOR, size=11),
    showlegend=False
), row=2, col=2)


# --- Update Layout and Final Styling ---
fig.update_layout(
    height=750,
    width=1200,
    paper_bgcolor=BACKGROUND_COLOR,
    plot_bgcolor=PLOT_BACKGROUND_COLOR,
    font=dict(family=FONT_FAMILY, size=12, color=FONT_COLOR),
    showlegend=True,
    barmode='stack',

    # Main Title and Subtitle
    annotations=[
        # Main Title
        go.layout.Annotation(
            text="<b>SchoolAnalytix®</b>",
            xref="paper", yref="paper",
            x=0.01, y=0.99, xanchor='left', yanchor='top',
            showarrow=False, font=dict(size=24, color=TITLE_FONT_COLOR)
        ),
        # Page Title
        go.layout.Annotation(
            text="<span style='font-size: 24px;'><b>Student Retention</b></span><br><span style='color:#888'>Data Last Updated: 4/3/2023 6:14:07 PM</span>",
            xref="paper", yref="paper",
            x=0.01, y=0.90, xanchor='left', yanchor='top',
            align='left', showarrow=False, font=dict(size=14, color=TITLE_FONT_COLOR)
        )
    ],

    # Specific subplot styling
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True, domain=[0.1, 0.9]),
    yaxis2=dict(showgrid=False, range=[0, 100], fixedrange=True),
    xaxis2=dict(showgrid=False, fixedrange=True),
    legend=dict(
        orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.25,
        traceorder='normal', bgcolor='rgba(0,0,0,0)',
        font=dict(size=11)
    ),
    legend2=dict(
        yanchor="top", y=1, xanchor="left", x=1.01,
        traceorder='normal', bgcolor='rgba(0,0,0,0)',
        font=dict(size=11)
    ),
    yaxis4=dict(range=[0, 110], showgrid=True, gridcolor='#EAEAEA', fixedrange=True),
    xaxis4=dict(showgrid=False, type='category', fixedrange=True),
    margin=dict(l=20, r=20, t=180, b=80),
)

# Update subplot titles style
for i in fig['layout']['annotations']:
    if '<b>' in i['text']: # Differentiate subplot titles
        i['font'] = dict(size=13, color=TITLE_FONT_COLOR)
        i['xanchor'] = 'left'
        if i['xref'] != 'paper': # Don't realign main titles
             i['x'] = 0

# Hide legends for plots that don't need them
fig.data[0].showlegend = False # Student Comp bar
fig.data[1].showlegend = False # Retention by School bar
fig.update_traces(selector=dict(type='pie'), showlegend=True, legendgroup='group1', legend="legend")
fig.update_traces(selector=dict(xaxis='x4'), showlegend=True, legendgroup='group2', legend="legend2")

fig.show()
