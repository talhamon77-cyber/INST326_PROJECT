import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from data_manager import DataManager
from participants import StudentParticipant, AdultParticipant, SeniorParticipant


class TestDataManager(unittest.TestCase):
    def test_save_load_roundtrip(self):
        with TemporaryDirectory() as tmp:
            dm = DataManager(Path(tmp))

            original = [
                StudentParticipant("Ana", 20, "ana@terpmail.umd.edu", "UMD"),
                AdultParticipant("Ben", 35, "ben@email.com", "Teacher"),
                SeniorParticipant("Cora", 70, "cora@email.com", True),
            ]

            ok, msg = dm.save_participants_to_json(original, "participants.json")
            self.assertTrue(ok, msg)

            loaded, msg = dm.load_participants_from_json("participants.json")
            self.assertEqual(len(loaded), 3, msg)

            self.assertIsInstance(loaded[0], StudentParticipant)
            self.assertEqual(loaded[0].school, "UMD")

            self.assertIsInstance(loaded[1], AdultParticipant)
            self.assertEqual(loaded[1].occupation, "Teacher")

            self.assertIsInstance(loaded[2], SeniorParticipant)
            self.assertEqual(loaded[2].retirement_status, True)

    def test_load_missing_file(self):
        with TemporaryDirectory() as tmp:
            dm = DataManager(Path(tmp))
            loaded, msg = dm.load_participants_from_json("nope.json")
            self.assertEqual(loaded, [])
            self.assertIn("file not found", msg.lower())

    def test_import_missing_file(self):
        with TemporaryDirectory() as tmp:
            dm = DataManager(Path(tmp))
            imported, msg = dm.import_participants(Path(tmp) / "missing.json")
            self.assertEqual(imported, [])
            self.assertIn("file not found", msg.lower())

    def test_import_corrupted_json(self):
        with TemporaryDirectory() as tmp:
            dm = DataManager(Path(tmp))

            bad_path = Path(tmp) / "bad.json"
            bad_path.write_text("{ not valid json", encoding="utf-8")

            imported, msg = dm.import_participants(bad_path)
            self.assertEqual(imported, [])
            self.assertIn("corrupted json", msg.lower())

    def test_import_json_skips_invalid_records(self):
        with TemporaryDirectory() as tmp:
            dm = DataManager(Path(tmp))

            path = Path(tmp) / "mixed.json"
            payload = [
                {"type": "student", "name": "Ana", "age": 20, "email": "ana@terpmail.umd.edu", "school": "UMD"},
                {"type": "adult", "name": "Ben", "age": 35, "email": "ben@email.com", "occupation": "Teacher"},
                {"type": "adult", "name": "BadOne"},  # invalid, missing fields
                "not a dict",  # invalid
            ]
            path.write_text(json.dumps(payload), encoding="utf-8")

            imported, msg = dm.import_participants(path)
            self.assertEqual(len(imported), 2, msg)
            self.assertIn("invalid", msg.lower())

    def test_import_csv_success(self):
        with TemporaryDirectory() as tmp:
            dm = DataManager(Path(tmp))

            csv_path = Path(tmp) / "people.csv"
            csv_path.write_text(
                "type,name,age,email,school,occupation,retirement_status\n"
                "student,Ana,20,ana@terpmail.umd.edu,UMD,,\n"
                "adult,Ben,35,ben@email.com,,Teacher,\n"
                "senior,Cora,70,cora@email.com,,,true\n",
                encoding="utf-8"
            )

            imported, msg = dm.import_participants(csv_path)
            self.assertEqual(len(imported), 3, msg)
            self.assertIsInstance(imported[0], StudentParticipant)
            self.assertIsInstance(imported[1], AdultParticipant)
            self.assertIsInstance(imported[2], SeniorParticipant)

    def test_import_csv_skips_bad_rows(self):
        with TemporaryDirectory() as tmp:
            dm = DataManager(Path(tmp))

            csv_path = Path(tmp) / "bad_people.csv"
            csv_path.write_text(
                "type,name,age,email,school,occupation,retirement_status\n"
                "student,Ana,20,ana@terpmail.umd.edu,UMD,,\n"
                "adult,Ben,notanumber,ben@email.com,,Teacher,\n"
                "senior,Cora,70,cora@email.com,,,true\n",
                encoding="utf-8"
            )

            imported, msg = dm.import_participants(csv_path)
            self.assertEqual(len(imported), 2, msg)
            self.assertIn("invalid", msg.lower())

    def test_export_report_to_json(self):
        with TemporaryDirectory() as tmp:
            dm = DataManager(Path(tmp))

            report = {"top_product": "Widget", "average_satisfaction": 4.2}
            ok, msg = dm.export_report_to_json(report, "report.json")
            self.assertTrue(ok, msg)

            report_path = Path(tmp) / "report.json"
            self.assertTrue(report_path.exists())

            loaded = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["top_product"], "Widget")
            self.assertEqual(loaded["average_satisfaction"], 4.2)


if __name__ == "__main__":
    unittest.main()
