# ASD Screening Questionnaire Feature

## Overview
A comprehensive, professional screening questionnaire component that allows users to complete autism spectrum disorder screening directly within the application.

## Implementation Date
March 11, 2026

## Features

### 1. **Comprehensive Questionnaire**
- **Personal Information Section (6 fields)**:
  - Age (numeric input, 1-120 range)
  - Gender (Male/Female/Other)
  - Ethnicity (8 options: White, Black, Asian, Hispanic, Middle Eastern, South Asian, Mixed, Other)
  - Jaundice at Birth (Yes/No)
  - Family History of Autism (Yes/No)
  - Previous Exam Result (Not Tested/Positive/Negative)

- **Behavioral Screening (10 yes/no questions)**:
  1. Prefers Same Routine?
  2. Repeats Words/Phrases?
  3. Extreme Focus on Topics?
  4. Struggles with Empathy?
  5. Upset by Changes?
  6. Finds Socializing Hard?
  7. Difficulty Making Friends?
  8. Repetitive Movements?
  9. Avoids Eye Contact?
  10. Struggles with Expressions?

### 2. **Smart Risk Assessment**
- **Automatic Score Calculation**: Counts "Yes" answers (0-10 scale)
- **Risk Level Classification**:
  - **Low**: 0-3 "Yes" answers (Green)
  - **Medium**: 4-6 "Yes" answers (Orange)
  - **High**: 7-10 "Yes" answers (Red)

### 3. **Data Persistence**
- ✅ Saves screening results to database
- ✅ One screening per user (updates on resubmission)
- ✅ Pre-populates form with previous answers on revisit
- ✅ Persists across page refreshes and sessions
- ✅ Displays results immediately after submission

### 4. **Dashboard Integration**
- ✅ New "ASD Screening" card at top of dashboard
- ✅ Shows "Start Screening" or "View Results" based on completion status
- ✅ Displays screening results card with:
  - Total score (X/10)
  - Risk level (Low/Medium/High)
  - Color-coded gradient background
  - "View Details" button to screening page
- ✅ Responsive design for mobile devices

### 5. **Professional UI/UX**
- **Modern Card-Based Layout**: Each question in its own card
- **Progress Bar**: Real-time progress tracking as form is filled
- **Color-Coded Results**: 
  - Green gradient for Low risk
  - Orange gradient for Medium risk
  - Red gradient for High risk
- **Form Validation**: Required fields, age range checks
- **Responsive Grid**: 3-4 columns on desktop → 1 column on mobile
- **Hover Effects**: Cards lift on hover for better UX
- **Professional Typography**: Clean, readable fonts

## Technical Implementation

### Database Schema
**New Table: `screening_results`**
```sql
CREATE TABLE screening_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    ethnicity TEXT NOT NULL,
    jaundice TEXT NOT NULL,
    family_history TEXT NOT NULL,
    exam_result TEXT NOT NULL,
    q1_routine TEXT NOT NULL,
    q2_repeats TEXT NOT NULL,
    q3_focus TEXT NOT NULL,
    q4_empathy TEXT NOT NULL,
    q5_changes TEXT NOT NULL,
    q6_socializing TEXT NOT NULL,
    q7_friends TEXT NOT NULL,
    q8_movements TEXT NOT NULL,
    q9_eye_contact TEXT NOT NULL,
    q10_expressions TEXT NOT NULL,
    total_score INTEGER,
    risk_level TEXT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_email) REFERENCES users (email)
)
```

### Backend Routes
**Route: `/screening`**
- **GET**: Display form, pre-populate if screening exists
- **POST**: Process submission, calculate score, save to database, display results

### Files Modified/Created
1. **Created**: `templates/screening.html` (~500 lines)
2. **Modified**: `database.py` (+100 lines)
   - Added `screening_results` table to `init_database()`
   - Added `save_screening_result(user_email, screening_data)` method
   - Added `get_screening_result(user_email)` method
3. **Modified**: `app.py` (+60 lines)
   - Added `/screening` route (GET and POST)
   - Updated `/dashboard` route to pass screening data
4. **Modified**: `templates/dashboard.html` (+50 lines)
   - Added screening card to dashboard grid
   - Added results display card (conditional on completion)

## User Flow

### First-Time User
1. Login → Dashboard
2. See "ASD Screening" card with "Start Screening" button
3. Click → Navigate to screening form
4. Fill out 16 fields (6 personal + 10 behavioral)
5. Progress bar updates as form is filled
6. Submit → See results immediately
7. Results saved to database
8. Return to dashboard → See results card with score and risk level

### Returning User
1. Login → Dashboard
2. See "ASD Screening" card with "View Results" button
3. See results card showing previous score and risk level
4. Click "View Results" or "View Details" → Navigate to screening page
5. Form pre-populated with previous answers
6. Can update answers and resubmit
7. Updated results saved (overwrites previous)

## Benefits

### For Users
- ✅ Quick self-assessment (5-10 minutes)
- ✅ Immediate feedback on risk level
- ✅ Professional, easy-to-understand results
- ✅ Can update screening anytime
- ✅ Accessible from dashboard and navigation

### For System
- ✅ Structured data collection
- ✅ Database-backed persistence
- ✅ Scalable to handle many users
- ✅ Ready for future analytics/reporting
- ✅ Integrates with existing authentication

## Future Enhancements

### Potential Additions
1. **PDF Export**: Download screening results as PDF
2. **Email Results**: Send results to user's email
3. **Screening History**: Track multiple screenings over time
4. **Charts/Visualizations**: Graphical representation of results
5. **Professional Recommendations**: Based on risk level
6. **Share with Healthcare Provider**: Export for professional review
7. **Multi-language Support**: Translate questionnaire
8. **Age-Specific Questions**: Customize based on age group

## Deployment Notes

### Production Checklist
- ✅ Database schema includes screening_results table
- ✅ PostgreSQL support included (same schema)
- ✅ Form validation on client and server side
- ✅ Error handling for database operations
- ✅ Session-based authentication required
- ✅ Responsive design for all devices
- ✅ Accessible navigation structure

### Testing Recommendations
1. Test form submission with all field combinations
2. Test pre-population on revisit
3. Test score calculation (0-10 range)
4. Test risk level classification
5. Test dashboard display with/without screening
6. Test mobile responsiveness
7. Test concurrent users

## Success Metrics
- User completion rate (% who start and finish)
- Time to complete screening
- Update frequency (how often users retake)
- Risk level distribution across users
- Dashboard engagement with screening card

---

**Status**: ✅ PRODUCTION READY  
**Last Updated**: March 11, 2026  
**Version**: 1.0.0
