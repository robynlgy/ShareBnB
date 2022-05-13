import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Alert from "./shared/Alert";

/** Form component used for logging in user.
 * props: login
 * state: formData
 */
function LoginForm({ login }) {
  const initialValue = {
    username: "",
    password: "",
  };
  const [formData, setFormData] = useState(initialValue);
  const navigate = useNavigate();
  const [alerts, setAlerts] = useState(null);

  /** Update form input. */
  function handleChange(evt) {
    const { name, value } = evt.target;
    setFormData((fData) => ({
      ...fData,
      [name]: value,
    }));
  }

  /** Call parent function. */
  async function handleSubmit(evt) {
    evt.preventDefault();
    try {
      await login(formData);
      navigate("/");
    } catch (err) {
      setAlerts(err);
    }
  }

  const formInputsHTML = (
    <div className="mb-3">
      <label htmlFor="signup-username">Username: </label>
      <input
        id="signup-username"
        name="username"
        className="form-control"
        placeholder="Enter username"
        onChange={handleChange}
        value={formData.username}
        aria-label="signup-form-username"
      />
      <label htmlFor="signup-password">Password: </label>
      <input
        type="password"
        id="signup-password"
        name="password"
        className="form-control"
        placeholder="Enter password"
        onChange={handleChange}
        value={formData.password}
        aria-label="signup-form-password"
      />
    </div>
  );

  return (
    <form
      className="justify-content-center container bg-dark mt-5 py-3 rounded-3"
      onSubmit={handleSubmit}
    >
      {formInputsHTML}

      {alerts && <Alert alerts={alerts} />}

      <button className="btn-outline-light btn ms-3 py-1 btn-sm">
        Login
      </button>
    </form>
  );
}

export default LoginForm;
