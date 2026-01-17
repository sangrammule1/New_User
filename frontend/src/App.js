import { useState } from "react";

function App() {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    phone: "",
    email: "",
    zipcode: "",
    houseno: "",
    streetno: "",
    dob: "",
    time: "",
    create_time: ""
    });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://localhost:6080/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    const data = await response.json();
    alert(data.message);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2 >Registration Form</h2 >

      <form onSubmit={handleSubmit}>
        <div >
          <label >First Name:</label > <br />
          <input
            name="first_name"
            value={form.first_name}
            onChange={handleChange}
            required
          />
        </div >

        <div >
          <label >Last Name:</label > <br />
          <input
            name="last_name"
            value={form.last_name}
            onChange={handleChange}
            required
          />
        </div >

        <div >
          <label >Phone:</label > <br />
          <input
            name="phone"
            value={form.phone}
            onChange={handleChange}
            required
          />
        </div>
        <div >
          <label >Email:</label > <br />
          <input
            name="email"
            value={form.email}
            onChange={handleChange}
            required
          />
        </div >
        <div >
          <label >Zipcode:</label > <br />
          <input
            name="zipcode"
            value={form.zipcode}
            onChange={handleChange}
            required
          />
        </div >
        <div >
          <label >House Number:</label > <br />
          <input
            name="houseno"
            value={form.houseno}
            onChange={handleChange}
            required
          />
        </div >
        <div >
          <label >Date of Birth:</label > <br />
          <input
            type="date"
            name="dob"
            value={form.dob}
            onChange={handleChange}
            required
          />
        </div >
        <div >
          <label >Time:</label > <br />
          <input
            type="time"
            name="time"
            value={form.time}
            onChange={handleChange}
            required
          />
        </div >
        <div >
          <label >Create Time:</label > <br />
          <input
            type="datetime-local"
            name="create_time"
            value={form.create_time}
            onChange={handleChange}
            required
          />
        </div >
        <br/>
        <button type="submit">Submit</button>
      </form>
    </div >
  );
}

export default App;