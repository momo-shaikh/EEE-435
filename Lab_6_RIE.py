import numpy as np
import plotly.graph_objects as go

# Your measured etch rates with 9.01 at center position (index 9)
etch_rates = np.array([
    8.85, 8.90, 8.92, 8.95, 8.97, 8.99, 8.99, 9.00, 8.99, 9.01,
    8.99, 8.98, 8.98, 8.97, 8.96, 8.96, 8.94, 8.92, 8.92
])

# Create a coordinate grid for the wafer
n_points = 100  # Number of points for interpolation
radius = 150  # Assuming 300mm wafer
x = np.linspace(-radius, radius, n_points)
y = np.linspace(-radius, radius, n_points)
X, Y = np.meshgrid(x, y)

# Convert to radial coordinates
R = np.sqrt(X**2 + Y**2)

# Create radial positions for the original data points
half_points = len(etch_rates) // 2
r_measured = np.linspace(0, radius, half_points + 1)

# Create the 2D array using numpy's interpolation
z = np.zeros_like(X)
for i in range(len(x)):
    for j in range(len(y)):
        r = np.sqrt((x[i])**2 + (y[j])**2)
        if r <= radius:
            z[j, i] = np.interp(r, r_measured, etch_rates[half_points::-1])
        else:
            z[j, i] = np.nan  # Set points outside wafer to NaN

# Create the contour plot
fig = go.Figure(data=go.Contour(
    z=z,
    x=x,
    y=y,
    colorscale='Spectral_r',
    contours=dict(
        start=8.85,
        end=9.01,
        size=0.02,
        showlabels=True,
        labelfont=dict(size=12, color='black')
    ),
    colorbar=dict(
        title=dict(
            text='Etch Rate (Å/s)',
            side='right',
            font=dict(size=14),
            #pad=15  # Add padding between title and colorbar
        ),
        x=1.15,  # Move colorbar further right
        len=0.9,  # Adjust length of colorbar
        dtick=0.02
    ),
    ncontours=16,
    zmin=8.85,
    zmax=9.01
))

# Update layout
fig.update_layout(
    title='RIE Etch Rate Distribution (Bullseye Effect)',
    xaxis_title='Position (mm)',
    yaxis_title='Position (mm)',
    width=800,  # Increased width to accommodate colorbar
    height=600,
    showlegend=False,
    plot_bgcolor='white',
    margin=dict(r=150)  # Increased right margin to prevent label cutoff
)

# Make it circular like a wafer
fig.update_layout(
    shapes=[dict(
        type="circle",
        xref="x",
        yref="y",
        x0=-radius,
        y0=-radius,
        x1=radius,
        y1=radius,
        line_color="black",
        line_width=2,
        fillcolor='rgba(255,255,255,0)'
    )]
)

# Show the plot
fig.show()