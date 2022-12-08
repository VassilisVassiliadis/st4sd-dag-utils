# Utility scripts to handle ST4SD DAGs

Collection of miscellaneous utilities to handle Directed Acyclic Graphs (DAGs) that use the [Simulation Toolkit For Scientific Discovery](https://github.com/st4sd/).

## Quick start


### Setup your development environment

1. Install python 3.8+
2. Create a virtual environment (e.g. `python3 -m venv --copies my_env`)
3. Activate your virtual environment (e.g. `source my_env/bin/activate`)
4. Install requirements with `pip install -r requirements.txt`

### Get test data

1. Run `git submodule init`
2. Run `git submodule update`
3. You should now be able to see the contents of the directory `band-gap-gamess` (e.g. `ls -lth band-gap-gamess`)

### Run on test data

```commandline
python3 scripts/dag-extract.py \
    --manifest band-gap-gamess/dft/manifest.yaml \
    band-gap-gamess/dft/homo-lumo-dft.yaml 
```

The output should look similar to this:

```json
{
  "stage0.SetFunctional": [
    "stage0.SetBasis"
  ],
  "stage0.SMILESToGAMESSInput": [
    "stage0.SetFunctional",
    "stage0.GetMoleculeIndex"
  ],
  "stage1.AnalyzeEnergies": [
    "stage1.GeometryOptimisation"
  ],
  "stage1.ExtractEnergies": [
    "stage1.GeometryOptimisation",
    "stage1.CreateLabels"
  ],
  "stage1.GeometryOptimisation": [
    "stage0.SMILESToGAMESSInput"
  ],
  "stage0.GetMoleculeIndex": [],
  "stage1.CreateLabels": [
    "stage0.GetMoleculeIndex"
  ],
  "stage0.SetBasis": []
}
```