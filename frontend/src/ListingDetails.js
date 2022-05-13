import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import ShareBBApi from "./api";
import LoadingSpinner from "./shared/LoadingSpinner";
import ListingImageForm from "./ListingImageForm";
import { useContext } from "react";
import UserContext from "./UserContext";

/** Presentational Component for each list item in list of Listings,
 * linking to their detail page
 * props: listing
 */

function ListingDetails() {
  const { id } = useParams();
  const [listing, setListing] = useState({
    data: {},
    isLoading: true,
  });

  const { currentUser } = useContext(UserContext);

  useEffect(
    function getListing() {
      async function fetchListingFromAPI() {
        const listingResp = await ShareBBApi.getListing(id);
        setListing(() => ({ data: { ...listingResp }, isLoading: false }));
      }
      if (listing.isLoading) fetchListingFromAPI();
    },
    [listing, id]
  );

  async function changeImage() {
    setListing((prev) => ({ ...prev, isLoading: true }));
  }

  if (listing.isLoading) return <LoadingSpinner />;
  return (
    <div className="bg-dark my-3 d-flex p-3 container">
      <div className="row">
      {listing.data.imageUrl && (
        <img
          className="listing-detail-img"
          src={listing.data.imageUrl}
          alt={`listing-${id}`}
        />
      )}
      </div>
      <div className="text-start ms-5">
        <h4>{listing.data.name}</h4>
        <p>{listing.data.location}</p>
        <p>{listing.data.price}</p>
        <p>{listing.data.listingType}</p>
        <p>{listing.data.detail}</p>
        {(currentUser && currentUser.username === listing.data.hostUsername) ?
          <ListingImageForm changeImage={changeImage} id={id} />
          :
          <button className="btn btn-outline-light mt-5">Message host (Coming Soon!)</button>
        }

      </div>
    </div>
  );
}

export default ListingDetails;
