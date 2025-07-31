"""
Tube Calculator App for Space Vehicle Engineering
A comprehensive tool for calculating mass, volume, and total length of tubing systems
with 2D visualization and export capabilities.

Author: Jthomas
Date: July 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
from io import BytesIO
import CoolProp.CoolProp as CP
from CoolProp.CoolProp import PropsSI

# Configure Streamlit page
st.set_page_config(
    page_title="Tube and PipeCalculator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Material properties database
MATERIALS = {
    "Stainless Steel 316L": {"density": 8000, "density_imperial": 0.289},  # kg/m³, lb/in³
    "Stainless Steel 321": {"density": 8030, "density_imperial": 0.290},
    "Stainless Steel 347": {"density": 8030, "density_imperial": 0.290},
    "Stainless Steel 15-7 PH": {"density": 7800, "density_imperial": 0.282},
    "Aluminum 6061-T6": {"density": 2700, "density_imperial": 0.098},
    "Aluminum 2024-T3": {"density": 2780, "density_imperial": 0.100},
    "Aluminum 7075-T6": {"density": 2810, "density_imperial": 0.102},
    "Titanium Ti-6Al-4V": {"density": 4430, "density_imperial": 0.160},
    "Titanium Grade 2": {"density": 4510, "density_imperial": 0.163},
    "Titanium Ti-3Al-2.5V": {"density": 4480, "density_imperial": 0.162},
    "Inconel 625": {"density": 8440, "density_imperial": 0.305},
    "Inconel 718": {"density": 8220, "density_imperial": 0.297},
    "Inconel X-750": {"density": 8280, "density_imperial": 0.299},
    "Monel 400": {"density": 8830, "density_imperial": 0.319},
    "Monel K-500": {"density": 8440, "density_imperial": 0.305},
    "Hastelloy C-276": {"density": 8890, "density_imperial": 0.321},
    "Hastelloy X": {"density": 8220, "density_imperial": 0.297},
    "Copper C101": {"density": 8940, "density_imperial": 0.323},
    "Copper C110": {"density": 8960, "density_imperial": 0.324},
    "Brass 360": {"density": 8500, "density_imperial": 0.307},
    "Nickel 200": {"density": 8890, "density_imperial": 0.321},
    "Nimonic 90": {"density": 8180, "density_imperial": 0.295},
    "Waspaloy": {"density": 8220, "density_imperial": 0.297}
}

# Standard tube sizes (Outer Diameter in mm and inches)
TUBE_SIZES = {
    "1/8\"": {"od_mm": 3.175, "od_in": 0.125},
    "3/16\"": {"od_mm": 4.763, "od_in": 0.1875},
    "1/4\"": {"od_mm": 6.35, "od_in": 0.25},
    "5/16\"": {"od_mm": 7.938, "od_in": 0.3125},
    "3/8\"": {"od_mm": 9.525, "od_in": 0.375},
    "1/2\"": {"od_mm": 12.7, "od_in": 0.5},
    "5/8\"": {"od_mm": 15.875, "od_in": 0.625},
    "3/4\"": {"od_mm": 19.05, "od_in": 0.75},
    "7/8\"": {"od_mm": 22.225, "od_in": 0.875},
    "1\"": {"od_mm": 25.4, "od_in": 1.0},
    "1-1/8\"": {"od_mm": 28.575, "od_in": 1.125},
    "1-1/4\"": {"od_mm": 31.75, "od_in": 1.25},
    "1-3/8\"": {"od_mm": 34.925, "od_in": 1.375},
    "1-1/2\"": {"od_mm": 38.1, "od_in": 1.5},
    "1-5/8\"": {"od_mm": 41.275, "od_in": 1.625},
    "1-3/4\"": {"od_mm": 44.45, "od_in": 1.75},
    "1-7/8\"": {"od_mm": 47.625, "od_in": 1.875},
    "2\"": {"od_mm": 50.8, "od_in": 2.0},
    "2-1/4\"": {"od_mm": 57.15, "od_in": 2.25},
    "2-1/2\"": {"od_mm": 63.5, "od_in": 2.5},
    "2-3/4\"": {"od_mm": 69.85, "od_in": 2.75},
    "3\"": {"od_mm": 76.2, "od_in": 3.0},
    "3-1/4\"": {"od_mm": 82.55, "od_in": 3.25},
    "3-1/2\"": {"od_mm": 88.9, "od_in": 3.5},
    "3-3/4\"": {"od_mm": 95.25, "od_in": 3.75},
    "4\"": {"od_mm": 101.6, "od_in": 4.0}
}

# Standard pipe sizes (Nominal Pipe Size - NPS)
PIPE_SIZES = {
    "1/8\" NPS": {"od_mm": 10.3, "od_in": 0.405},
    "1/4\" NPS": {"od_mm": 13.7, "od_in": 0.540},
    "3/8\" NPS": {"od_mm": 17.1, "od_in": 0.675},
    "1/2\" NPS": {"od_mm": 21.3, "od_in": 0.840},
    "3/4\" NPS": {"od_mm": 26.7, "od_in": 1.050},
    "1\" NPS": {"od_mm": 33.4, "od_in": 1.315},
    "1-1/4\" NPS": {"od_mm": 42.2, "od_in": 1.660},
    "1-1/2\" NPS": {"od_mm": 48.3, "od_in": 1.900},
    "2\" NPS": {"od_mm": 60.3, "od_in": 2.375},
    "2-1/2\" NPS": {"od_mm": 73.0, "od_in": 2.875},
    "3\" NPS": {"od_mm": 88.9, "od_in": 3.500},    "3-1/2\" NPS": {"od_mm": 101.6, "od_in": 4.000},
    "4\" NPS": {"od_mm": 114.3, "od_in": 4.500}
}

# Fluid properties database - common space vehicle fluids
FLUIDS = {
    "None": {"coolprop_name": None, "description": "No fluid (empty tube)"},
    "Hydrogen": {"coolprop_name": "Hydrogen", "description": "Gaseous or liquid hydrogen (H2)"},
    "Oxygen": {"coolprop_name": "Oxygen", "description": "Gaseous or liquid oxygen (O2)"},
    "Nitrogen": {"coolprop_name": "Nitrogen", "description": "Gaseous or liquid nitrogen (N2)"},
    "Helium": {"coolprop_name": "Helium", "description": "Helium gas (He)"},
    "Air": {"coolprop_name": "Air", "description": "Standard air mixture"},
    "Water": {"coolprop_name": "Water", "description": "Water (H2O)"},
    "Methane": {"coolprop_name": "Methane", "description": "Gaseous or liquid methane (CH4)"},
    "Propane": {"coolprop_name": "Propane", "description": "Gaseous or liquid propane (C3H8)"},
    "Carbon Dioxide": {"coolprop_name": "CarbonDioxide", "description": "Carbon dioxide (CO2)"},
    "Ammonia": {"coolprop_name": "Ammonia", "description": "Ammonia (NH3)"},
    "Argon": {"coolprop_name": "Argon", "description": "Argon gas (Ar)"},
    "Xenon": {"coolprop_name": "Xenon", "description": "Xenon gas (Xe)"},
    "Krypton": {"coolprop_name": "Krypton", "description": "Krypton gas (Kr)"},
    "Neon": {"coolprop_name": "Neon", "description": "Neon gas (Ne)"}
}

# Wall thickness options (in mm and inches)
WALL_THICKNESS = {
    "0.028\"": {"mm": 0.71, "in": 0.028},
    "0.035\"": {"mm": 0.89, "in": 0.035},
    "0.049\"": {"mm": 1.24, "in": 0.049},
    "0.065\"": {"mm": 1.65, "in": 0.065},
    "0.083\"": {"mm": 2.11, "in": 0.083},
    "0.095\"": {"mm": 2.41, "in": 0.095},
    "0.109\"": {"mm": 2.77, "in": 0.109},
    "0.120\"": {"mm": 3.05, "in": 0.120},
    "0.134\"": {"mm": 3.40, "in": 0.134},
    "0.148\"": {"mm": 3.76, "in": 0.148},
    "0.165\"": {"mm": 4.19, "in": 0.165},
    "0.180\"": {"mm": 4.57, "in": 0.180},
    "0.203\"": {"mm": 5.16, "in": 0.203},
    "0.220\"": {"mm": 5.59, "in": 0.220},
    "0.237\"": {"mm": 6.02, "in": 0.237},
    "0.250\"": {"mm": 6.35, "in": 0.250},
    "0.280\"": {"mm": 7.11, "in": 0.280},
    "0.300\"": {"mm": 7.62, "in": 0.300},
    "0.337\"": {"mm": 8.56, "in": 0.337},
    "0.375\"": {"mm": 9.53, "in": 0.375},
    "0.438\"": {"mm": 11.13, "in": 0.438},
    "0.500\"": {"mm": 12.70, "in": 0.500}
}

class TubeSegment:
    """Class to represent a tube segment with all its properties"""
    
    def __init__(self, name, tube_type, size, wall_thickness, length, material, units="metric", 
                 fluid_name="None", temperature=20, pressure=1.013, temp_units="C", pressure_units="bar"):
        self.name = name
        self.tube_type = tube_type  # "Tube" or "Pipe"
        self.size = size
        self.wall_thickness = wall_thickness
        self.length = length
        self.material = material
        self.units = units
        self.is_continuous = True
        
        # Fluid properties
        self.fluid_name = fluid_name
        self.temperature = temperature
        self.pressure = pressure
        self.temp_units = temp_units
        self.pressure_units = pressure_units
        
        # Calculate properties
        self._calculate_properties()
    
    def _calculate_properties(self):
        """Calculate volume, mass, and other properties"""
        if self.units == "metric":
            # Get dimensions in mm
            if self.tube_type == "Tube":
                od = TUBE_SIZES[self.size]["od_mm"]
            else:
                od = PIPE_SIZES[self.size]["od_mm"]
            
            wt = WALL_THICKNESS[self.wall_thickness]["mm"]
            length = self.length * 1000  # Convert m to mm
            density = MATERIALS[self.material]["density"]  # kg/m³
            
            # Calculate internal diameter
            id_mm = od - 2 * wt
            
            # Volume calculations (in m³)
            self.internal_volume = math.pi * (id_mm/2)**2 * length / 1e9  # m³
            self.material_volume = math.pi * ((od/2)**2 - (id_mm/2)**2) * length / 1e9  # m³
            
            # Tube mass calculation (in kg)
            self.tube_mass = self.material_volume * density
            
            # Store dimensions for display
            self.od = od
            self.id = id_mm
            self.wall_thickness_actual = wt
            
            # Calculate fluid properties
            self._calculate_fluid_properties()
            
            # Total mass = tube mass + fluid mass
            self.mass = self.tube_mass + self.fluid_mass
            
        else:  # Imperial units
            # Get dimensions in inches
            if self.tube_type == "Tube":
                od = TUBE_SIZES[self.size]["od_in"]
            else:
                od = PIPE_SIZES[self.size]["od_in"]
            
            wt = WALL_THICKNESS[self.wall_thickness]["in"]
            length_in = self.length * 12  # Convert ft to inches
            density_lbin3 = MATERIALS[self.material]["density_imperial"]  # lb/in³
            
            # Calculate internal diameter
            id_in = od - 2 * wt
            
            # Volume calculations in cubic inches (more direct for mass calculation)
            internal_volume_in3 = math.pi * (id_in/2)**2 * length_in  # in³
            material_volume_in3 = math.pi * ((od/2)**2 - (id_in/2)**2) * length_in  # in³
            
            # Tube mass calculation (in lbs) - direct calculation in cubic inches
            self.tube_mass = material_volume_in3 * density_lbin3
            
            # Convert volumes to standard units (ft³) for consistency
            self.internal_volume = internal_volume_in3 / 1728  # ft³
            self.material_volume = material_volume_in3 / 1728  # ft³
            
            # Store dimensions for display
            self.od = od
            self.id = id_in
            self.wall_thickness_actual = wt
            
            # Calculate fluid properties
            self._calculate_fluid_properties()
            
            # Total mass = tube mass + fluid mass
            self.mass = self.tube_mass + self.fluid_mass
    
    def _calculate_fluid_properties(self):
        """Calculate fluid mass and properties"""
        # Calculate fluid density
        fluid_props = calculate_fluid_density(
            self.fluid_name, 
            self.temperature, 
            self.pressure,
            self.temp_units,
            self.pressure_units
        )
        
        self.fluid_density_kg_m3 = fluid_props["density_kg_m3"]
        self.fluid_density_lb_ft3 = fluid_props["density_lb_ft3"]
        self.fluid_phase = fluid_props["phase"]
        self.fluid_error = fluid_props["error_msg"]
        
        # Calculate fluid mass
        if self.units == "metric":
            self.fluid_mass = self.fluid_density_kg_m3 * self.internal_volume  # kg
        else:
            self.fluid_mass = self.fluid_density_lb_ft3 * self.internal_volume  # lb

def get_display_values(segment, target_units):
    """Convert segment values for display in the target unit system"""
    if segment.units == target_units:
        # No conversion needed
        return {
            'length': segment.length,
            'od': segment.od,
            'id': segment.id,
            'wall_thickness_actual': segment.wall_thickness_actual,
            'mass': segment.mass,
            'tube_mass': segment.tube_mass,
            'fluid_mass': segment.fluid_mass,
            'internal_volume': segment.internal_volume,
            'material_volume': segment.material_volume
        }
    
    # Conversion needed
    if segment.units == "metric" and target_units == "imperial":
        # Convert from metric to imperial
        return {
            'length': segment.length * 3.28084,  # m to ft
            'od': segment.od / 25.4,  # mm to in
            'id': segment.id / 25.4,  # mm to in
            'wall_thickness_actual': segment.wall_thickness_actual / 25.4,  # mm to in
            'mass': segment.mass * 2.20462,  # kg to lb
            'tube_mass': segment.tube_mass * 2.20462,  # kg to lb
            'fluid_mass': segment.fluid_mass * 2.20462,  # kg to lb
            'internal_volume': segment.internal_volume * 35.3147,  # m³ to ft³
            'material_volume': segment.material_volume * 35.3147  # m³ to ft³
        }
    elif segment.units == "imperial" and target_units == "metric":
        # Convert from imperial to metric
        return {
            'length': segment.length / 3.28084,  # ft to m
            'od': segment.od * 25.4,  # in to mm
            'id': segment.id * 25.4,  # in to mm
            'wall_thickness_actual': segment.wall_thickness_actual * 25.4,  # in to mm
            'mass': segment.mass / 2.20462,  # lb to kg
            'tube_mass': segment.tube_mass / 2.20462,  # lb to kg
            'fluid_mass': segment.fluid_mass / 2.20462,  # lb to kg
            'internal_volume': segment.internal_volume / 35.3147,  # ft³ to m³
            'material_volume': segment.material_volume / 35.3147  # ft³ to m³
        }

def calculate_totals(segments, target_units=None):
    """Calculate total values for all segments in the target unit system"""
    if not segments:
        return {
            "total_length": 0,
            "total_internal_volume": 0,
            "total_mass": 0,
            "total_tube_mass": 0,
            "total_fluid_mass": 0,
            "total_material_volume": 0
        }
    
    total_length = 0
    total_internal_volume = 0
    total_mass = 0
    total_tube_mass = 0
    total_fluid_mass = 0
    total_material_volume = 0
    
    for seg in segments:
        if target_units:
            # Get converted values
            display_values = get_display_values(seg, target_units)
            total_length += display_values['length']
            total_internal_volume += display_values['internal_volume']
            total_mass += display_values['mass']
            total_tube_mass += display_values['tube_mass']
            total_fluid_mass += display_values['fluid_mass']
            total_material_volume += display_values['material_volume']
        else:
            # Use original values
            total_length += seg.length
            total_internal_volume += seg.internal_volume
            total_mass += seg.mass
            total_tube_mass += seg.tube_mass
            total_fluid_mass += seg.fluid_mass
            total_material_volume += seg.material_volume
    
    return {
        "total_length": total_length,
        "total_internal_volume": total_internal_volume,
        "total_mass": total_mass,
        "total_tube_mass": total_tube_mass,
        "total_fluid_mass": total_fluid_mass,
        "total_material_volume": total_material_volume
    }

def create_2d_visualization(segments, units):
    """Create 2D visualization of the tube system"""
    if not segments:
        return None
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("System Layout", "Diameter Distribution", "Mass Distribution (Tube + Fluid)", "Volume Distribution"),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
      # System Layout (Top Left)
    x_pos = 0
    
    # Improved color handling for many segments
    if len(segments) <= len(px.colors.qualitative.Set3):
        colors = px.colors.qualitative.Set3
    else:
        # Use a continuous colorscale for many segments
        colors = px.colors.sample_colorscale("viridis", [i/(len(segments)-1) for i in range(len(segments))])
    
    for i, segment in enumerate(segments):
        # Get converted values for display
        display_values = get_display_values(segment, units)
        
        if segment.is_continuous and i > 0:
            # Continuous segment - connects to previous
            x_start = x_pos
        else:
            # Separate segment - add gap
            x_pos += 1
            x_start = x_pos
        
        x_end = x_start + display_values['length']
        
        # Draw tube as rectangle
        color = colors[i % len(colors)]
        fig.add_trace(
            go.Scatter(
                x=[x_start, x_end, x_end, x_start, x_start],
                y=[-display_values['od']/2, -display_values['od']/2, display_values['od']/2, display_values['od']/2, -display_values['od']/2],
                fill="toself",
                fillcolor=color,
                line=dict(color="black", width=1),
                name=segment.name,
                showlegend=True,
                hovertemplate=f"<b>{segment.name}</b><br>" +
                             f"Length: {display_values['length']:.2f}<br>" +
                             f"OD: {display_values['od']:.2f}<br>" +
                             f"ID: {display_values['id']:.2f}<br>" +
                             "<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Draw internal diameter
        fig.add_trace(
            go.Scatter(
                x=[x_start, x_end, x_end, x_start, x_start],
                y=[-display_values['id']/2, -display_values['id']/2, display_values['id']/2, display_values['id']/2, -display_values['id']/2],
                fill="toself",
                fillcolor="white",
                line=dict(color="gray", width=0.5),
                showlegend=False,
                hoverinfo="skip"
            ),
            row=1, col=1
        )
        
        x_pos = x_end
      # Diameter Distribution (Top Right)
    segment_names = [seg.name for seg in segments]
    outer_diameters = [get_display_values(seg, units)['od'] for seg in segments]
    inner_diameters = [get_display_values(seg, units)['id'] for seg in segments]
    
    fig.add_trace(
        go.Bar(x=segment_names, y=outer_diameters, name="Outer Diameter", marker_color="lightblue"),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(x=segment_names, y=inner_diameters, name="Inner Diameter", marker_color="darkblue"),
        row=1, col=2
    )
    
    # Mass Distribution (Bottom Left) - Stacked bar showing tube and fluid mass
    tube_masses = [get_display_values(seg, units)['tube_mass'] for seg in segments]
    fluid_masses = [get_display_values(seg, units)['fluid_mass'] for seg in segments]
    
    fig.add_trace(
        go.Bar(x=segment_names, y=tube_masses, name="Tube Mass", marker_color="orange"),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(x=segment_names, y=fluid_masses, name="Fluid Mass", marker_color="lightcoral"),
        row=2, col=1
    )
    
    # Volume Distribution (Bottom Right)
    volumes = [get_display_values(seg, units)['internal_volume'] for seg in segments]
    fig.add_trace(
        go.Bar(x=segment_names, y=volumes, name="Internal Volume", marker_color="green"),
        row=2, col=2
    )
    
    # Update layout
    length_unit = "m" if units == "metric" else "ft"
    diameter_unit = "mm" if units == "metric" else "in"
    mass_unit = "kg" if units == "metric" else "lb"
    volume_unit = "m³" if units == "metric" else "ft³"
    
    fig.update_xaxes(title_text=f"Position ({length_unit})", row=1, col=1)
    fig.update_yaxes(title_text=f"Diameter ({diameter_unit})", row=1, col=1)
    fig.update_yaxes(title_text=f"Diameter ({diameter_unit})", row=1, col=2)
    fig.update_yaxes(title_text=f"Mass ({mass_unit})", row=2, col=1)
    fig.update_yaxes(title_text=f"Volume ({volume_unit})", row=2, col=2)
    
    fig.update_layout(
        height=800,
        title_text="Tube System Analysis",
        showlegend=True,
        legend=dict(x=1.05, y=1)
    )
    
    return fig

def export_to_excel(segments, totals, units):
    """Export results to Excel format"""
    # Create DataFrame for segments
    segment_data = []
    for seg in segments:
        length_unit = "m" if units == "metric" else "ft"
        diameter_unit = "mm" if units == "metric" else "in"
        mass_unit = "kg" if units == "metric" else "lb"
        volume_unit = "m³" if units == "metric" else "ft³"
        
        # Get values converted to the target unit system
        display_values = get_display_values(seg, units)
        
        segment_data.append({
            "Segment Name": seg.name,
            "Type": seg.tube_type,
            "Size": seg.size,
            "Wall Thickness": seg.wall_thickness,
            f"Length ({length_unit})": round(display_values['length'], 3),
            "Material": seg.material,
            f"Outer Diameter ({diameter_unit})": round(display_values['od'], 3),
            f"Inner Diameter ({diameter_unit})": round(display_values['id'], 3),
            f"Wall Thickness ({diameter_unit})": round(display_values['wall_thickness_actual'], 3),
            f"Internal Volume ({volume_unit})": round(display_values['internal_volume'], 6),
            f"Material Volume ({volume_unit})": round(display_values['material_volume'], 6),
            f"Tube Mass ({mass_unit})": round(display_values['tube_mass'], 3),
            "Fluid": seg.fluid_name,
            f"Temperature ({seg.temp_units})": seg.temperature,
            f"Pressure ({seg.pressure_units})": seg.pressure,
            "Fluid Phase": seg.fluid_phase,
            f"Fluid Mass ({mass_unit})": round(display_values['fluid_mass'], 3),
            f"Total Mass ({mass_unit})": round(display_values['mass'], 3),
            "Continuous": seg.is_continuous
        })
    
    df_segments = pd.DataFrame(segment_data)
    
    # Create DataFrame for totals
    length_unit = "m" if units == "metric" else "ft"
    mass_unit = "kg" if units == "metric" else "lb"
    volume_unit = "m³" if units == "metric" else "ft³"
    
    totals_data = {
        "Parameter": [
            f"Total Length ({length_unit})",
            f"Total Internal Volume ({volume_unit})",
            f"Total Material Volume ({volume_unit})",
            f"Total Tube Mass ({mass_unit})",
            f"Total Fluid Mass ({mass_unit})",
            f"Total System Mass ({mass_unit})"
        ],
        "Value": [
            round(totals["total_length"], 3),
            round(totals["total_internal_volume"], 6),
            round(totals["total_material_volume"], 6),
            round(totals["total_tube_mass"], 3),
            round(totals["total_fluid_mass"], 3),
            round(totals["total_mass"], 3)
        ]
    }
    
    df_totals = pd.DataFrame(totals_data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_segments.to_excel(writer, sheet_name='Segments', index=False)
        df_totals.to_excel(writer, sheet_name='Totals', index=False)
    
    return output.getvalue()

def calculate_fluid_density(fluid_name, temperature, pressure, temp_units="K", pressure_units="Pa"):
    """
    Calculate fluid density using CoolProp
    
    Args:
        fluid_name: Name of the fluid from FLUIDS database
        temperature: Temperature value
        pressure: Pressure value
        temp_units: Temperature units ("K" for Kelvin, "C" for Celsius, "F" for Fahrenheit)
        pressure_units: Pressure units ("Pa", "bar", "psi", "atm")
    
    Returns:
        dict: {density_kg_m3, density_lb_ft3, phase, error_msg}
    """
    if fluid_name == "None" or FLUIDS[fluid_name]["coolprop_name"] is None:
        return {
            "density_kg_m3": 0.0,
            "density_lb_ft3": 0.0,
            "phase": "None",
            "error_msg": None
        }
    
    try:
        coolprop_name = FLUIDS[fluid_name]["coolprop_name"]
        
        # Convert temperature to Kelvin
        if temp_units == "C":
            temp_K = temperature + 273.15
        elif temp_units == "F":
            temp_K = (temperature - 32) * 5/9 + 273.15
        else:  # Kelvin
            temp_K = temperature
        
        # Convert pressure to Pa
        if pressure_units == "bar":
            pressure_Pa = pressure * 100000
        elif pressure_units == "psi":
            pressure_Pa = pressure * 6894.76
        elif pressure_units == "atm":
            pressure_Pa = pressure * 101325
        else:  # Pa
            pressure_Pa = pressure
        
        # Check if inputs are reasonable
        if temp_K <= 0:
            return {"density_kg_m3": 0.0, "density_lb_ft3": 0.0, "phase": "Invalid", 
                   "error_msg": "Temperature must be above absolute zero"}
        
        if pressure_Pa <= 0:
            return {"density_kg_m3": 0.0, "density_lb_ft3": 0.0, "phase": "Invalid", 
                   "error_msg": "Pressure must be positive"}
        
        # Calculate density in kg/m³
        density_kg_m3 = PropsSI('D', 'T', temp_K, 'P', pressure_Pa, coolprop_name)
        
        # Convert to lb/ft³
        density_lb_ft3 = density_kg_m3 * 0.062428
        
        # Determine phase
        try:
            phase_index = PropsSI('Phase', 'T', temp_K, 'P', pressure_Pa, coolprop_name)
            if phase_index == 0:
                phase = "Liquid"
            elif phase_index == 1:
                phase = "Supercritical"
            elif phase_index == 2:
                phase = "Supercritical Gas"
            elif phase_index == 3:
                phase = "Supercritical Liquid"
            elif phase_index == 5:
                phase = "Gas"
            elif phase_index == 6:
                phase = "Two Phase"
            else:
                phase = f"Phase {phase_index}"
        except:
            phase = "Unknown"
        
        return {
            "density_kg_m3": density_kg_m3,
            "density_lb_ft3": density_lb_ft3,
            "phase": phase,
            "error_msg": None
        }
        
    except Exception as e:
        error_msg = f"CoolProp error: {str(e)}"
        if "outside the range of validity" in str(e):
            error_msg = "Temperature/pressure outside valid range for this fluid"
        elif "not a valid fluid name" in str(e):
            error_msg = f"'{fluid_name}' is not supported by CoolProp"
        
        return {
            "density_kg_m3": 0.0,
            "density_lb_ft3": 0.0,
            "phase": "Error",
            "error_msg": error_msg
        }

def get_default_conditions(fluid_name, units="metric"):
    """
    Get reasonable default temperature and pressure conditions for common fluids
    
    Args:
        fluid_name: Name of the fluid
        units: "metric" or "imperial"
    
    Returns:
        dict: {temperature, pressure, temp_units, pressure_units}
    """
    # Default conditions at standard conditions (20°C, 1 atm)
    defaults = {
        "None": {"temp_C": 20, "pressure_bar": 1.013},
        "Hydrogen": {"temp_C": -253, "pressure_bar": 1.013},  # Liquid hydrogen
        "Oxygen": {"temp_C": -183, "pressure_bar": 1.013},   # Liquid oxygen
        "Nitrogen": {"temp_C": 20, "pressure_bar": 1.013},   # Gaseous nitrogen
        "Helium": {"temp_C": 20, "pressure_bar": 1.013},     # Gaseous helium
        "Air": {"temp_C": 20, "pressure_bar": 1.013},        # Standard air
        "Water": {"temp_C": 20, "pressure_bar": 1.013},      # Liquid water
        "Methane": {"temp_C": -162, "pressure_bar": 1.013},  # Liquid methane
        "Propane": {"temp_C": 20, "pressure_bar": 1.013},    # Gaseous propane
        "Carbon Dioxide": {"temp_C": 20, "pressure_bar": 1.013},
        "Ammonia": {"temp_C": 20, "pressure_bar": 1.013},
        "Argon": {"temp_C": 20, "pressure_bar": 1.013},
        "Xenon": {"temp_C": 20, "pressure_bar": 1.013},
        "Krypton": {"temp_C": 20, "pressure_bar": 1.013},
        "Neon": {"temp_C": 20, "pressure_bar": 1.013}
    }
    
    fluid_defaults = defaults.get(fluid_name, defaults["Air"])
    
    if units == "metric":
        return {
            "temperature": fluid_defaults["temp_C"],
            "pressure": fluid_defaults["pressure_bar"],
            "temp_units": "C",
            "pressure_units": "bar"
        }
    else:  # imperial
        temp_F = fluid_defaults["temp_C"] * 9/5 + 32
        pressure_psi = fluid_defaults["pressure_bar"] * 14.5038
        return {
            "temperature": temp_F,
            "pressure": pressure_psi,
            "temp_units": "F",
            "pressure_units": "psi"
        }

def main():
    """Main Streamlit application"""
    
    # Initialize session state
    if 'segments' not in st.session_state:
        st.session_state.segments = []
    
    # Title and description
    st.title("🚀 Tube and Pipe Calculator")
    st.markdown("*Advanced tube system analysis for engineers*")
      # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Initialize unit tracking in session state
        if 'last_units' not in st.session_state:
            st.session_state.last_units = "metric"
        
        # Units selection
        units = st.radio(
            "Units System",
            ["metric", "imperial"],
            format_func=lambda x: "Metric (SI)" if x == "metric" else "Imperial (US)"
        )
        
        # Detect unit system change and warn user
        if units != st.session_state.last_units:
            st.warning("⚠️ **Unit system changed!** Please verify all input values in the form before adding segments.")
            st.session_state.last_units = units
        
        st.divider()
        
        # Fluid Properties Section
        st.header("🌊 Fluid Properties")
        st.info("Fluid properties apply to all new segments.")
        
        # Initialize fluid session state
        if 'global_fluid_name' not in st.session_state:
            st.session_state.global_fluid_name = "None"
        if 'global_temperature' not in st.session_state:
            st.session_state.global_temperature = 20.0
        if 'global_pressure' not in st.session_state:
            st.session_state.global_pressure = 1.013
        
        # Fluid selection
        fluid_options = list(FLUIDS.keys())
        fluid_name = st.selectbox(
            "Fluid Type",
            fluid_options,
            key="global_fluid_select",
            help="Select the fluid inside the tube/pipe"
        )
        st.session_state.global_fluid_name = fluid_name
        
        # Temperature and pressure inputs if fluid is not "None"
        if fluid_name != "None":
            st.caption(f"ℹ️ {FLUIDS[fluid_name]['description']}")
            
            # Get default conditions for the selected fluid
            defaults = get_default_conditions(fluid_name, units)
            
            # Temperature input
            temp_unit = "°C" if units == "metric" else "°F"
            temperature = st.number_input(
                f"Temperature ({temp_unit})",
                value=float(defaults["temperature"]),
                step=1.0,
                key="global_temperature_sidebar",
                help="Operating temperature of the fluid"
            )
            st.session_state.global_temperature = temperature
            
            # Pressure input
            pressure_unit = "bar" if units == "metric" else "psi"
            pressure = st.number_input(
                f"Pressure ({pressure_unit})",
                min_value=0.001,
                value=float(defaults["pressure"]),
                step=0.1,
                key="global_pressure_sidebar",
                help="Operating pressure of the fluid"
            )
            st.session_state.global_pressure = pressure
            
            # Calculate and display fluid properties preview
            temp_units_coolprop = "C" if units == "metric" else "F"
            pressure_units_coolprop = "bar" if units == "metric" else "psi"
            
            fluid_props = calculate_fluid_density(
                fluid_name, temperature, pressure, 
                temp_units_coolprop, pressure_units_coolprop
            )
            
            if fluid_props["error_msg"]:
                st.warning(f"⚠️ {fluid_props['error_msg']}")
            else:
                density_unit = "kg/m³" if units == "metric" else "lb/ft³"
                density_value = fluid_props["density_kg_m3"] if units == "metric" else fluid_props["density_lb_ft3"]
                st.caption(f"🧪 **Density:** {density_value:.3f} {density_unit}")
                st.caption(f"**Phase:** {fluid_props['phase']}")
        else:
            # Reset to default values for "None"
            st.session_state.global_temperature = 20.0 if units == "metric" else 68.0
            st.session_state.global_pressure = 1.013 if units == "metric" else 14.7
        
        st.divider()
        
        # Export section
        st.header("📊 Export Data")
        if st.session_state.segments:
            totals = calculate_totals(st.session_state.segments, units)
            
            excel_data = export_to_excel(st.session_state.segments, totals, units)
            st.download_button(
                label="📊 Download Excel Report",
                data=excel_data,
                file_name="tube_calculator_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )            # CSV export
            segment_data = []
            for seg in st.session_state.segments:
                # Get values converted to the target unit system
                display_values = get_display_values(seg, units)
                segment_data.append({
                    "Name": seg.name,
                    "Type": seg.tube_type,
                    "Size": seg.size,
                    "Wall_Thickness": seg.wall_thickness,
                    "Length": display_values['length'],
                    "Material": seg.material,
                    "OD": display_values['od'],
                    "ID": display_values['id'],
                    "Internal_Volume": display_values['internal_volume'],
                    "Tube_Mass": display_values['tube_mass'],
                    "Fluid": seg.fluid_name,
                    "Fluid_Phase": seg.fluid_phase,
                    "Fluid_Mass": display_values['fluid_mass'],
                    "Total_Mass": display_values['mass'],
                    "Continuous": seg.is_continuous
                })
            
            df_csv = pd.DataFrame(segment_data)
            csv_data = df_csv.to_csv(index=False)
            
            st.download_button(
                label="📄 Download CSV Data",
                data=csv_data,
                file_name="tube_calculator_data.csv",
                mime="text/csv"
            )
        else:
            st.info("Add segments to enable export")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("➕ Add Tube Segment")
          # Initialize session state for form values if not exists
        if 'form_tube_type' not in st.session_state:
            st.session_state.form_tube_type = "Tube"
        if 'form_tube_size' not in st.session_state:
            st.session_state.form_tube_size = "1/2\""
        if 'form_pipe_size' not in st.session_state:
            st.session_state.form_pipe_size = "1/2\" NPS"
        if 'form_wall_thickness' not in st.session_state:
            st.session_state.form_wall_thickness = "0.065\""
        if 'form_material' not in st.session_state:
            st.session_state.form_material = "Stainless Steel 316L"
        
        # Tube type selection OUTSIDE the form for immediate updates
        tube_type = st.selectbox(
            "Tube Type", 
            ["Tube", "Pipe"], 
            index=0 if st.session_state.form_tube_type == "Tube" else 1,
            key="tube_type_select"
        )
          # Update session state when tube type changes
        if tube_type != st.session_state.form_tube_type:
            st.session_state.form_tube_type = tube_type
            # Force a rerun to refresh the size options immediately
            st.rerun()
        
        with st.form("add_segment"):
            # Segment name
            segment_name = st.text_input("Segment Name", value=f"Segment {len(st.session_state.segments) + 1}")
            
            # Size selection with proper state management
            if tube_type == "Tube":
                size_options = list(TUBE_SIZES.keys())
                try:
                    current_index = size_options.index(st.session_state.form_tube_size)
                except ValueError:
                    current_index = size_options.index("1/2\"") if "1/2\"" in size_options else 0
                    st.session_state.form_tube_size = size_options[current_index]
                
                size = st.selectbox(
                    "Size", 
                    size_options, 
                    index=current_index, 
                    key="tube_size_select",
                    help="Standard tube sizes (OD)"
                )
                st.session_state.form_tube_size = size
                
                # Show selected tube size in both units
                od_in = TUBE_SIZES[size]['od_in']
                od_mm = TUBE_SIZES[size]['od_mm']
                st.caption(f"📐 OD: {od_in}\" ({od_mm} mm)")
                
            else:
                size_options = list(PIPE_SIZES.keys())
                try:
                    current_index = size_options.index(st.session_state.form_pipe_size)
                except ValueError:
                    current_index = size_options.index("1/2\" NPS") if "1/2\" NPS" in size_options else 0
                    st.session_state.form_pipe_size = size_options[current_index]
                
                size = st.selectbox(
                    "Size", 
                    size_options, 
                    index=current_index, 
                    key="pipe_size_select",
                    help="Nominal Pipe Size (NPS)"
                )
                st.session_state.form_pipe_size = size
                
                # Show selected pipe size in both units
                od_in = PIPE_SIZES[size]['od_in']
                od_mm = PIPE_SIZES[size]['od_mm']
                st.caption(f"📐 Actual OD: {od_in}\" ({od_mm} mm)")
            
            # Wall thickness
            wall_thickness_options = list(WALL_THICKNESS.keys())
            try:
                wt_index = wall_thickness_options.index(st.session_state.form_wall_thickness)
            except ValueError:
                wt_index = wall_thickness_options.index("0.065\"") if "0.065\"" in wall_thickness_options else 0
                st.session_state.form_wall_thickness = wall_thickness_options[wt_index]
            
            wall_thickness = st.selectbox(
                "Wall Thickness", 
                wall_thickness_options, 
                index=wt_index, 
                key="wall_thickness_select"
            )
            st.session_state.form_wall_thickness = wall_thickness
            
            # Show selected wall thickness in both units
            wt_in = WALL_THICKNESS[wall_thickness]['in']
            wt_mm = WALL_THICKNESS[wall_thickness]['mm']
            st.caption(f"📏 Selected: {wt_in}\" ({wt_mm} mm)")
            
            # Calculate and show resulting inner diameter as preview
            if tube_type == "Tube":
                od_preview = TUBE_SIZES[size]['od_in'] if units == 'imperial' else TUBE_SIZES[size]['od_mm']
            else:
                od_preview = PIPE_SIZES[size]['od_in'] if units == 'imperial' else PIPE_SIZES[size]['od_mm']
            
            wt_preview = WALL_THICKNESS[wall_thickness]['in'] if units == 'imperial' else WALL_THICKNESS[wall_thickness]['mm']
            id_preview = od_preview - 2 * wt_preview
            unit_label = "in" if units == 'imperial' else "mm"
            
            if id_preview > 0:
                st.caption(f"🔍 **Resulting ID:** {id_preview:.3f} {unit_label}")
            else:
                st.caption(f"⚠️ **Warning:** Wall too thick - would result in negative ID!")
            
            # Length
            length_unit = "meters" if units == "metric" else "feet"
            length = st.number_input(f"Length ({length_unit})", min_value=0.001, value=1.0, step=0.1, key="length_input")
            
            # Material
            material_options = list(MATERIALS.keys())
            try:
                material_index = material_options.index(st.session_state.form_material)
            except ValueError:
                material_index = material_options.index("Stainless Steel 316L") if "Stainless Steel 316L" in material_options else 0
                st.session_state.form_material = material_options[material_index]
            
            material = st.selectbox(
                "Material", 
                material_options, 
                index=material_index, 
                key="material_select"
            )
            st.session_state.form_material = material
              # Show selected material density in both units
            density_metric = MATERIALS[material]['density']
            density_imperial = MATERIALS[material]['density_imperial']
            st.caption(f"⚖️ Density: {density_metric} kg/m³ ({density_imperial:.3f} lb/in³)")
            
            # Display current fluid selection (controlled from sidebar)
            st.divider()
            st.write(f"**Selected Fluid:** {st.session_state.global_fluid_name}")
            if st.session_state.global_fluid_name != "None":
                temp_unit = "°C" if units == "metric" else "°F"
                pressure_unit = "bar" if units == "metric" else "psi"
                st.write(f"**Temperature:** {st.session_state.global_temperature:.1f} {temp_unit}")
                st.write(f"**Pressure:** {st.session_state.global_pressure:.2f} {pressure_unit}")
            
            # Continuous checkbox
            is_continuous = st.checkbox("Continuous with previous segment", value=True, key="continuous_checkbox")
              # Add segment button
            if st.form_submit_button("Add Segment", type="primary"):
                # Get the OD for the selected size for validation
                if tube_type == "Tube":
                    od_val = TUBE_SIZES[size]['od_in'] if units == 'imperial' else TUBE_SIZES[size]['od_mm']
                else:
                    od_val = PIPE_SIZES[size]['od_in'] if units == 'imperial' else PIPE_SIZES[size]['od_mm']
                
                # Get the wall thickness for validation
                wt_val = WALL_THICKNESS[wall_thickness]['in'] if units == 'imperial' else WALL_THICKNESS[wall_thickness]['mm']
                
                # Validation check
                if wt_val * 2 >= od_val:
                    unit_label = "in" if units == 'imperial' else "mm"
                    st.error(f"❌ **Invalid Geometry:** Total wall thickness ({wt_val*2:.3f} {unit_label}) cannot be greater than or equal to the Outer Diameter ({od_val:.3f} {unit_label}). Please select a smaller wall thickness.")
                else:
                    try:
                        # Create segment with error handling
                        temp_units_coolprop = "C" if units == "metric" else "F"
                        pressure_units_coolprop = "bar" if units == "metric" else "psi"
                        
                        new_segment = TubeSegment(
                            name=segment_name,
                            tube_type=tube_type,
                            size=size,
                            wall_thickness=wall_thickness,
                            length=length,
                            material=material,
                            units=units,
                            fluid_name=st.session_state.global_fluid_name,
                            temperature=st.session_state.global_temperature,
                            pressure=st.session_state.global_pressure,
                            temp_units=temp_units_coolprop,
                            pressure_units=pressure_units_coolprop
                        )
                        new_segment.is_continuous = is_continuous
                        st.session_state.segments.append(new_segment)
                        st.success(f"✅ Added segment: {segment_name} - {tube_type} {size} with {st.session_state.global_fluid_name}")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ **Failed to add segment.** Could not calculate fluid properties. Please check your temperature and pressure values.\n\nError details: {str(e)}")
    
    with col2:
        st.header("📋 Current Segments")
        
        if st.session_state.segments:
            for i, segment in enumerate(st.session_state.segments):
                with st.expander(f"{segment.name} ({segment.tube_type} - {segment.size})", expanded=False):
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        length_unit = "m" if units == "metric" else "ft"
                        diameter_unit = "mm" if units == "metric" else "in"
                        mass_unit = "kg" if units == "metric" else "lb"
                        volume_unit = "m³" if units == "metric" else "ft³"
                          # Get converted values for display
                        display_values = get_display_values(segment, units)
                        
                        st.write(f"**Length:** {round(display_values['length'], 2)} {length_unit}")
                        st.write(f"**OD:** {round(display_values['od'], 3)} {diameter_unit}")
                        st.write(f"**ID:** {round(display_values['id'], 3)} {diameter_unit}")
                        st.write(f"**Tube Mass:** {round(display_values['tube_mass'], 3)} {mass_unit}")
                        st.write(f"**Fluid:** {segment.fluid_name} ({segment.fluid_phase})")
                        if segment.fluid_name != "None":
                            st.write(f"**Fluid Mass:** {round(display_values['fluid_mass'], 3)} {mass_unit}")
                        st.write(f"**Total Mass:** {round(display_values['mass'], 3)} {mass_unit}")
                        st.write(f"**Volume:** {round(display_values['internal_volume'], 6)} {volume_unit}")
                        st.write(f"**Material:** {segment.material}")
                        st.write(f"**Continuous:** {'Yes' if segment.is_continuous else 'No'}")
                    
                    with col_b:
                        if st.button("🗑️", key=f"delete_{i}", help="Delete segment"):
                            st.session_state.segments.pop(i)
                            st.rerun()
        else:
            st.info("No segments added yet. Use the form on the left to add your first segment.")
    
    # Totals section
    if st.session_state.segments:
        st.divider()
        st.header("📊 System Totals")
        
        totals = calculate_totals(st.session_state.segments, units)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        length_unit = "m" if units == "metric" else "ft"
        mass_unit = "kg" if units == "metric" else "lb"
        volume_unit = "m³" if units == "metric" else "ft³"
        
        with col1:
            st.metric("Total Length", f"{totals['total_length']:.2f} {length_unit}")
        
        with col2:
            st.metric("Tube Mass", f"{totals['total_tube_mass']:.3f} {mass_unit}")
        
        with col3:
            st.metric("Fluid Mass", f"{totals['total_fluid_mass']:.3f} {mass_unit}")
        
        with col4:
            st.metric("Total Mass", f"{totals['total_mass']:.3f} {mass_unit}")
        
        with col5:
            st.metric("Internal Volume", f"{totals['total_internal_volume']:.6f} {volume_unit}")
    
    # Visualization section
    if st.session_state.segments:
        st.divider()
        st.header("📈 2D Visualization")
        
        # Visualization controls
        show_viz = st.checkbox("Show 2D Visualization", value=True)
        
        if show_viz:
            # Visualization controls
            col_viz1, col_viz2 = st.columns([1, 1])
            with col_viz1:
                aspect_ratio = st.slider("🎛️ Visual Aspect Ratio (Y/X)", 0.1, 5.0, 1.0, step=0.1, 
                                       help="Adjust the visual scaling of the system layout diagram")
            with col_viz2:
                st.write("")  # Spacer for future controls
            
            # Update continuity settings
            st.subheader("Segment Continuity Settings")
            cols = st.columns(min(len(st.session_state.segments), 4))
            
            for i, segment in enumerate(st.session_state.segments):
                with cols[i % 4]:
                    segment.is_continuous = st.checkbox(
                        f"{segment.name} continuous",
                        value=segment.is_continuous,
                        key=f"continuous_{i}",
                        disabled=(i == 0)  # First segment can't be continuous
                    )
            
            # Generate and display visualization
            fig = create_2d_visualization(st.session_state.segments, units)
            if fig:
                # Apply aspect ratio to the system layout plot
                fig.update_yaxes(scaleanchor="x", scaleratio=aspect_ratio, row=1, col=1)
                st.plotly_chart(fig, use_container_width=True)
    
    # Clear all button
    if st.session_state.segments:
        st.divider()
        if st.button("🗑️ Clear All Segments", type="secondary"):
            st.session_state.segments = []
            st.success("All segments cleared!")
            st.rerun()
    
    # Footer
    st.divider()
    st.markdown("*Built for simplicity and efficiency.")

if __name__ == "__main__":
    main()
