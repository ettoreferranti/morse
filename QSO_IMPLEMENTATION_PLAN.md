# QSO Feature Implementation Plan

## Project Overview

Implementation of realistic amateur radio QSO (contact) practice mode for the Morse Code learning application. This feature allows users to practice listening comprehension by transcribing elements from simulated CW QSO exchanges.

## GitHub Issues Created

All work items have been created as GitHub issues and can be tracked at:
https://github.com/ettoreferranti/morse/issues

### Issue List

| # | Issue | Priority | Complexity | Phase |
|---|-------|----------|------------|-------|
| #2 | QSO Data Module Foundation | High | Medium | Phase 1 |
| #3 | Call Sign Generator | High | Medium-High | Phase 1 |
| #4 | QSO Template System | High | Medium | Phase 1 |
| #5 | QSO Generator Integration | High | Medium | Phase 1 |
| #6 | Practice Session Manager | High | Medium-High | Phase 2 |
| #7 | Scoring System | High | Medium | Phase 2 |
| #8 | GUI Practice Tab | High | High | Phase 3 |
| #9 | Abbreviation Glossary | Medium | Low-Medium | Phase 3 |
| #10 | Audio Controls & Workflow | High | Medium | Phase 3 |
| #11 | Configuration Extension | Medium | Low-Medium | Phase 4 |
| #12 | Documentation Updates | Medium | Low | Phase 4 |

## Implementation Phases

### Phase 1: Data Generation (Backend) - Issues #2-5
**Goal:** Create the backend data generation system

**Duration Estimate:** 3-5 development sessions

**Work Items:**
1. **Issue #2: QSO Data Module Foundation**
   - Start here - foundational data structures
   - No dependencies
   - Creates: `qso_data.py` with all reference data
   - Deliverable: Importable module with data lists and abbreviations

2. **Issue #3: Call Sign Generator**
   - Depends on: #2
   - Creates: `CallSignGenerator` class
   - Deliverable: Function that generates valid call signs for all supported regions

3. **Issue #4: QSO Template System**
   - Depends on: #2
   - Creates: `QSOTemplate` class
   - Deliverable: Templates for minimal/medium/chatty QSOs with variable substitution

4. **Issue #5: QSO Generator Integration**
   - Depends on: #2, #3, #4
   - Creates: Orchestration logic
   - Deliverable: Complete QSO generation pipeline producing Morse-ready text

**Phase 1 Success Criteria:**
- ✅ Can generate randomized QSO exchange text
- ✅ Call signs are realistic for all regions
- ✅ Templates produce varied but authentic exchanges
- ✅ Output is compatible with existing MorseCode class

---

### Phase 2: Practice Logic (Backend) - Issues #6-7
**Goal:** Implement session management and scoring

**Duration Estimate:** 2-3 development sessions

**Work Items:**
1. **Issue #6: Practice Session Manager**
   - Depends on: #5, existing MorseCode class
   - Creates: `qso_practice.py` with `QSOPracticeSession` class
   - Deliverable: Session manager that can run multi-QSO practice sessions

2. **Issue #7: Scoring System**
   - Depends on: #6
   - Creates: Scoring logic in `qso_practice.py`
   - Deliverable: Validation and scoring with fuzzy matching

**Phase 2 Success Criteria:**
- ✅ Can run a complete practice session programmatically
- ✅ Audio plays correctly using existing MorseCode class
- ✅ Scoring accurately validates user input
- ✅ Fuzzy matching provides appropriate partial credit
- ✅ Session statistics are tracked and reported

---

### Phase 3: GUI Integration (Frontend) - Issues #8-10
**Goal:** Create user interface and interaction

**Duration Estimate:** 4-6 development sessions

**Work Items:**
1. **Issue #8: GUI Practice Tab**
   - Depends on: #6, #7
   - Modifies: `morse_gui.py`
   - Deliverable: New tab with complete QSO practice interface

2. **Issue #9: Abbreviation Glossary**
   - Depends on: #2, #8
   - Modifies: `morse_gui.py`
   - Deliverable: Searchable glossary dialog and quick reference

3. **Issue #10: Audio Controls & Workflow**
   - Depends on: #8
   - Modifies: `morse_gui.py`
   - Deliverable: Complete user interaction flow

**Phase 3 Success Criteria:**
- ✅ New QSO tab appears in GUI
- ✅ Users can start/complete practice sessions
- ✅ Audio plays and can be replayed
- ✅ Forms validate and provide feedback
- ✅ Scoring displays correctly with visual feedback
- ✅ Glossary is accessible and helpful
- ✅ UI is responsive and doesn't freeze during playback

---

### Phase 4: Configuration & Polish - Issues #11-12
**Goal:** Configuration system and documentation

**Duration Estimate:** 2-3 development sessions

**Work Items:**
1. **Issue #11: Configuration Extension**
   - Depends on: All backend issues
   - Modifies: `config.json`, `morse.py`, `morse_gui.py`
   - Deliverable: QSO-specific configuration options

2. **Issue #12: Documentation Updates**
   - Depends on: All other issues (documents completed features)
   - Modifies: `README.md`, `CONFIG.md`, `CLAUDE.md`
   - Deliverable: Complete documentation of QSO feature

**Phase 4 Success Criteria:**
- ✅ All QSO settings are configurable
- ✅ Configuration persists across sessions
- ✅ Documentation is complete and accurate
- ✅ User guide helps new users understand the feature
- ✅ Developer documentation explains architecture

---

## Development Workflow Recommendations

### Getting Started
1. Create a feature branch: `git checkout -b feature/qso-practice`
2. Start with Issue #2 (Data Module) - it has no dependencies
3. Write tests as you go (especially for call sign generation)
4. Commit frequently with references to issue numbers

### Branch Strategy
```
main
  └── feature/qso-practice (main feature branch)
        ├── feature/qso-data (Issues #2-5)
        ├── feature/qso-backend (Issues #6-7)
        ├── feature/qso-gui (Issues #8-10)
        └── feature/qso-config (Issues #11-12)
```

Alternative: Work directly in `feature/qso-practice` and merge issues as completed.

### Commit Message Format
```
Issue #N: Brief description

Detailed explanation of changes
- Bullet points for major changes
- Reference any design decisions

Refs: #N
```

Example:
```
Issue #2: Add QSO data module with reference data

- Created qso_data.py with all data lists
- Implemented abbreviation dictionary
- Added validation for all data structures
- Follows security patterns from morse.py

Refs: #2
```

### Testing Strategy

**Unit Tests (create as you go):**
- `test_qso_data.py` - Test data validation
- `test_callsign_generator.py` - Test all call sign formats
- `test_qso_template.py` - Test template rendering
- `test_qso_scoring.py` - Test scoring logic

**Integration Tests:**
- `test_qso_generation.py` - End-to-end QSO generation
- `test_qso_session.py` - Complete session workflow

**Manual Testing Checklist:**
- [ ] Generate 20 call signs for each supported region
- [ ] Verify all templates render correctly
- [ ] Test QSO at each verbosity level
- [ ] Run complete session in GUI
- [ ] Test all audio controls (play/replay/skip)
- [ ] Verify scoring with various inputs
- [ ] Test fuzzy matching edge cases
- [ ] Verify configuration persistence
- [ ] Test glossary search functionality

### Code Style Guidelines

**Follow Existing Patterns:**
- Match style from `morse.py` and `morse_gui.py`
- Use same security validation patterns
- Follow same logging conventions
- Maintain docstring format

**Security Considerations:**
- Validate all user inputs
- Use existing sanitization patterns
- Set reasonable limits (max call sign length, etc.)
- Add logging for security events

**Performance:**
- Don't block UI during audio playback (use threading)
- Keep QSO generation fast (< 100ms)
- Cache templates if needed
- Limit session history to prevent memory issues

---

## Dependencies Map

```
Issue #2 (Data Module)
  ├─> Issue #3 (Call Sign Generator)
  ├─> Issue #4 (Template System)
  └─> Issue #9 (Glossary)

Issue #3, #4 (Generators & Templates)
  └─> Issue #5 (QSO Generator)

Issue #5 (QSO Generator)
  └─> Issue #6 (Session Manager)

Issue #6 (Session Manager)
  ├─> Issue #7 (Scoring)
  └─> Issue #8 (GUI Tab)

Issue #7, #8 (Scoring & GUI)
  └─> Issue #10 (Audio Controls)

All Backend Issues
  └─> Issue #11 (Configuration)

All Issues
  └─> Issue #12 (Documentation)
```

---

## Suggested Development Order

### Week 1: Backend Foundation
- [ ] Issue #2: QSO Data Module (Day 1-2)
- [ ] Issue #3: Call Sign Generator (Day 2-3)
- [ ] Issue #4: Template System (Day 3-4)
- [ ] Issue #5: QSO Generator Integration (Day 4-5)
- [ ] Write tests for all backend components

**Checkpoint:** Can generate complete QSOs programmatically

### Week 2: Backend Logic
- [ ] Issue #6: Session Manager (Day 1-2)
- [ ] Issue #7: Scoring System (Day 2-3)
- [ ] Integration testing
- [ ] Bug fixes

**Checkpoint:** Can run practice sessions in Python REPL

### Week 3: GUI Implementation
- [ ] Issue #8: GUI Practice Tab (Day 1-3)
- [ ] Issue #9: Glossary (Day 3-4)
- [ ] Issue #10: Audio Controls (Day 4-5)

**Checkpoint:** Feature is usable in GUI

### Week 4: Polish & Documentation
- [ ] Issue #11: Configuration (Day 1-2)
- [ ] Issue #12: Documentation (Day 2-3)
- [ ] End-to-end testing
- [ ] Bug fixes and refinement
- [ ] Prepare for merge to main

**Checkpoint:** Feature is complete and documented

---

## Future Enhancements (Post-MVP)

Track these as separate issues later:

### Deferred Features
- **Contest-Style QSOs** - Shorter, rapid exchanges
- **DX Expedition Scenarios** - Pileup simulation
- **QRM/QSB Effects** - Realistic interference and fading
- **Statistics Persistence** - Track progress over time
- **Difficulty Progression** - Adaptive difficulty based on performance
- **Custom Templates** - User-defined QSO formats
- **Export Functionality** - Save QSO logs
- **Multi-language Support** - Non-English operators

### Technical Debt to Avoid
- Keep modules decoupled (qso_data, qso_practice, morse_gui)
- Write comprehensive docstrings
- Add TODO comments for future enhancements
- Don't hard-code values that should be configurable
- Maintain test coverage above 70%

---

## Success Metrics

### Feature Complete When:
1. ✅ All 11 GitHub issues are closed
2. ✅ User can complete a QSO practice session in GUI
3. ✅ Scoring works accurately with appropriate feedback
4. ✅ Documentation is complete
5. ✅ No known critical bugs
6. ✅ Code passes existing security standards
7. ✅ Feature integrates seamlessly with existing app

### Quality Gates:
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing checklist complete
- [ ] Code review by maintainer
- [ ] Documentation review
- [ ] No regressions in existing features

---

## Communication

### Issue Updates
- Comment on issues with progress
- Reference commits in issue comments
- Use GitHub's task lists in issues
- Close issues with "Closes #N" in commit message

### Getting Help
- Comment on specific issue for questions
- Reference QSO_FEATURE.md for specifications
- Check CLAUDE.md for architecture guidance

---

## Quick Reference

**Main Documents:**
- `QSO_FEATURE.md` - Complete technical specification
- `QSO_IMPLEMENTATION_PLAN.md` - This document
- GitHub Issues - Detailed work items

**Key Files to Create:**
- `qso_data.py` - Data and generation classes
- `qso_practice.py` - Session and scoring logic
- Modifications to `morse_gui.py` - New tab and glossary

**Key Files to Modify:**
- `config.json` - Add QSO configuration
- `morse.py` - Extend config validation
- `README.md`, `CONFIG.md`, `CLAUDE.md` - Documentation

---

**Last Updated:** 2025-11-28
**Status:** Ready for implementation
**Estimated Total Effort:** 12-17 development sessions (3-4 weeks)
