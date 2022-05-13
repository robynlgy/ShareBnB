import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Alert from "./shared/Alert";

/** Form component used for creating a new listing.
 * props: listing
 * state: formData
 */
function ListingForm({ addListing }) {
  const initialValue = {
    name:"",
    price:"",
    location:"",
    details:"",
    listingType:"",
  };
  const [formData, setFormData] = useState(initialValue);
  const navigate = useNavigate();
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
      navigate("/listings");
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
      />
      <label htmlFor="price">Price: </label>
      <input
        id="price"
        name="price"
        className="form-control"
        placeholder="Enter price"
        onChange={handleChange}
        value={formData.price}
        aria-label="price"
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
      />

    </div>
  );

  return (
    <form
      className="justify-content-center container bg-light"
      onSubmit={handleSubmit}
    >
      {formInputsHTML}

      {alerts && <Alert alerts={alerts} />}

      <button className="btn btn-primary ms-3 py-1 btn-sm">
        Submit
      </button>
    </form>
  );
}

export default ListingForm;
