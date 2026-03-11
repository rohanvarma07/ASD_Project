# Screening Feature - Quick Test Guide

## How to Test the New Screening Feature

### Step 1: Login
1. Navigate to `http://localhost:5001`
2. Click "Login" or navigate to `/login`
3. Use credentials:
   - Email: `admin@example.com`
   - Password: `Admin@123`

### Step 2: Access Screening from Dashboard
1. After login, you'll see the dashboard
2. Look for the new **"ASD Screening"** card (top-left)
3. Button will say **"Start Screening"** (first time) or **"View Results"** (if already completed)
4. Below the cards, you'll see a results card if screening is complete

### Step 3: Complete the Screening
1. Click "Start Screening" or navigate to `/screening`
2. You'll see a beautiful form with:
   - Header with title and description
   - Progress bar (initially empty)
   - Personal Information section (6 fields)
   - Behavioral Screening section (10 questions)
3. Fill out all fields:
   - **Age**: Enter any number 1-120 (e.g., `25`)
   - **Gender**: Select Male/Female/Other
   - **Ethnicity**: Choose from dropdown
   - **Jaundice**: Yes/No
   - **Family History**: Yes/No
   - **Exam Result**: Not Tested/Positive/Negative
   - **10 Behavioral Questions**: Answer Yes/No for each
4. Watch the progress bar fill up as you complete fields
5. Click "Submit Screening 🚀"

### Step 4: View Results
After submission, you'll see:
1. **Flash message** at top: "Screening completed! Risk Level: [Low/Medium/High] (Score: X/10)"
2. **Results card** below the form with:
   - Color-coded gradient (Green=Low, Orange=Medium, Red=High)
   - Total score (X/10)
   - Risk level
   - Helpful message based on risk level

### Step 5: Verify Dashboard Integration
1. Click "Dashboard" in navigation or go to `/dashboard`
2. You should see:
   - "ASD Screening" card now shows **"View Results"** button
   - New colored results card displaying your score and risk level
   - "View Details →" button to go back to screening page

### Step 6: Test Data Persistence (Refresh)
1. While on dashboard, press **Refresh (F5)** or **Cmd+R**
2. Results card should still be visible
3. Click "View Results" → Form should be pre-populated with your answers
4. This proves data persists in database!

### Step 7: Test Update Functionality
1. Go to `/screening`
2. Change some answers (e.g., change some "No" to "Yes")
3. Click "Update Screening 🚀"
4. Score and risk level should update
5. Dashboard should reflect new results

## Sample Test Scenarios

### Scenario 1: Low Risk (Score 0-3)
Answer "No" to all 10 behavioral questions
- Expected: Green card, "Low" risk level, score 0/10
- Message: "Lower indicators detected. Monitor development regularly."

### Scenario 2: Medium Risk (Score 4-6)
Answer "Yes" to 5 behavioral questions, "No" to 5
- Expected: Orange card, "Medium" risk level, score 5/10
- Message: "Moderate indicators detected. Consider professional consultation."

### Scenario 3: High Risk (Score 7-10)
Answer "Yes" to 8-10 behavioral questions
- Expected: Red card, "High" risk level, score 8-10/10
- Message: "Higher indicators detected. Professional evaluation recommended."

## What to Look For

### ✅ Successful Implementation Indicators
- [ ] Progress bar animates smoothly as form is filled
- [ ] Form validation prevents empty submissions
- [ ] All 16 fields save correctly
- [ ] Score calculates correctly (count of "Yes" answers)
- [ ] Risk level matches score (0-3=Low, 4-6=Medium, 7-10=High)
- [ ] Results display with correct color coding
- [ ] Dashboard shows screening card
- [ ] Dashboard shows results card (if completed)
- [ ] Form pre-populates on revisit
- [ ] Data persists across page refreshes
- [ ] Update button replaces submit button after completion
- [ ] Mobile responsive (test on phone or resize browser)

### 🐛 Common Issues to Check
- [ ] If results don't show → Check database connection
- [ ] If form doesn't pre-populate → Check `get_screening_result()` method
- [ ] If score is wrong → Verify field names match (q1_routine, q2_repeats, etc.)
- [ ] If dashboard doesn't update → Check `screening_data` is passed to template
- [ ] If progress bar doesn't work → Check JavaScript is loading

## Browser Testing
Test in:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers (iOS Safari, Chrome Android)

## Database Verification

### Check if screening was saved:
```bash
# Open SQLite database
sqlite3 asd_database.db

# View screening results
SELECT * FROM screening_results;

# Expected output:
# id | user_email | age | gender | ethnicity | ... | total_score | risk_level | completed_at
# 1  | admin@example.com | 25 | Male | Asian | ... | 5 | Medium | 2026-03-11 10:55:00
```

## Navigation Testing

### All routes should be accessible:
1. `/` → Home page
2. `/register` → Registration
3. `/login` → Login
4. `/dashboard` → Dashboard (after login)
5. `/screening` → **NEW** Screening questionnaire (after login)
6. `/upload` → Upload dataset (after login)
7. `/results` → View results (after login)
8. `/about` → About page
9. `/logout` → Logout

## Performance Testing
- [ ] Form loads quickly (< 1 second)
- [ ] Submission processes quickly (< 2 seconds)
- [ ] Dashboard loads with results (< 1 second)
- [ ] No console errors in browser DevTools

## Expected Timeline
- **Initial screening**: 5-10 minutes
- **Update screening**: 2-5 minutes
- **View results**: Immediate

---

**Quick Test Checklist**:
1. ✅ Login successful
2. ✅ Dashboard shows screening card
3. ✅ Screening form loads
4. ✅ Progress bar works
5. ✅ All fields accept input
6. ✅ Form validates properly
7. ✅ Submission succeeds
8. ✅ Results display correctly
9. ✅ Dashboard updates with results
10. ✅ Refresh persists data
11. ✅ Update functionality works
12. ✅ Mobile responsive

**Status**: Ready for testing! 🚀
