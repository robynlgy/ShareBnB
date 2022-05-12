import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Alert from "./shared/Alert";
import ShareBBApi from "./api";

function ListingForm() {

  // const [formData, setFormData] = useState(initialValue);
  const [selectedFile, setSelectedFile] = useState();
  const [isFilePicked, setIsFilePicked] = useState(false);
  const navigate = useNavigate();
  const [alerts, setAlerts] = useState(null);


  async function addImage(id, imageData) {
    const response = await ShareBBApi.listingImage(id, imageData);
  }

  /** Call parent function. */
  async function handleSubmit(evt) {
    evt.preventDefault();
    const formData = new FormData();
    formData.append('File', selectedFile);
    console.log('formData',formData);
    console.log('selectedFile',selectedFile);
    try {
      const result = await addImage(1,formData);
      console.log('Success:', result)
    } catch (err) {
      // setAlerts(err);
      console.log(err)
    }
  }

  const changeHandler = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsFilePicked(true);
  };

  return (
    <form
      className="justify-content-center container bg-light"
      onSubmit={handleSubmit}
    >
      {/* {formInputsHTML} */}

      <input
        type="file"
        id="file"
        name="file"
        className="form-control"
        aria-label="file-url"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />
      <div>
 
      {/* {alerts && <Alert alerts={alerts} />} */}
      </div>
      <button className="btn-primary btn ms-3 py-1 btn-sm">
        Submit
      </button>
    </form>
  );
}
export default ListingForm;