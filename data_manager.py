from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple, Optional

from participants import Participant, StudentParticipant, AdultParticipant, SeniorParticipant


class DataManager:
    """
    Persistence and file exchange for Participants and Analysis Reports.

    Participants are stored as JSON list of dicts with a "type" field so we can rebuild subclasses.
    Reports are exported as JSON dicts.
    """

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, filename: str) -> Path:
        return self.data_dir / filename

    def _participant_to_dict(self, p: Participant) -> Dict[str, Any]:
        base = {
            "name": p.name,
            "age": p.age,
            "email": p.email,
        }

        if isinstance(p, StudentParticipant):
            base["type"] = "student"
            base["school"] = p.school
            return base

        if isinstance(p, AdultParticipant):
            base["type"] = "adult"
            base["occupation"] = p.occupation
            return base

        if isinstance(p, SeniorParticipant):
            base["type"] = "senior"
            base["retirement_status"] = p.retirement_status
            return base

        raise ValueError("Unsupported participant type")

    def _participant_from_dict(self, d: Dict[str, Any]) -> Participant:
        required = {"type", "name", "age", "email"}
        if not required.issubset(d.keys()):
            raise ValueError(f"Missing required participant fields: {d}")

        p_type = str(d["type"]).strip().lower()
        name = str(d["name"])
        age = int(d["age"])
        email = str(d["email"])

        if p_type == "student":
            school = str(d.get("school", ""))
            return StudentParticipant(name, age, email, school)

        if p_type == "adult":
            occupation = str(d.get("occupation", ""))
            return AdultParticipant(name, age, email, occupation)

        if p_type == "senior":
            retirement_status = d.get("retirement_status", False)
            retirement_status_bool = bool(retirement_status)
            return SeniorParticipant(name, age, email, retirement_status_bool)

        raise ValueError(f"Unknown participant type: {p_type}")

    def save_participants_to_json(
        self,
        participants: Sequence[Participant],
        filename: str = "participants.json",
    ) -> Tuple[bool, str]:
        path = self._path(filename)
        try:
            payload = [self._participant_to_dict(p) for p in participants]
            with path.open("w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            return True, f"Saved {len(payload)} participants to {path}"
        except (OSError, TypeError, ValueError) as e:
            return False, f"Save failed: {e}"

    def load_participants_from_json(
        self,
        filename: str = "participants.json",
    ) -> Tuple[List[Participant], str]:
        path = self._path(filename)
        if not path.exists():
            return [], f"Load skipped: file not found at {path}"

        try:
            with path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except json.JSONDecodeError as e:
            return [], f"Load failed: corrupted JSON: {e}"
        except OSError as e:
            return [], f"Load failed: {e}"

        if not isinstance(raw, list):
            return [], "Load failed: expected a JSON list"

        participants: List[Participant] = []
        bad = 0

        for item in raw:
            if not isinstance(item, dict):
                bad += 1
                continue
            try:
                participants.append(self._participant_from_dict(item))
            except Exception:
                bad += 1

        msg = f"Loaded {len(participants)} participants from {path}"
        if bad:
            msg += f" with {bad} invalid record(s) skipped"
        return participants, msg

    def import_participants(self, source_path: Path) -> Tuple[List[Participant], str]:
        source_path = Path(source_path)
        if not source_path.exists():
            return [], f"Import failed: file not found at {source_path}"

        suffix = source_path.suffix.lower()
        if suffix == ".json":
            return self._import_participants_from_json(source_path)
        if suffix == ".csv":
            return self._import_participants_from_csv(source_path)

        return [], f"Import failed: unsupported file type {suffix}"

    def _import_participants_from_json(self, source_path: Path) -> Tuple[List[Participant], str]:
        try:
            with source_path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except json.JSONDecodeError as e:
            return [], f"Import failed: corrupted JSON: {e}"
        except OSError as e:
            return [], f"Import failed: {e}"

        if not isinstance(raw, list):
            return [], "Import failed: expected a JSON list"

        participants: List[Participant] = []
        bad = 0
        for item in raw:
            if not isinstance(item, dict):
                bad += 1
                continue
            try:
                participants.append(self._participant_from_dict(item))
            except Exception:
                bad += 1

        msg = f"Imported {len(participants)} participants from {source_path}"
        if bad:
            msg += f" with {bad} invalid record(s) skipped"
        return participants, msg

    def _import_participants_from_csv(self, source_path: Path) -> Tuple[List[Participant], str]:
        """
        CSV expected columns:
        type,name,age,email,school,occupation,retirement_status

        Only some columns apply based on type.
        """
        participants: List[Participant] = []
        bad = 0

        try:
            with source_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    return [], "Import failed: CSV missing header row"

                for row in reader:
                    try:
                        d = {
                            "type": str(row.get("type", "")).strip().lower(),
                            "name": str(row.get("name", "")).strip(),
                            "age": int(row.get("age", 0)),
                            "email": str(row.get("email", "")).strip(),
                            "school": str(row.get("school", "")).strip(),
                            "occupation": str(row.get("occupation", "")).strip(),
                            "retirement_status": str(row.get("retirement_status", "")).strip().lower() in {"true", "1", "yes"},
                        }
                        participants.append(self._participant_from_dict(d))
                    except Exception:
                        bad += 1
        except OSError as e:
            return [], f"Import failed: {e}"

        msg = f"Imported {len(participants)} participants from {source_path}"
        if bad:
            msg += f" with {bad} invalid row(s) skipped"
        return participants, msg

    def export_report_to_json(
        self,
        report: Dict[str, Any],
        filename: str = "analysis_report.json",
    ) -> Tuple[bool, str]:
        path = self._path(filename)
        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return True, f"Exported report to {path}"
        except (OSError, TypeError) as e:
            return False, f"Export failed: {e}"
