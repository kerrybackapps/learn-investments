# Utility functions for handling unavailable data sources
import plotly.graph_objects as go
from pages.formatting import largefig

def create_unavailable_message_fig(message="Access to Ken French's Data Library is temporarily unavailable."):
    """
    Creates a Plotly figure displaying a message about unavailable data.

    Args:
        message: The message to display

    Returns:
        A Plotly figure object
    """
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color="red"),
        align="center",
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return largefig(fig)

def create_unavailable_table():
    """
    Creates an empty table structure for when data is unavailable.

    Returns:
        An empty list (for Dash DataTable)
    """
    return [{"message": "Data temporarily unavailable"}]
