import { useState } from "react";
import "./App.css";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  const [form, setForm] = useState({
    attendance: "",
    study_hours: "",
    previous_marks: "",
    assignment_completion: ""
  });

  const [result, setResult] = useState("");

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    if (
      !form.attendance ||
      !form.study_hours ||
      !form.previous_marks ||
      !form.assignment_completion
    ) {
      alert("Please fill all fields");
      return;
    }

    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        attendance: parseInt(form.attendance),
        study_hours: parseInt(form.study_hours),
        previous_marks: parseInt(form.previous_marks),
        assignment_completion: parseInt(form.assignment_completion)
      })
    });

    const data = await response.json();
    setResult(data.risk);
  }

  return (
    <div className={`app ${darkMode ? "dark" : "light"}`}>
      <div className="container">
        <div className="card">
          <div
            className="toggle"
            onClick={() => setDarkMode(!darkMode)}
          >
            {darkMode ? "☀ Light Mode" : "🌙 Dark Mode"}
          </div>

          <h1>Student Risk Predictor</h1>

          <form onSubmit={handleSubmit}>
            <input
              name="attendance"
              placeholder="Attendance (%)"
              onChange={handleChange}
            />
            <input
              name="study_hours"
              placeholder="Study Hours"
              onChange={handleChange}
            />
            <input
              name="previous_marks"
              placeholder="Previous Marks (%)"
              onChange={handleChange}
            />
            <input
              name="assignment_completion"
              placeholder="Assignment Completion (%)"
              onChange={handleChange}
            />

            <button type="submit">Predict</button>
          </form>

          {result && (
            <div
              className={`result ${
                result === "YES" ? "risk" : "safe"
              }`}
            >
              Risk Status: {result}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
