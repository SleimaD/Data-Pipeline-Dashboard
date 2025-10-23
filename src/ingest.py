from __future__ import annotations

import re
from datetime import datetime
from typing import List, Optional, Dict, Union, IO

import pandas as pd

#Read raw web server logs (Apache or Nginx) and turn them into a clean pandas DataFrame.

LOG_PATTERN = re.compile(
    r'^'
    r'(?P<ip>\S+)\s+'            # client IP
    r'(?P<ident>\S+)\s+'         # identd
    r'(?P<auth>\S+)\s+'          # authenticated user 
    r'\[(?P<timestamp>[^\]]+)\]\s+'  # date/time
    r'"(?P<method>[A-Za-z]+)\s+'    # HTTP method
    r'(?P<path>[^\s"]+)\s+'      # path
    r'(?P<protocol>[^\"]+)"\s+' # protocol
    r'(?P<status>\d{3}|000)\s+'      # HTTP status code
    r'(?P<size>\S+)'              # response size in bytes or '-'
    r'(?:\s+"(?P<referrer>[^"]*)"\s+"(?P<user_agent>[^"]*)")?'  
)


def parse_log_line(line: str) -> Optional[Dict[str, Union[str, int, None, datetime]]]:
    #Parse raw log line. Return a dict with typed fields or None if the line doesn't match.

    line = line.strip('\n')
    if not line:
        return None
    
    match = LOG_PATTERN.match(line)

    if not match:
        return None
    data = match.groupdict()

    # Type conversions / normalization
    ts_str = data.pop('timestamp')
    
    try:
        data['timestamp'] = datetime.strptime(ts_str, "%d/%b/%Y:%H:%M:%S %z")
    except Exception:
        # on failure we store None instead of crashing.
        data['timestamp'] = None
    
    # HTTP status. int or None (if malformed)
    try:
        data['status'] = int(data['status'])
    except ValueError:
        data['status'] = None

    # Response size. int or None 
    size_val = data.get('size')

    if size_val is None or size_val == '-' or size_val == '':
        data['size'] = None
    else:
        try:
            data['size'] = int(size_val)
        except ValueError:
            data['size'] = None
    return data


def parse_log_file(file_like: Union[str, IO[bytes], IO[str]]) -> pd.DataFrame:
    #Read a file path or a file-like object and build a DataFrame from valid lines.


    records: List[Dict[str, Union[str, int, None, datetime]]] = []

    # Accept both a file-like object (uploads) and a local path
    if hasattr(file_like, 'read'):
       
        for raw_line in file_like:
            if isinstance(raw_line, bytes):
                try:
                    line = raw_line.decode('utf-8', errors='ignore')
                except Exception:
                    line = raw_line.decode('latin-1', errors='ignore')
            else:
                line = raw_line

            entry = parse_log_line(line)
            if entry:
                records.append(entry)
    else:
        # Local file path
        with open(file_like, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                entry = parse_log_line(line)
                if entry:
                    records.append(entry)

    # Build the DataFrame from parsed records
    df = pd.DataFrame.from_records(records)
    return df
