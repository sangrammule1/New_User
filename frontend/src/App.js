import { useState } from "react";
import "./App.css";

function App() {
  const translations = {
    en: {
      firstName: "First Name",
      lastName: "Last Name",
      phone: "Phone",
      email: "Email",
      required: "*",
      firstNamePlaceholder: "Enter first name",
      lastNamePlaceholder: "Enter last name",
      phonePlaceholder: "Enter phone number",
      emailPlaceholder: "Enter email address",
      firstNameError: "First name is required",
      lastNameError: "Last name is required",
      phoneError: "Phone is required",
      registrationTitle: "Registration Form",
      registrationSubtitle: "Please fill in all required fields to complete your registration",
      cancelButton: "Cancel",
      submitButton: "Submit",
      submittingText: "Submitting...",
      successMessage: "Form submitted successfully!",
      errorMessage: "An error occurred. Please try again.",
    },
    hi: {
      firstName: "पहला नाम",
      lastName: "अंतिम नाम",
      phone: "फ़ोन",
      email: "ईमेल",
      required: "*",
      firstNamePlaceholder: "पहला नाम दर्ज करें",
      lastNamePlaceholder: "अंतिम नाम दर्ज करें",
      phonePlaceholder: "फ़ोन नंबर दर्ज करें",
      emailPlaceholder: "ईमेल पता दर्ज करें",
      firstNameError: "पहला नाम आवश्यक है",
      lastNameError: "अंतिम नाम आवश्यक है",
      phoneError: "फ़ोन आवश्यक है",
      registrationTitle: "पंजीकरण फ़ॉर्म",
      registrationSubtitle: "अपना पंजीकरण पूरा करने के लिए कृपया सभी आवश्यक फ़ील्ड भरें",
      cancelButton: "रद्द करें",
      submitButton: "सबमिट करें",
      submittingText: "सबमिट हो रहा है...",
      successMessage: "फ़ॉर्म सफलतापूर्वक सबमिट हो गया!",
      errorMessage: "एक त्रुटि हुई। कृपया पुनः प्रयास करें।",
    },
  };

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    phone: "",
    email: "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [language, setLanguage] = useState("en"); // State for language

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    const processedValue = name === "house_no" ? (value === "" ? null : parseInt(value, 10)) : value;
    setForm({ ...form, [name]: processedValue });
    if (errors[name]) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const validateForm = () => {
    const newErrors = {};
    const currentTranslations = translations[language];

    if (!form.first_name.trim()) {
      newErrors.first_name = currentTranslations.firstNameError;
    }
    if (!form.last_name.trim()) {
      newErrors.last_name = currentTranslations.lastNameError;
    }
    if (!form.phone.trim()) {
      newErrors.phone = currentTranslations.phoneError;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch("http://localhost:6080/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await response.json();
      alert(data.message || translations[language].successMessage);

      if (response.ok) {
        setForm({
          first_name: "",
          last_name: "",
          phone: "",
          email: "",
        });
      }
    } catch (error) {
      alert(translations[language].errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const currentTranslations = translations[language];

  return (
    <div className={`form-container ${isDarkMode ? 'dark' : ''}`}>
      <div className="language-selector-container">
        <select value={language} onChange={handleLanguageChange}>
          <option value="en">English</option>
          <option value="hi">हिन्दी</option>
        </select>
      </div>
      <div className="form-panel">
        <div className="form-header">
          <h2 className="form-title">{currentTranslations.registrationTitle}</h2>
          <p className="form-subtitle">{currentTranslations.registrationSubtitle}</p>
        </div>

        <form onSubmit={handleSubmit} className="registration-form">
          <div className="form-row">
            <div className="form-field">
              <label className="form-label">
                {currentTranslations.firstName}<span className="required">{currentTranslations.required}</span>
              </label>
              <div className="input-wrapper">
                <input
                  className={`form-input ${errors.first_name ? 'error' : ''}`}
                  name="first_name"
                  value={form.first_name}
                  onChange={handleChange}
                  placeholder={currentTranslations.firstNamePlaceholder}
                  required
                />
                <span className="input-icon">👤</span>
              </div>
              {errors.first_name && <span className="error-message">{errors.first_name}</span>}
            </div>

            <div className="form-field">
              <label className="form-label">
                {currentTranslations.lastName}<span className="required">{currentTranslations.required}</span>
              </label>
              <div className="input-wrapper">
                <input
                  className={`form-input ${errors.last_name ? 'error' : ''}`}
                  name="last_name"
                  value={form.last_name}
                  onChange={handleChange}
                  placeholder={currentTranslations.lastNamePlaceholder}
                  required
                />
                <span className="input-icon">👤</span>
              </div>
              {errors.last_name && <span className="error-message">{errors.last_name}</span>}
            </div>
          </div>
          <div className="form-row">
            <div className="form-field">
              <label className="form-label">
                {currentTranslations.phone}<span className="required">{currentTranslations.required}</span>
              </label>
              <div className="input-wrapper">
                <input
                  className={`form-input ${errors.phone ? 'error' : ''}`}
                  name="phone"
                  value={form.phone}
                  onChange={handleChange}
                  placeholder={currentTranslations.phonePlaceholder}
                  required
                />
                <span className="input-icon">📞</span>
              </div>
              {errors.phone && <span className="error-message">{errors.phone}</span>}
            </div>

            <div className="form-field">
              <label className="form-label">
                {currentTranslations.email}
              </label>
              <div className="input-wrapper">
                <input
                  className="form-input"
                  name="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder={currentTranslations.emailPlaceholder}
                />
                <span className="input-icon">✉️</span>
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button type="button" className="cancel-button">
              <span>{currentTranslations.cancelButton}</span>
            </button>
            <button type="submit" className="submit-button" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <span className="spinner"></span>
                  <span>{currentTranslations.submittingText}</span>
                </>
              ) : (
                <>
                  <span>✓</span>
                  <span>{currentTranslations.submitButton}</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
      <div className="dark-mode-toggle-container">
        <button onClick={toggleDarkMode} className="dark-mode-toggle-button">
          {isDarkMode ? '☀️' : '🌙'}
        </button>
      </div>
    </div>
  );
}

export default App;