function validateContact(e) {
  e.preventDefault();
  const name = document.getElementById("fullname").value.trim();
  const email = document.getElementById("email").value;
  const message = document.getElementById("message").value.trim();

  if (name.length < 5) return alert("Please enter your full name.");
  if (!email.includes("@")) return alert("Please enter a valid email address.");
  if (message.length < 5) return alert("Please enter a message.");

  alert("✅ Thank you for contacting SecureCare Hospital!");
  e.target.reset();
  return true;
}

function validatePatientForm(e) {
  e.preventDefault();

  const form = e.target;
  const id = form.patient_id.value.trim();
  const age = parseInt(form.age.value);
  const glucose = parseFloat(form.avg_glucose_level.value);
  const bmi = parseFloat(form.bmi.value);

  if (!/^\d+$/.test(id)) {
    alert("❌ Patient ID must contain only numbers.");
    return false;
  }

  if (age < 0 || age > 120) {
    alert("❌ Age must be between 0 and 120.");
    return false;
  }

  if (glucose < 0 || bmi < 0) {
    alert("❌ Glucose and BMI must be positive numbers.");
    return false;
  }

  alert("✅ Patient registration saved successfully!");
  form.reset();
  return true;
}
