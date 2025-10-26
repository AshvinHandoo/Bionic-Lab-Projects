# MATLAB Requirements

### MATLAB Environment
- MATLAB R2022b or newer (recommended)
- Signal Processing Toolbox
- Statistics and Machine Learning Toolbox

---

### 🔗 JIDT (Java Information Dynamics Toolkit)

The transfer entropy (TE) scripts in this repository rely on the **JIDT** Java library to perform information-theoretic calculations (Kraskov and kernel estimators).

#### 1. Download JIDT
JIDT is an open-source toolkit available on GitHub:

👉 [https://github.com/jlizier/jidt](https://github.com/jlizier/jidt)

Click **Code → Download ZIP**, or clone directly:
```bash
git clone https://github.com/jlizier/jidt.git
```

#### 2. Add JIDT to your MATLAB Path
Extract or clone the toolkit, then in MATLAB:
```matlab
addpath(genpath('path_to_jidt/infodynamics-dist'));
```

This makes the `infodynamics.jar` file accessible to MATLAB’s Java interface.

#### 3. Verify JIDT Installation
In MATLAB:
```matlab
javaaddpath('path_to_jidt/infodynamics-dist/infodynamics.jar');
```
You can test by creating a simple TE calculator:
```matlab
teCalc = javaObject('infodynamics.measures.continuous.kraskov.TransferEntropyCalculatorKraskov');
disp(teCalc);
```
If no error appears, JIDT is installed correctly.

---

### 🧪 Notes
- The synthetic demo (`runDemoPipeline.m`) **does not require JIDT** and runs out-of-the-box.  
- The original TE scripts (under `src/analysis/`) **require JIDT** to compute true transfer entropy values.

_Last updated: 2025-10-26_
