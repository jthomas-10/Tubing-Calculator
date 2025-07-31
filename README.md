# Space Vehicle Tube Calculator 🚀

A comprehensive Python application for calculating mass, volume, and total length of tubing systems for space vehicle engineering applications.

## Features

### Core Functionality
- **Tube & Pipe Calculations**: Support for standard tube and pipe sizes
- **Multi-segment Systems**: Add multiple tube segments with different properties
- **Unit Conversion**: Switch between metric (SI) and imperial units
- **Material Database**: Includes common aerospace materials (SS316L, Al6061-T6, Ti-6Al-4V, Inconel 625, Copper)
- **Export Capabilities**: Download results as Excel or CSV files

### Advanced Features
- **2D Visualization**: Professional-grade plots showing system layout, diameter distribution, mass distribution, and volume distribution
- **Continuous/Separate Segments**: Define whether segments connect or are separate
- **Real-time Calculations**: Instant updates as you modify parameters
- **Professional UI**: Modern, sleek interface built with Streamlit

### Calculations
The app automatically calculates:
- **Internal Volume**: Fluid volume capacity
- **Material Volume**: Volume of tube/pipe material
- **Mass**: Total mass based on material density
- **Total Length**: Sum of all segments
- **Outer/Inner Diameters**: Based on standard sizes and wall thickness

## Installation

1. **Install Python Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run tube_calculator.py
   ```

3. **Open in Browser**:
   The app will automatically open in your default browser at `http://localhost:8501`

## Usage

### Adding Segments
1. Enter a segment name
2. Select tube type (Tube or Pipe)
3. Choose standard size from dropdown
4. Select wall thickness
5. Enter length in meters (metric) or feet (imperial)
6. Choose material from the database
7. Set continuity with previous segment
8. Click "Add Segment"

### Visualization
- Enable "Show 2D Visualization" to see your tube system
- Adjust continuity settings for each segment
- View system layout, diameter distribution, mass distribution, and volume distribution

### Export Data
- **Excel**: Comprehensive report with segments and totals in separate sheets
- **CSV**: Raw data for further analysis

## Technical Specifications

### Supported Tube Sizes
- **Tubes**: 1/8" to 4" standard tube sizes (26 sizes total)
- **Pipes**: 1/8" NPS to 4" NPS pipe sizes (13 sizes total)

### Wall Thickness Options
- 0.028" to 0.500" (0.71mm to 12.70mm) - 22 standard thicknesses

### Materials Database
- **Stainless Steels**: 316L, 321, 347, 15-7 PH
- **Aluminum Alloys**: 6061-T6, 2024-T3, 7075-T6
- **Titanium Alloys**: Ti-6Al-4V, Grade 2, Ti-3Al-2.5V
- **Nickel Superalloys**: Inconel 625/718/X-750, Hastelloy C-276/X, Nimonic 90, Waspaloy
- **Copper Alloys**: Monel 400/K-500, Copper C101/C110, Brass 360
- **Specialty**: Nickel 200
- **Total**: 23 aerospace-grade materials with accurate density values

### Units
- **Metric**: meters, millimeters, kg, m³
- **Imperial**: feet, inches, pounds, ft³

## File Structure
```
Tube Calculator/
├── tube_calculator.py    # Main application
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Calculations Reference

### Volume Calculations
- **Internal Volume**: π × (ID/2)² × Length
- **Material Volume**: π × ((OD/2)² - (ID/2)²) × Length

### Mass Calculations
- **Mass**: Material Volume × Material Density

### Diameter Calculations
- **Inner Diameter**: Outer Diameter - 2 × Wall Thickness

## Professional Features

### Visualization Quality
- Multi-panel layout showing different aspects of the system
- Interactive plots with hover information
- Professional color schemes and styling
- Comparable to industry tools like AFT Arrow

### Data Export
- Excel format with multiple sheets
- CSV format for data analysis
- Comprehensive parameter documentation
- Unit labels and precision formatting

### User Experience
- Intuitive interface design
- Real-time feedback
- Error prevention
- Professional aerospace styling

## Development Notes

This application was developed specifically for space vehicle engineering applications where:
- Accuracy is critical for flight systems
- Professional documentation is required
- Multiple unit systems must be supported
- Visual representation aids in system understanding
- Export capabilities are essential for reporting

The tool follows aerospace industry standards for tube and pipe sizing and includes materials commonly used in space applications.

## Future Enhancements

Potential improvements could include:
- Pressure drop calculations
- Thermal analysis
- Custom material database
- 3D visualization
- Integration with CAD systems
- Flow rate calculations
- Stress analysis integration
