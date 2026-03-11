# Archived Files

This directory contains archived documentation and status files from the ASD Detection System project.

## Contents

### legacy_docs/
Contains older documentation files that have been superseded by newer, consolidated documentation.

Original location: `docs/`

Files include:
- Database setup guides
- Deployment guides  
- Validation documentation
- Feature implementation notes

These files are kept for historical reference but are no longer actively maintained.

### status_files/
Contains temporary status files that were used during development.

Files include:
- DATABASE_CLEARED.txt
- DEPLOYMENT_READINESS.txt
- PROJECT_STATUS.txt
- QUICK_TEST.txt
- SCREENING_COMPLETE.md
- VALIDATION_FIXES.txt
- VALIDATION_IMPLEMENTATION.txt

These files have been superseded by:
- FINAL_STATUS.md
- INTEGRATION_COMPLETE.md
- ML_MODEL_GUIDE.md
- DATABASE_LOCK_FIX.md

## Restoration

If you need to restore any of these files:

```bash
# Restore specific file
cp archive/legacy_docs/FILENAME.md ./

# Restore all legacy docs
cp -r archive/legacy_docs docs/
```

---

**Archived**: March 11, 2026
**Reason**: Project cleanup and organization
