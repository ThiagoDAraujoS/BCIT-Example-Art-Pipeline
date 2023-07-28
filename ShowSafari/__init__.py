from datetime import date, time, datetime
import dataclasses_json.cfg

dataclasses_json.cfg.global_config.encoders[date] = date.isoformat
dataclasses_json.cfg.global_config.decoders[date] = date.fromisoformat

dataclasses_json.cfg.global_config.encoders[time] = time.isoformat
dataclasses_json.cfg.global_config.decoders[time] = time.fromisoformat

dataclasses_json.cfg.global_config.encoders[datetime] = datetime.isoformat
dataclasses_json.cfg.global_config.decoders[datetime] = datetime.fromisoformat
