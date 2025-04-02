# FHIR Data Transformation POC

A proof-of-concept project demonstrating the conversion between CSV data and FHIR (Fast Healthcare Interoperability Resources) format. This tool provides bidirectional transformation capabilities, allowing you to convert healthcare data between CSV and FHIR formats.

## Features

- CSV to FHIR conversion
- FHIR to CSV conversion
- FHIR resource validation
- Support for Patient and Observation resources
- Bundle creation and management
- Command-line interface for easy use

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd fhir-transform-poc
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### CSV to FHIR Conversion

Convert patient data:
```bash
python src/main.py to-fhir --patients data/sample_patient.csv --output output/patients.json
```

Convert observation data:
```bash
python src/main.py to-fhir --observations data/sample_observations.csv --output output/observations.json
```

Convert both patient and observation data:
```bash
python src/main.py to-fhir --patients data/sample_patient.csv --observations data/sample_observations.csv --output output/bundle.json
```

### FHIR Resource Validation

Validate FHIR resources:
```bash
python src/main.py validate output/patients.json --type Patient
python src/main.py validate output/observations.json --type Observation
python src/main.py validate output/bundle.json --type Bundle
```

### FHIR to CSV Conversion

Convert FHIR Bundle back to CSV:
```bash
python src/main.py to-csv output/bundle.json --output-dir output
```

## Data Format

### Patient CSV Format
```csv
id,family_name,given_name,gender,birth_date,address,city,country,phone
P001,Wang,Li,male,1985-05-15,123 Main St,Beijing,China,+86-10-12345678
```

### Observation CSV Format
```csv
id,patient_id,observation_date,code,code_system,display,value,unit
O001,P001,2023-01-15,8480-6,http://loinc.org,Systolic blood pressure,120,mmHg
```

## Project Structure

```
fhir-transform-poc/
├── src/
│   ├── main.py              # Main entry point
│   ├── fhir_transformer.py  # CSV to FHIR conversion
│   ├── reverse_transformer.py # FHIR to CSV conversion
│   └── validator.py         # FHIR resource validation
├── data/
│   ├── sample_patient.csv   # Sample patient data
│   └── sample_observations.csv # Sample observation data
├── output/                  # Output directory for generated files
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## Dependencies

- fhir.resources==8.0.0
- pandas==2.2.3
- pydantic==2.11.1
- python-dateutil==2.9.0.post0
- And other dependencies listed in requirements.txt

## Error Handling

The tool includes basic error handling for:
- Invalid CSV formats
- Missing required fields
- Invalid FHIR resource structures
- Date format issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here]

## Contact

[Your Contact Information]
