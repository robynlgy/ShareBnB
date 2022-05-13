import { useState, useEffect } from "react";
import ShareBBApi from "./api";
import LoadingSpinner from "./shared/LoadingSpinner";
import ListingForm from "./ListingForm";
import ListingCard from "./ListingCard";
import { useContext } from "react";
import UserContext from "./UserContext";

/** ListingsList component
 *
 * state: listings
 * props: none
 */

function ListingsList() {
  const [listings, setListings] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const { currentUser } = useContext(UserContext);

  useEffect(
    function getListings() {
      async function fetchListingsFromAPI() {
        const listingsResp = await ShareBBApi.getListings();
        console.log("listingsResp",listingsResp)
        setListings([...listingsResp]);
        setIsLoading(false);
      }
      if (isLoading) fetchListingsFromAPI();
    },
    [listings]
  );

  async function addListing(formData){
    const response = await ShareBBApi.addListing(formData)
    setListings([...listings, response])
  }

  if (isLoading) return < LoadingSpinner />

  return (
    <div className="pb-5">
      {currentUser && <ListingForm addListing={addListing}/>}

      {listings.map((listing)=>(
        <ListingCard key={listing.id} listing={listing}/>
      ))}
    </div>
  );
}

export default ListingsList;
