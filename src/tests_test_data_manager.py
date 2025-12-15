import tempfile
import csv
import json
from pathlib import Path
from anon_participant_data import StudentParticipant, AdultParticipant, SeniorParticipant, anonymize_participant_data
from data_manager import DataManager

def test_import_json_csv_anonymize_and_save():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        dm = DataManager(tmpdir)
        
        # 1. Create test JSON file
        json_data = [
            {"type": "student", "name": "Danieshia", "age": 20, "email": "dmaragh1@terpmail.umd.edu", "school": "University of Maryland"},
            {"type": "adult", "name": "Ash", "age": 35, "email": "ashley123@email.com", "occupation": "Teacher"}
        ]
        json_file = tmpdir / "test_input.json"
        with json_file.open("w") as f:
            json.dump(json_data, f)
        
        # 2. Import from JSON
        json_participants, msg = dm.import_participants(json_file)
        print(f"JSON Import: {msg}")
        assert len(json_participants) == 2
        assert json_participants[0].name == "Danieshia"
        assert json_participants[1].occupation == "Teacher"
        
        # 3. Create test CSV file
        csv_file = tmpdir / "test_input.csv"
        with csv_file.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["type", "name", "age", "email", "school", "occupation", "retirement_status"])
            writer.writeheader()
            writer.writerow({"type": "senior", "name": "Katie", "age": 70, "email": "katie@email.com", "retirement_status": "true", "school": "", "occupation": ""})
            writer.writerow({"type": "student", "name": "John", "age": 22, "email": "john@college.edu", "school": "MIT", "occupation": "", "retirement_status": ""})
        
        # 4. Import from CSV
        csv_participants, msg = dm.import_participants(csv_file)
        print(f"CSV Import: {msg}")
        assert len(csv_participants) == 2
        assert csv_participants[0].name == "Katie"
        assert csv_participants[0].retirement_status == True
        assert csv_participants[1].school == "MIT"
        
        # 5. Combine all participants
        all_participants = json_participants + csv_participants
        
        # 6. Load and verify combined data
        print(f"\nAll participants ({len(all_participants)}):")
        for p in all_participants:
            print(f"  {p.get_info()}")
        
        # 7. Anonymize the data
        anonymized = anonymize_participant_data(all_participants)
        print(f"\nAnonymized data:")
        for anon in anonymized:
            print(f"  {anon}")
        
        # 8. Save original participants to JSON
        success, msg = dm.save_participants_to_json(all_participants, "all_participants.json")
        assert success
        print(f"\n{msg}")
        
        # 9. Save anonymized data to JSON
        success, msg = dm.export_report_to_json(
            {"anonymized_participants": anonymized},
            "anonymized_report.json"
        )
        assert success
        print(f"{msg}")
        
        # 10. Verify files exist
        assert (tmpdir / "all_participants.json").exists()
        assert (tmpdir / "anonymized_report.json").exists()
        
        # 11. Load back and verify
        loaded, msg = dm.load_participants_from_json("all_participants.json")
        assert len(loaded) == 4
        print(f"\n{msg}")

if __name__ == "__main__":
    test_import_json_csv_anonymize_and_save()
