import { useState, useEffect } from "react";
import ShareBBApi from "./api";
import LoadingSpinner from "./shared/LoadingSpinner";
import ListingCard from "./ListingCard";

/** Presentational Component for each list item in list of Listings,
 * linking to their detail page
 * props: listing
 */

function UserListing() {
  const [listings, setListing] = useState({
    data: [],
    isLoading: true,
  });

  useEffect(
    function getUserListing() {
      async function fetchUserListingFromAPI() {
        const listingResp = await ShareBBApi.getCurrUserListing();
        setListing((prev) => ({ ...prev, data:[...listingResp], isLoading:false }));
      }
      if (listings.isLoading) fetchUserListingFromAPI();
    },
    [listings]
  );


  if (listings.isLoading) return <LoadingSpinner />;

  return (
    <div className=" my-3 p-3 container">
      {listings.data.map((listing) => (
        <ListingCard key={listing.id} listing={listing} />
      ))}
    </div>
  );
}

export default UserListing;
