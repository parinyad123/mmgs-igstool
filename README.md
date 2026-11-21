# IGS Tool — Satellite Imagery Quality Control Automation

A Python pipeline that automates **quality control of satellite image products**. Each delivered
product archive is checked against **configurable QC criteria** read from its **DIMAP metadata
(XML)** and from the imagery itself (**OpenCV**). The product is then routed to
**Pass / NotPass / Error** with a JSON report.

Built at **GISTDA** (Geo-Informatics and Space Technology Development Agency, Thailand), 2021–2022.
Designed with the operators who had been doing these checks by hand. Published with my
supervisor's permission.

> ⚠️ **Legacy code (2021–2022).** Uploaded as a portfolio snapshot and not maintained.

---

## Results from the included test runs

Counted from [`QCTestResult.csv`](QCTestResult.csv):

| | |
|---|---|
| Products processed | **285** (THEOS-1, levels 1A and 2A) |
| Time per product | **4.9 s average** (2.7 s min, 12.2 s max) |
| Outcome | 150 Pass · 135 NotPass |
| Report | 25 fields per product: overall status, failed criteria, timing, and the measured value of every criterion |

---

## How it works

```
Sample Product/*.zip
        │  unzip
        ▼
METADATA.DIM (DIMAP XML)  +  IMAGERY.TIF (4 bands)
        │
        ├─ QC01 Lost scan lines        ← metadata
        ├─ QC02 Viewing incidence angle← metadata
        ├─ QC03 Product completeness   ← all required files present and readable
        ├─ QC04 No-data ratio per band ┐ imagery (OpenCV),
        ├─ QC07 Pixel mode range       ┘ one thread per band
        ├─ QC05 Cloud coverage         ← database (disabled by default)
        ├─ QC06 Calibration file date  ← calibration parameter file
        └─ QC08 Pointing error         ← placeholder, not implemented
        │
        ▼
 Pass / NotPass / Error
        ├─► archive moved to AfterQCprocess/{Pass,NotPass,Error}
        └─► one JSON report per product (+ CSV export)
```

Six of the eight criteria are active. Cloud coverage is switched off by default and pointing error
is not implemented.

## Design decisions

- **Config-driven.** Every threshold and every per-check on/off switch is loaded from a
  PostgreSQL configuration table, with defaults in code if the database is unreachable. Operators
  can retune acceptance criteria without changing code.
- **Fault isolation.** Each check returns a value or an `ERROR` / `SKIP` sentinel, so one failing
  criterion never aborts a batch. A product with an error goes to the Error folder, not NotPass.
- **Multithreaded band checks.** The two pixel-level checks run one thread per spectral band.
  Threads finish in any order, so each result carries its band index and results are sorted back
  before thresholds are applied.

---

## Tech stack

`Python` · `OpenCV` · `NumPy` · `pandas` · `threading` / `queue` · `xml.etree.ElementTree` ·
`PostgreSQL` · `psycopg2`

## Project structure

```
QCDM/
  mainQC.py               orchestrator: unzip → run checks → route → report
  Lost_Line.py            QC01
  Incidence_Angle.py      QC02
  ProductCompletionV02.py QC03
  Nodata_Mode.py          QC04 + QC07 (multithreaded)
  Cloud_valiation.py      QC05
  CPFdate.py              QC06
  Result_QC_json.py       JSON report
  QCResultToCSV.py        CSV export
  config/                 config loading from PostgreSQL
TestResult/               CSV results of 7 test runs
QCTestResult.csv          combined test results
```

## Running it

Create these folders next to `QCDM/` before the first run:

```
QCDM_directory/CPFdemo/   calibration parameter files
Sample Product/           product archives (.zip) to check
```

`AfterQCprocess/` and `QCResultJSON/` are created automatically.

```bash
pip install -r requirements.txt
cd QCDM
python mainQC.py
```

PostgreSQL settings go in `QCDM/config/database.ini` (not included). Without it, the built-in
default thresholds are used.

---

## Looking back

What I'd change today: replace bare `except:` blocks with specific exceptions and logging, delete
commented-out code, move the main loop behind `main()` so it can be tested, make file names
consistent, and add unit tests for the numeric checks (no-data ratio, pixel mode).
