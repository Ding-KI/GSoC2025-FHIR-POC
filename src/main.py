import argparse
import os
from fhir_transformer import csv_to_fhir_patients, csv_to_fhir_observations, create_bundle, save_resources_to_json, save_bundle_to_json
from validator import validate_fhir_resources
from reverse_transformer import patients_to_csv, observations_to_csv, extract_patients_from_bundle, extract_observations_from_bundle

def parse_args():
    parser = argparse.ArgumentParser(description="FHIR data conversion tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # 转换为FHIR命令
    to_fhir_parser = subparsers.add_parser("to-fhir", help="Convert CSV to FHIR")
    to_fhir_parser.add_argument("--patients", help="Patient CSV file path")
    to_fhir_parser.add_argument("--observations", help="Observation CSV file path")
    to_fhir_parser.add_argument("--output", required=True, help="Output JSON file path")
    
    # 验证命令
    validate_parser = subparsers.add_parser("validate", help="Validate FHIR resources")
    validate_parser.add_argument("file", help="FHIR JSON file to validate")
    validate_parser.add_argument("--type", choices=["Patient", "Observation", "Bundle"], required=True, help="Resource type")
    
    # 转换回CSV命令
    to_csv_parser = subparsers.add_parser("to-csv", help="Convert FHIR to CSV")
    to_csv_parser.add_argument("bundle", help="FHIR Bundle JSON file")
    to_csv_parser.add_argument("--output-dir", default=".", help="Output directory")
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.command == "to-fhir":
        patients = []
        observations = []
        
        if args.patients:
            patients = csv_to_fhir_patients(args.patients)
            print(f"Converted {len(patients)} patient records")
        
        if args.observations:
            observations = csv_to_fhir_observations(args.observations)
            print(f"Converted {len(observations)} observation records")
        
        bundle = create_bundle(patients, observations)
        save_bundle_to_json(bundle, args.output)
        print(f"Created a Bundle with {len(bundle.entry)} entries and saved to {args.output}")
    
    elif args.command == "validate":
        result = validate_fhir_resources(args.file, args.type)
        print(f"Validation results:")
        print(f"- Valid resources: {result['valid_count']}")
        print(f"- Error resources: {result['error_count']}")
        if result['error_count'] > 0:
            for msg in result['error_messages']:
                print(f"  * {msg}")
    
    elif args.command == "to-csv":
        patients = extract_patients_from_bundle(args.bundle)
        observations = extract_observations_from_bundle(args.bundle)
        
        patients_file = os.path.join(args.output_dir, "patients_output.csv")
        observations_file = os.path.join(args.output_dir, "observations_output.csv")
        
        patient_count = patients_to_csv(patients, patients_file)
        obs_count = observations_to_csv(observations, observations_file)
        
        print(f"Converted {patient_count} patient records to {patients_file}")
        print(f"Converted {obs_count} observation records to {observations_file}")

if __name__ == "__main__":
    main()