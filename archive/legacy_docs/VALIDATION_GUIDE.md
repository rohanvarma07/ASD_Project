# Email & Password Validation Guide

## Overview
The ASD Detection System now includes comprehensive validation for registration and login forms to ensure data integrity and security.

---

## Email Validation

### ✅ Supported Email Formats

The system accepts a wide range of email formats with various top-level domains (TLDs):

#### Common TLDs Supported:
- **Generic**: `.com`, `.net`, `.org`, `.edu`, `.gov`, `.mil`
- **Country Codes**: `.in`, `.us`, `.uk`, `.ca`, `.au`, `.de`, `.fr`, `.jp`, `.cn`, `.br`, `.ru`, `.za`
- **Modern**: `.io`, `.ai`, `.me`, `.co`
- **Combined**: `.co.in`, `.co.uk`, `.ac.in`, `.edu.in`, `.gov.in`

#### Valid Email Examples:
```
✓ user@example.com
✓ john.doe@company.in
✓ admin@university.edu
✓ contact@organization.org
✓ info@startup.io
✓ support@business.co.uk
✓ student@college.ac.in
✓ teacher@school.edu.in
✓ developer@tech.ai
✓ test.user+tag@domain.net
```

### ❌ Invalid Email Examples:
```
✗ plainaddress (missing @ and domain)
✗ @nodomain.com (missing local part)
✗ user@.com (missing domain name)
✗ user..name@domain.com (consecutive dots)
✗ user@domain (missing TLD)
✗ user @domain.com (space before @)
✗ user@@domain.com (double @)
✗ user@domain.xyz (unsupported TLD)
```

### Validation Rules:
1. **Format**: `localpart@domain.tld`
2. **Local Part**: 1-64 characters, can include letters, numbers, dots, underscores, percent, plus, hyphen
3. **Domain**: 3-255 characters, must have valid TLD
4. **Special Cases**: No consecutive dots (..), exactly one @ symbol
5. **TLD Verification**: Must end with a recognized top-level domain

---

## Password Validation

### ✅ Password Requirements

Strong passwords must meet ALL of the following criteria:

#### Mandatory Requirements:
1. **Minimum Length**: At least 8 characters
2. **Maximum Length**: Up to 128 characters
3. **Uppercase Letter**: At least one (A-Z)
4. **Lowercase Letter**: At least one (a-z)
5. **Number**: At least one digit (0-9)
6. **Special Character**: At least one from `!@#$%^&*()_+-=[]{};:'",.<>?/\|~`
7. **No Spaces**: Password cannot contain whitespace

#### Valid Password Examples:
```
✓ MyPass123!
✓ SecureP@ssw0rd
✓ Admin#2026Test
✓ User$1234Strong
✓ Abc123!@#xyz
✓ P@ssW0rd2026!
✓ Test@User#123
✓ MyS3cur3P@ss!
```

#### Invalid Password Examples:
```
✗ pass123        (no uppercase, no special char)
✗ PASSWORD!      (no lowercase, no number)
✗ Password123    (no special character)
✗ Pass@12        (less than 8 characters)
✗ my pass 123!   (contains spaces)
✗ password       (no uppercase, no number, no special char)
✗ 12345678       (no letters, no special char)
```

### Password Strength Indicators:
- **Weak**: Missing multiple requirements
- **Medium**: Meets minimum requirements
- **Strong**: 8+ characters with all requirements
- **Very Strong**: 12+ characters with mixed complexity

---

## Mobile Number Validation

### ✅ Valid Mobile Format

Indian mobile number validation:

#### Requirements:
1. **Exactly 10 digits**
2. **First digit**: Must be 6, 7, 8, or 9 (Indian mobile format)
3. **No spaces or special characters**

#### Valid Examples:
```
✓ 9876543210
✓ 8765432109
✓ 7654321098
✓ 6543210987
```

#### Invalid Examples:
```
✗ 1234567890 (starts with 1)
✗ 98765432   (less than 10 digits)
✗ 987654321012 (more than 10 digits)
✗ 98765-43210 (contains hyphen)
✗ 987 654 3210 (contains spaces)
```

---

## Frontend Validation (JavaScript)

### Real-time Validation Features:
- ✅ Instant feedback on field blur
- ✅ Clear, specific error messages
- ✅ Visual indicators (red border for errors)
- ✅ Inline help text with format hints
- ✅ Form submission prevention if invalid

### Error Display:
- Red border on invalid fields
- Error message below the field
- Automatic error clearing when field is corrected

---

## Backend Validation (Python/Flask)

### Server-side Security:
- ✅ All fields validated before database insertion
- ✅ Protection against malicious inputs
- ✅ Duplicate email prevention
- ✅ Password hashing with Werkzeug
- ✅ SQL injection protection with parameterized queries

### Flash Messages:
Users receive immediate feedback for:
- Missing required fields
- Invalid email format
- Weak password
- Password mismatch
- Mobile number format errors
- Duplicate account attempts

---

## Testing the Validation

### Test Scenario 1: Invalid Email Formats
1. Try registering with `user@example` (no TLD)
2. Try registering with `user..test@example.com` (consecutive dots)
3. Try registering with `user@domain.xyz` (unsupported TLD)

**Expected Result**: Error message "Please use a valid email domain (e.g., .com, .in, .org, .edu, .net)"

### Test Scenario 2: Weak Passwords
1. Try `password123` (no uppercase, no special char)
2. Try `Password!` (less than 8 chars)
3. Try `PASSWORD123!` (no lowercase)

**Expected Result**: Specific error message for each missing requirement

### Test Scenario 3: Invalid Mobile
1. Try `1234567890` (starts with 1)
2. Try `98765` (less than 10 digits)

**Expected Result**: Error message "Please enter a valid 10-digit mobile number (must start with 6-9)"

### Test Scenario 4: Valid Registration
1. Email: `test.user@example.com`
2. Mobile: `9876543210`
3. Password: `MyPass123!`
4. Confirm: `MyPass123!`

**Expected Result**: "Registration successful! Please login."

---

## Security Benefits

### 1. Email Validation
- Prevents typos in email addresses
- Ensures deliverability for email notifications
- Reduces fake account creation
- Validates against common email providers

### 2. Password Validation
- **Brute Force Protection**: Complex passwords harder to crack
- **Dictionary Attack Prevention**: Not simple words
- **Character Variety**: Increases password entropy
- **Length Requirement**: Exponentially harder to break

### 3. Mobile Validation
- Ensures Indian mobile format
- Prevents invalid phone numbers
- Maintains data quality for SMS notifications

---

## Error Messages Reference

### Registration Form Errors:

| Field | Error Condition | Message |
|-------|----------------|---------|
| Username | Empty | "Username is required" |
| Username | < 3 chars | "Username must be at least 3 characters" |
| Username | > 50 chars | "Username must not exceed 50 characters" |
| Email | Empty | "Email is required" |
| Email | Invalid format | "Please enter a valid email address" |
| Email | Invalid TLD | "Please use a valid email domain (e.g., .com, .in, .org, .edu, .net)" |
| Email | Consecutive dots | "Email cannot contain consecutive dots" |
| Mobile | Empty | "Mobile number is required" |
| Mobile | Invalid format | "Please enter a valid 10-digit mobile number (must start with 6-9)" |
| Password | Empty | "Password is required" |
| Password | < 8 chars | "Password must be at least 8 characters long" |
| Password | No uppercase | "Password must contain at least one uppercase letter (A-Z)" |
| Password | No lowercase | "Password must contain at least one lowercase letter (a-z)" |
| Password | No number | "Password must contain at least one number (0-9)" |
| Password | No special char | "Password must contain at least one special character (!@#$%^&* etc.)" |
| Password | Contains spaces | "Password must not contain spaces" |
| Confirm Password | Empty | "Please confirm your password" |
| Confirm Password | Mismatch | "Passwords do not match" |

### Login Form Errors:

| Field | Error Condition | Message |
|-------|----------------|---------|
| Email | Empty | "Email is required" |
| Email | Invalid format | "Please enter a valid email address" |
| Password | Empty | "Password is required" |
| Credentials | Wrong | "Invalid email or password" |

---

## Implementation Details

### Files Modified:
1. **`app.py`** - Backend validation functions
   - `validate_email()` - Comprehensive email check
   - `validate_password()` - Password strength validation
   - `validate_mobile()` - Mobile number format check

2. **`static/js/script.js`** - Frontend validation
   - `validateEmailFormat()` - Real-time email validation
   - `validatePasswordStrength()` - Real-time password check
   - `isValidMobile()` - Mobile format verification

3. **`templates/register.html`** - Updated form with hints
4. **`templates/login.html`** - Updated login form

### Validation Flow:
```
User Input → Frontend Validation → Form Submit → Backend Validation → Database
```

Both frontend and backend validation ensure maximum security and user experience.

---

## Best Practices for Users

### Creating a Strong Password:
1. Use a mix of uppercase and lowercase letters
2. Include numbers and special characters
3. Avoid common words or patterns
4. Make it at least 8 characters (12+ recommended)
5. Don't reuse passwords from other sites

### Example Strong Passwords:
- `MyASD@2026Test`
- `SecureApp#123Pass`
- `Autism$Detect99!`

### Email Tips:
- Use your primary email for important accounts
- Verify the domain extension matches your provider
- Avoid typos that could prevent login

---

## Developer Notes

### Adding New TLDs:
To support additional top-level domains, update the `common_tlds` list in:
- `app.py` - `validate_email()` function
- `script.js` - `validateEmailFormat()` function

### Adjusting Password Complexity:
Modify the validation functions to change requirements:
- Minimum length: Currently 8 characters
- Special characters: Customize the allowed set
- Complexity rules: Add or remove regex patterns

### Internationalization:
Current mobile validation is set for Indian numbers (10 digits, starts with 6-9). To support international formats, update the `validate_mobile()` and `isValidMobile()` functions.

---

## Summary

✅ **Email**: Supports 20+ TLDs including .com, .in, .org, .edu, .net, .co.uk, etc.  
✅ **Password**: Minimum 8 characters with uppercase, lowercase, number, and special character  
✅ **Mobile**: 10-digit Indian format starting with 6-9  
✅ **Real-time**: Frontend validation provides instant feedback  
✅ **Secure**: Backend validation prevents malicious inputs  
✅ **User-friendly**: Clear error messages guide users to correct issues  

**Your data is validated at every step for maximum security and accuracy!** 🔒
