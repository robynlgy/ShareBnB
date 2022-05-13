import { useState } from "react";
import Alert from "./shared/Alert";

/** Form component used for creating a new listing.
 * props: addListing
 * state: formData, alerts
 */
function ListingForm({ addListing, toggleForm }) {
  const initialValue = {
    name:"",
    price:"",
    location:"",
    details:"",
    listingType:"",
  };
  const [formData, setFormData] = useState(initialValue);
  const [alerts, setAlerts] = useState(null)

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
      await addListing(formData);
      setAlerts(["Successfully added!"])
      setTimeout(()=>{
        toggleForm()
      },2000)
    } catch (err) {
      console.log("errors",err)
      // setAlerts(err)
    }
  }

  const formInputsHTML = (
    <div className="mb-3">
      <label htmlFor="name">Name: </label>
      <input
        id="name"
        name="name"
        className="form-control"
        placeholder="Enter name"
        onChange={handleChange}
        value={formData.name}
        aria-label="name"
        required
      />
      <label htmlFor="price">Price: </label>
      <input
        type="number"
        id="price"
        name="price"
        className="form-control"
        placeholder="Enter price"
        onChange={handleChange}
        value={formData.price}
        aria-label="price"
        required
      />
      <label htmlFor="location">Location: </label>
      <input
        id="location"
        name="location"
        className="form-control"
        placeholder="Enter location"
        onChange={handleChange}
        value={formData.location}
        aria-label="location"
        required
      />
      <label htmlFor="details">Details: </label>
      <input
        id="details"
        name="details"
        className="form-control"
        placeholder="Enter details"
        onChange={handleChange}
        value={formData.details}
        aria-label="details"
        required
      />
      <label htmlFor="listingType">Listing type: </label>
      <input
        id="listingType"
        name="listingType"
        className="form-control"
        placeholder="Enter listing type"
        onChange={handleChange}
        value={formData.listingType}
        aria-label="listingType"
        required
      />

    </div>
  );

  return (
    <form
      className="custom-form justify-content-center container bg-dark rounded-3 py-2 my-2"
      onSubmit={handleSubmit}
    >
      {formInputsHTML}

      {alerts && <Alert alerts={alerts} />}

      <button className="btn btn-outline-light ms-3 py-1 btn-sm">
        Submit
      </button>
    </form>
  );
}

export default ListingForm;
